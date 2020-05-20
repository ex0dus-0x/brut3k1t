#!/usr/bin/env python3
"""
ftp.py

    Module Name:
        ftp

    Author:
        YOU <you@email.com>

    Description:
        DESCRIPTION
"""

import dataclasses

# include any other networking imports needed!

from brute.core.protocol import ProtocolBruteforce


@dataclasses.dataclass
class Ftp(ProtocolBruteforce):
    name = "ftp"

    address = 2
    port = 2


    @property
    def success(self) -> int:
        return 0


    def init(self):
        """
        Performs the necessary initialzation in order to interact
        with the service. This means creating any client objects,
        setting up the environment, etc.
        """
        pass


    #def sanity(self):


    def brute(self, username, pwd_guess) -> int:
        """
        `brute()` should be implemented to represent how a single
        response against the service would be done. The engine will then
        use this as a callback during the bruteforce execution.
        """
        pass



if __name__ == "__main__":
    args = Ftp.parse_args()
    Ftp(
        address = args.address,
        username = args.username,
        wordlist = args.wordlist,
        delay = args.delay,
        port = args.port
    ).run()
