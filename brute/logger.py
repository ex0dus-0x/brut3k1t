"""
logger.py

    Defines interfaces used to consume and handle outputs in brute.
"""

class Color:
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
        :type log_level:
            0 = output all, no logging
            1 = output errors
            2 = output warnings
            3 = output all, with logging

        :type out_log: path to file to write log to.
        """
        self.level = log_level
        self.out_log = out_log


    ######################
    # General program I/O
    ######################

    @staticmethod
    def warn(input_str: str):
        print(f"{Color.O}{input_str}{Color.W}")

    @staticmethod
    def error(input_str: str):
        print(f"{Color.R}{input_str}{Color.W}")

    @staticmethod
    def good(input_str: str):
        print(f"{Color.G}{input_str}{Color.W}")

    @staticmethod
    def output(color: Color, input_str: str, end_color = Color.W):
        print(f"{color}{input_str}{end_color}")

    #########################
    # Authentication Handlers
    #########################

    def auth_success(self, user, pwd):
        self.good(f"[*] Username: {user} | [*] Password found: {pwd}\n")

    def auth_fail(self, user, pwd):
        self.warn(f"[*] Username: {user} | [*] Password: {pwd} | Incorrect!\n")
