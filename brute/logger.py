"""
logger.py

    Defines interfaces used to consume and handle outputs in brute.
"""

import enum
import time
import typing as t


class Color(enum.Enum):
    """
    Enumeration for color encodings for display.
    """

    W = "\033[0m"  # white (normal)
    R = "\033[31m"  # red
    G = "\033[32m"  # green
    O = "\033[33m"  # orange
    B = "\033[34m"  # blue
    P = "\033[35m"  # purple
    C = "\033[36m"  # cyan
    GR = "\033[37m"  # gray


class BruteLogger:
    """
    Defines a simple module-wide logging interface.
    Enables colorized outputs, and logfile ingestion and dumping.
    """

    def __init__(self, mod: str, log_level: int = 0, out_log: str = "brute.log"):
        """
        :type mod: namespace logging info is being emitted from
        :type log_level:
            0 = regular display
            1 = output errors
            2 = output warnings and errors
            3 = output all, with logging to file

        :type out_log: path to file to write log to if log_level == 3
        """
        self.mod = mod
        self.level = log_level
        self.out_log = out_log
        self.time = time.time()

    def log(self, callback: t.Callable[[str], None]) -> None:
        pass

    ######################
    # General program I/O
    ######################

    @staticmethod
    def warn(input_str: str):
        print(f"{Color.O.value}{input_str}{Color.W.value}")

    @staticmethod
    def error(input_str: str):
        print(f"{Color.R.value}{input_str}{Color.W.value}")

    @staticmethod
    def good(input_str: str):
        print(f"{Color.G.value}{input_str}{Color.W.value}")

    @staticmethod
    def output(color: Color, input_str: str, end_color: Color = Color.W):
        print(f"{color.value}{input_str}{end_color.value}")

    #########################
    # Authentication Handlers
    #########################

    def auth_success(self, user, pwd):
        self.good(f"[*] Username: {user} | [*] Password found: {pwd}\n")

    def auth_fail(self, user, pwd):
        self.warn(f"[*] Username: {user} | [*] Password: {pwd} | Incorrect!\n")

    #########################
    # Logfile interaction
    #########################

    @staticmethod
    def to_logfmt(input_dict: t.Dict[t.Any, t.Any]) -> str:
        """
        Helper for converting structed dicts into printable/loggable
        logfmt strings.

        :type input_dict: dict with any key-value type
        """
        logfmt: str = ""
        for key, val in input_dict.items():
            logfmt += f"{key}={val} "
        return logfmt
