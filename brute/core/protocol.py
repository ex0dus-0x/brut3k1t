"""
protocol.py

    Defines the base parent object used for instantiating a module
    that targets network protocols other than HTTP/HTTPs
"""

import dataclasses

from brute.core import base


@dataclasses.dataclass
class ProtocolBruteforce(base.BruteBase):
    """
    Parent object inheriting BruteBase, extending attributes and methods to use
    when attempting to bruteforce against network-based protocols.
    """

    # address identifier to protocol service
    address: str = dataclasses.field(default_factory=str)

    # default port the service should reside on
    port: int = dataclasses.field(default_factory=int)
