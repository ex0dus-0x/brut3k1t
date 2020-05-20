#!/usr/bin/env python3
"""
NAME.py

    Module Name:
        NAME

    Author:
        YOU <you@email.com>

    Description:
        DESCRIPTION

"""

import dataclasses

from brute.core.web import WebBruteforce


@dataclasses.dataclass
class MOD(WebBruteforce):
    name = "NAME"
    address = "https://yoururl.com"

    fields = { "username": "", "password": "" }


    @property
    def success(self):
        """
        Returns successful condition to check for in the HTTP response title
        by the engine. This change to a new title _should_ indicate a successful authentication.
        """
        return "Success!"


    #def init(self):

    #def sanity(self):

    #def brute(self):


if __name__ == "__main__":
    args = MOD.parse_args()
    MOD(
        username = args.username,
        wordlist = args.wordlist,
        delay = args.delay,
        headless = args.headless
    ).run()
