import os
import json
import logging
import requests
import time
import platform
from requests.adapters import HTTPAdapter
from requests.cookies import create_cookie
from requests.packages.urllib3.util.retry import Retry
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWidgets import qApp
from PyQt5.QtNetwork import QNetworkCookie
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from deriva.core import read_config, read_credential, write_credential, get_credential, load_cookies_from_file, \
    format_exception, DEFAULT_SESSION_CONFIG, DEFAULT_CREDENTIAL, DEFAULT_CREDENTIAL_FILE, DEFAULT_COOKIE_JAR_FILE
from deriva.core.utils.version_utils import get_installed_version
from deriva.qt import __version__ as VERSION

DEFAULT_CONFIG = {
    "servers": [],
    "cookie_jars": [
        DEFAULT_COOKIE_JAR_FILE,
        os.path.join(os.path.expanduser(os.path.normpath("~/.bdbag")), "deriva-cookies.txt")
    ]
}

DEFAULT_CONFIG_FILE = os.path.join(os.path.expanduser(os.path.normpath("~/.deriva")), "auth-agent-config.json")

DEFAULT_HTML = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>DERIVA Auth Agent</title></head>' \
               '<body style="text-align: center; vertical-align: middle;">' \
               '<div style = "margin-top: 50px;"><font size="+2">' \
               'Authenticating to:<br/><br/><b>%s</b><br/><br/>Please wait...</font></div>' \
               '</body></html>'

ERROR_HTML = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Error</title></head>' \
             '<body style="text-align: center; vertical-align: middle;">%s</body></html>'

SUCCESS_HTML = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">' \
               '<title>Authentication Success</title></head>' \
               '<body style="text-align: center; vertical-align: middle;">' \
               '<div style = "margin-top: 50px;"><font size="+2"><b>Authentication Successful.</b></font></div>' \
               '</body></html>'


