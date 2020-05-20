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

# include any other networking imports needed!

from brute.core.protocol import ProtocolBruteforce


@dataclasses.dataclass
class MOD(ProtocolBruteforce):
    name = "NAME"

    address = ??
    port = ??


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
    args = MOD.parse_args()
    MOD(
        address = args.address,
        username = args.username,
        wordlist = args.wordlist,
        delay = args.delay,
        port = args.port
    ).run()
