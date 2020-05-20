"""
logger.py

    Defines interfaces used to consume and handle outputs in brute.
"""

from enum import Enum
from typing import Optional


class Color(Enum):
    """
    defines an enumeration for color encodings
    """
    W = '\033[0m'       # white (normal)
    R = '\033[31m'      # red
    G = '\033[32m'      # green
    O = '\033[33m'      # orange
    B = '\033[34m'      # blue
    P = '\033[35m'      # purple
    C = '\033[36m'      # cyan
    GR = '\033[37m'     # gray



class BruteLogger:
    """
    Defines a simple module-wide logging interface.
    Enables colorized outputs, and logfile ingestion and dumping.
    """

    def __init__(self, mod: str, log_level: int = 0, out_log: str = "brute.log"):
        """
        :type log_level: if set 0, print regularly
        """
        pass

    ######################
    # General program I/O
    ######################

    def warn(input_str: str):
	print("{}{}{}".format(Color.O, input_str, Color.W))

    def error(input_str: str):
	print("{}{}{}".format(Color.R, input_str, Color.W))

    def good(input_str: str):
	print("{}{}{}".format(Color.G, input_str, Color.W))

    def output(color: Color, input_str: str, end_color = Color.W):
        print("{}{}{}".format(color, input_str, end_color))

    #########################
    # Authentication Handlers
    #########################

    def auth_success(user, pwd):
        self.good("[*] Username: {} | [*] Password found: {}\n".format(user, pwd))

    def auth_fail(user, pwd):
        self.warn("[*] Username: {} | [*] Password: {} | Incorrect!\n".format(user, pwd))