class AuthWidget(QWebEngineView):

    def __init__(self, parent, config=None, credential_file=None, cookie_persistence=False, log_level=logging.INFO):
        super(AuthWidget, self).__init__(parent)

        self.parent = parent
        self.config = None
        self.config_file = DEFAULT_CONFIG_FILE
        self.credential = DEFAULT_CREDENTIAL
        self.credential_file = None
        self.cookie_file = None
        self.cookie_jar = None
        self.auth_url = None
        self.authn_session = None
        self.authn_session_page = None
        self.authn_cookie_name = None
        self.authn_expires = time.time()
        self._success_callback = None
        self._failure_callback = None
        self._session = requests.session()
        self.token = None
        self.default_profile = QWebEngineProfile("deriva-auth", self)
        self.private_profile = QWebEngineProfile(self)

        logging.getLogger().setLevel(log_level)
        info = "%s v%s [Python: %s (PyQt: %s), %s]" % (
            self.__class__.__name__, get_installed_version(VERSION),
            platform.python_version(), PYQT_VERSION_STR, platform.platform(aliased=True))
        logging.info("Initializing authorization provider: %s" % info)
        self.cookie_persistence = cookie_persistence
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._onTimerFired)
        self.configure(config, credential_file)

    def configure(self, config, credential_file):
        self.config = config if config else read_config(self.config_file, create_default=True, default=DEFAULT_CONFIG)
        self.credential_file = credential_file if credential_file else DEFAULT_CREDENTIAL_FILE
        host = self.config.get("host")
        if not host:
            self.set_current_html(ERROR_HTML % "Could not locate hostname parameter in configuration.")
            return
        self.auth_url = QUrl()
        self.auth_url.setScheme(config.get("protocol", "https"))
        self.auth_url.setHost(host)
        if config.get("port") is not None:
            self.auth_url.setPort(config["port"])
        self.authn_cookie_name = self.config.get("cookie_name", "webauthn")

        self.cookie_file = DEFAULT_SESSION_CONFIG.get("cookie_jar")
        self.cookie_jar = load_cookies_from_file(self.cookie_file)

        retries = Retry(connect=DEFAULT_SESSION_CONFIG['retry_connect'],
                        read=DEFAULT_SESSION_CONFIG['retry_read'],
                        backoff_factor=DEFAULT_SESSION_CONFIG['retry_backoff_factor'],
                        status_forcelist=DEFAULT_SESSION_CONFIG['retry_status_forcelist'])

        self._session.mount(self.auth_url.toString() + '/',
                            HTTPAdapter(max_retries=retries))

    def set_current_html(self, html):
        page = QWebEnginePage(self.parent)
        page.setHtml(html)
        self.setPage(page)
        self.update()
        qApp.processEvents()

    def authenticated(self, get_session=True):
        if self.authn_session is None and get_session:
            credentials = get_credential(self.config["host"])
            if credentials and 'bearer-token' in credentials:
                if not self.token:
                    logging.info("Authenticating to [%s] using externally issued bearer token." %
                                 self.auth_url.toString())
                    self._session.headers.update(
                        {'Authorization': 'Bearer {token}'.format(token=credentials['bearer-token'])})
                    r = self._session.get(self.auth_url.toString() + "/authn/session")
                    if r.status_code == 200:
                        self._onSessionContent(r.json())
                        self.token = self._session.headers["Authorization"]
                        self.credential = credentials
                        return True
            return False

        now = time.time()
        if now >= self.authn_expires:
            return False

        return True

    def login(self):
        if self.authenticated():
            return
        if not (self.auth_url and (self.auth_url.host() and self.auth_url.scheme())):
            logging.error("Missing or invalid hostname parameter in configuration.")
            return
        logging.info("Authenticating to host: %s" % self.auth_url.toString())
        qApp.setOverrideCursor(Qt.WaitCursor)
        self._cleanup()
        self.authn_session_page = QWebEnginePage(self.private_profile, self.parent) \
            if not self.cookie_persistence else QWebEnginePage(self.default_profile, self.parent)
        self.authn_session_page.profile().setPersistentCookiesPolicy(
            QWebEngineProfile.ForcePersistentCookies if self.cookie_persistence else
            QWebEngineProfile.NoPersistentCookies)
        if self.cookie_persistence:
            logging.debug("QTWebEngine persistent storage located at: %s" %
                          self.authn_session_page.profile().persistentStoragePath())
        self.authn_session_page.profile().cookieStore().cookieAdded.connect(self._onCookieAdded)
        self.authn_session_page.profile().cookieStore().cookieRemoved.connect(self._onCookieRemoved)
        self.authn_session_page.loadProgress.connect(self._onLoadProgress)
        self.authn_session_page.loadFinished.connect(self._onLoadFinished)

        self.authn_session_page.setUrl(QUrl(self.auth_url.toString() + "/authn/preauth"))
        self.setPage(self.authn_session_page)

    def logout(self, delete_cookies=False):
        if not (self.auth_url and (self.auth_url.host() and self.auth_url.scheme())):
            return
        if self.authenticated(False):
            try:
                logging.info("Logging out of host: %s" % self.auth_url.toString())
                auth_header = self._session.headers.get("Authorization")
                if auth_header and (auth_header.startswith("Bearer ") or auth_header.startswith("bearer ")):
                    logging.info("An externally created bearer token was used to login to: %s. The logout process will "
                                 "invalidate your current session but will not automatically revoke this token." %
                                 self.auth_url.toString())
                if delete_cookies and self.cookie_persistence:
                    if self.authn_session_page:
                        self.authn_session_page.profile().cookieStore().deleteAllCookies()
                self._session.delete(self.auth_url.toString() + "/authn/session")
                if self.credential_file:
                    creds = read_credential(self.credential_file, create_default=True)
                    host = self.auth_url.host()
                    if creds.get(host):
                        del creds[host]
                    write_credential(self.credential_file, creds)
            except Exception as e:
                logging.warning("Logout error: %s" % format_exception(e))
        self._cleanup()

    def setSuccessCallback(self, callback=None):
        self._success_callback = callback

    def setFailureCallback(self, callback=None):
        self._failure_callback = callback

    def setStatus(self, message):
        if self.window().statusBar is not None:
            self.window().statusBar().showMessage(message)

    def _execSuccessCallback(self):
        if self._success_callback:
            self._success_callback(host=self.auth_url.host(), credential=self.credential)

    def _execFailureCallback(self, message):
        if self._failure_callback:
            self._failure_callback(host=self.auth_url.host(), message=message)

    def _onTimerFired(self):
        if not self.authenticated():
            self.authn_session = None
            return
        resp = self._session.put(self.auth_url.toString() + "/authn/session")
        seconds_remaining = self.authn_session['seconds_remaining']
        self.authn_expires = time.time() + seconds_remaining + 1
        if resp.ok:
            logging.trace("webauthn session:\n%s\n", resp.json())
            logging.info("Session refreshed for: %s" % self.auth_url.host())
        else:
            logging.warning(
                "Unable to refresh session for: %s. Server responded: %s" %
                (self.auth_url.host(),
                 str.format("%s %s: %s" % (resp.status_code, resp.reason, resp.content.decode()))))

    def _onSessionContent(self, content):
        try:
            qApp.restoreOverrideCursor()
            self.set_current_html(SUCCESS_HTML)
            try:
                self.authn_session = json.loads(content) if isinstance(content, str) else content
            except json.JSONDecodeError:
                raise RuntimeError("Unable to parse response from server: %s" % content)
            seconds_remaining = self.authn_session['seconds_remaining']
            if not self._timer.isActive():
                interval = seconds_remaining // 2
                logging.info("Authentication successful for [%s]: credential refresh in %d seconds." %
                             (self.auth_url.toString(), interval))
                self._timer.start(interval * 1000)
            self.authn_expires = time.time() + seconds_remaining + 1
            logging.trace("webauthn session:\n%s\n", json.dumps(self.authn_session, indent=2))
            QTimer.singleShot(100, self._execSuccessCallback)
        except (ValueError, Exception) as e:
            error = format_exception(e)
            logging.error(error)
            self.set_current_html(ERROR_HTML % content)
            self._execFailureCallback(error)

    def _onPreAuthContent(self, content):
        try:
            if not content:
                logging.debug("no preauth content")
                return
            preauth = json.loads(content)
            logging.trace("webauthn preauth:\n%s\n", json.dumps(preauth, indent=2))
            qApp.setOverrideCursor(Qt.WaitCursor)
            self.authn_session_page.setUrl(QUrl(preauth["redirect_url"]))
        except (ValueError, Exception) as e:
            logging.error(format_exception(e))
            self.set_current_html(ERROR_HTML % content)

    def _onLoadFinished(self, result):
        qApp.restoreOverrideCursor()
        qApp.processEvents()
        if not result:
            self.setPage(self.authn_session_page)
            logging.debug("Page load error: %s" % self.authn_session_page.url().toDisplayString())
            return
        self.set_current_html(DEFAULT_HTML % self.auth_url.host())
        path = self.authn_session_page.url().path()
        if path == "/authn/preauth":
            self.authn_session_page.toPlainText(self._onPreAuthContent)
        elif path == "/authn/session":
            self.authn_session_page.toPlainText(self._onSessionContent)
        else:
            if self.page() != self.authn_session_page:
                self.page().deleteLater()
                self.setPage(self.authn_session_page)

    def _onLoadProgress(self, progress):
        self.setStatus("Loading page: %s [%d%%]" % (self.page().url().host(), progress))

    def _onCookieAdded(self, cookie):
        cookie_str = str(cookie.toRawForm(QNetworkCookie.NameAndValueOnly), encoding='utf-8')
        cookie_name = str(cookie.name(), encoding='utf-8')
        cookie_val = str(cookie.value(), encoding='utf-8')
        if (cookie_name == self.authn_cookie_name) and (cookie.domain() == self.config.get("host")):
            logging.trace("%s cookie added:\n\n%s\n\n" % (self.authn_cookie_name, cookie_str))
            self.credential["cookie"] = "%s=%s" % (self.authn_cookie_name, cookie_val)
            host = self.auth_url.host()
            cred_entry = dict()
            cred_entry[host] = self.credential
            if self.credential_file:
                creds = read_credential(self.credential_file, create_default=True)
                creds.update(cred_entry)
                write_credential(self.credential_file, creds)
            self.token = "Cookie %s" % cookie_val
            self._session.cookies.set(self.authn_cookie_name, cookie_val, domain=host, path='/')
            if self.cookie_jar is not None:
                self.cookie_jar.set_cookie(
                    create_cookie(self.authn_cookie_name,
                                  cookie_val,
                                  domain=host,
                                  path='/',
                                  expires=0,
                                  discard=False,
                                  secure=True))
                for path in self.config.get("cookie_jars", DEFAULT_CONFIG["cookie_jars"]):
                    path_dir = os.path.dirname(path)
                    if os.path.isdir(path_dir):
                        logging.debug("Saving cookie jar to: %s" % path)
                        self.cookie_jar.save(path, ignore_discard=True, ignore_expires=True)
                    else:
                        logging.debug("Cookie jar save path [%s] does not exist." % path_dir)

    def _onCookieRemoved(self, cookie):
        cookie_str = str(cookie.toRawForm(QNetworkCookie.NameAndValueOnly), encoding='utf-8')
        cookie_name = str(cookie.name(), encoding='utf-8')
        if cookie_name == self.authn_cookie_name and cookie.domain() == self.url().host():
            logging.trace("%s cookie removed:\n\n%s\n\n" % (self.authn_cookie_name, cookie_str))
            if self.cookie_jar:
                self.cookie_jar.clear(cookie_name, path=cookie.path(), domain=cookie.domain())

    def _cleanup(self):
        self._timer.stop()
        self.token = None
        self.authn_session = None
        self.authn_expires = time.time()
        if self.authn_session_page:
            self.authn_session_page.loadProgress.disconnect(self._onLoadProgress)
            self.authn_session_page.loadFinished.disconnect(self._onLoadFinished)
            self.authn_session_page.profile().cookieStore().cookieAdded.disconnect(self._onCookieAdded)
            self.authn_session_page.profile().cookieStore().cookieRemoved.disconnect(self._onCookieRemoved)
            self.authn_session_page.deleteLater()
            self.authn_session_page = None
