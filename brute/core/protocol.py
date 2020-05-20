"""
protocol.py

    Defines the base parent object used for instantiating a module
    that targets network protocols other than HTTP/HTTPs
"""

import argparse
import dataclasses
import typing as t

from brute.core.base import BruteBase


@dataclasses.dataclass
class ProtocolBruteforce(BruteBase):
    """
    Parent object inheriting BruteBase, extending attributes and methods to use
    when attempting to bruteforce against network-based protocols.
    """

    # overrides from base
    address: t.Optional[str] = None

    # default port the service should reside on
    port: int = dataclasses.field(default_factory=int)


    def __str__(self) -> str:
        return f"{self.name}"


    @classmethod
    def parse_args(cls) -> argparse.Namespace:

        # check if child classes already initialized and parsed arguments
        if cls._args:
            return cls._args

        # check if child classes already initialized an argument parser with options
        if not cls._parser:
            parser: argparse.ArgumentParser = argparse.ArgumentParser(f"{str(cls)} standalone credential stuffing module")
        else:
            parser: argparse.ArgumentParser = cls._parser

        parser.add_argument("-a", "--address", dest="address",
            help="Provide host address for protocol attack, otherwise default attribute will be used."
        )

        parser.add_argument(
            "-p", "--port", type=int, dest="port", default=cls.port,
            help="Provide port for host address for specified service. If not specified, will be automatically set as default."
        )

        # set parser, and finalize initialization in subclass
        cls._parser = parser
        return super().parse_args()
