#!/usr/bin/env python3
import dataclasses

from brute.core import protocol

@dataclasses.dataclass
class SSHBruteforce(protocol.ProtocolBruteforce):
    name = "ssh"
