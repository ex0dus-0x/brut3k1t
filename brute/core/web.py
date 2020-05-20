"""
web.py

    Defines the WebBruteforce object for HTTP/web-based attacks.
    Implements a headless and browser mode for attack, and can be
    arbitrarily implemented for any URL endpoint doing authentication.
"""

import mechanize
import selenium
import dataclasses
import typing as t

from brute.core import base


@dataclasses.dataclass
class WebBruteforce(base.BruteBase):
    """
    Parent bruteforce object inherting from base in order
    to extend functionality for attacking HTTP/HTTPs-based web services.
    """

    # represents the base URL endpoint being targeted, without any appended parameters
    url: str = dataclasses.field(default_factory=str)

    # represents any key-value parameters needed to work with the endpoint. Should NOT include
    # the username and password field, which should appear seperate in the fields parameter.
    params: t.Optional[t.Dict[str, t.Optional[str]]] = None

    # represents a mapping for embedded field elements to find. Values should represent the form
    # params for the specific site to input with.
    fields: t.Dict[str, t.Optional[str]] = dataclasses.field(default_factory={
        "username": None,
        "password": None
    })

    # represents headers to pass with response.
    # TODO: populate and more configurations
    headers: t.Dict[str, str] = dataclasses.field(default_factory={
        "User-Agent": "Mozilla/5.0"
    })

    # if set, will not attach to an actual browser process to perform bruteforce
    headless: bool = True


    def init():
        """
        Initializes the proper browser for authentication based on configuration, and performs
        necessary error-checking.
        """

        # error if no field params are set.
        if not all(self.fields.values()):
            raise base.BruteException("no input parameters for user/pwd combo given for module.")

        if self.headless:

            # initialize headless browser
            browser = mechanize.Browser()
            browser.set_handle_robots(False)

            # configure before requesting
            cookies = mechanize.CookieJar()
            browser.set_cookiejar(cookies)
            browser.addheaders = [(k, v) for k, v in self.headers.items()]
            browser.set_handle_refresh(False)

            # initialize as attribute, and open
            self.browser = browser
            self.browser.open(self.url)

        else:
            self.browser = selenium.webdriver.Firefox()
            self.browser.get(self.url)


    def brute(self, username: str, pwd_guess: str) -> str:
        """
        Overrides based on whether we are running headless or browser mode.
        """
        if self.headless:
            return self._headless_brute(username, pwd_guess)
        else:
            return self._driver_brute(username, pwd_guess)


    def _headless_brute(self, username: str, pwd_guess: str) -> str:
        """
        Attempts authentication using a headless browser provided by mechanize. Should be the
        fast and default way to do any type of web-based bruteforcing.
        """
        self.browser.select_form(nr = 0)
        self.browser.form[self.field["username"]] = username
        self.browser.form[self.field["password"]] = pwd_guess
        response = self.browser.submit()
        return response.read()


    def _driver_brute(self, username: str, pwd_guess: str) -> str:
        """
        Uses a Firefox-based webdriver in order to attempt authentication by
        spawning actual browser processes. Should be used in the situation that
        the headless run does not yield anything successful, and more visibility is needed.
        """

        # find the username input field, and send keys
        user_elem = self.browser.find_element_by_name(self.fields["username"])
        user_elem.clear()
        user_elem.send_keys(self.username)

        # find the password input field, and send keys
        pwd_elem = self.browser.find_element_by_name(self.fields["password"])
        pwd_elem.clear()
        pwd_elem.send_keys(pwd_guess)

        # press return key to attempt to auth, and wait briefly
        pwd_elem.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
        time.sleep(2)
        return self.browser.title
