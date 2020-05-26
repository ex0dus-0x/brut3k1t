"""
base.py

    Defines the base-level dataclass for every bruteforce module type.
    Implements the most basic properties and method required for any
    credential stuffing attack.
"""

import os
import time
import argparse
import typing as t
import dataclasses

from brute.logger import BruteLogger


class BruteException(Exception):
    """
    Defines a custom exception class for the Brute* objects
    """

    pass


@dataclasses.dataclass
class BruteBase:
    """
    Root base dataclasses.dataclass to inherit properties and methods
    for instantiation of a Brute module. Contains the most basic
    attributes and methods needed to operate, and should be inherited
    by a parent bruteforce object, not directly by modules.
    """

    # name of the target undergoing testing, primarily used for
    # identification and display.
    name: str = dataclasses.field(default_factory=str)

    # address to the specific target being tested
    address: dataclasses.InitVar[str] = None

    # defines a combo list, which is a file with a combined key value pair of usernames and
    # passwords. This should be used primarily for credential stuffing unique credentials,
    # as it's more traditionally done.
    combos: t.Optional[str] = None
    _combo_path: str = dataclasses.field(init=False, repr=False)
    _combos_dict: t.Dict[str, str] = dataclasses.field(init=False, repr=False)

    # target username, or any fixed identifier (ie hash) necessary for bruteforcing. When called,
    # username is checked to be a single username, a comma-seperated list of usernames,
    # or a path to a file.
    username: t.Optional[str] = None
    _username_path: t.Optional[str] = dataclasses.field(init=False, repr=False)
    _usernames: t.List[str] = dataclasses.field(init=False, repr=False)

    # wordlist is a placeholder attribute that is replaced by the wordlist property method. When
    # called, _wordlist_path is returned, and when set, the wordlist pool is populated
    wordlist: t.Optional[str] = None
    _wordlist_path: str = dataclasses.field(init=False, repr=False)
    _wordlist: t.List[str] = dataclasses.field(init=False, repr=False)

    # latency between each request, default is 5 sec.
    delay: int = 5

    # timeout before stopping attack, default is 0 for indefinite. If multiple usernames
    # specified, timeout will be enforced for each one before execution of the next attack.
    timeout: int = 0

    # TODO: log to store per request transaction. Can be dumped for further analysis.
    log: BruteLogger = BruteLogger(__name__)

    # private attributes for argument parsing
    _args: t.Optional[argparse.Namespace] = None
    _parser: t.Optional[argparse.ArgumentParser] = None

    def __str__(self) -> str:
        return f"{self.name}"

    @classmethod
    def parse_args(cls) -> argparse.Namespace:
        """
        Auxiliary argument parser that should be invoked for use if the plugin module
        written is being used as a standalone script.
        """

        # check if child classes already initialized and parsed arguments
        if cls._args:
            return cls._args

        # check if child classes already initialized an argument parser with options
        if not cls._parser:
            parser: argparse.ArgumentParser = argparse.ArgumentParser(
                f"{str(cls)} standalone credential stuffing module"
            )
        else:
            parser = cls._parser

        parser.add_argument(
            "-c",
            "--combo_list",
            dest="combo_list",
            help="Path to combination list (--username and --wordlist will be ignored).",
        )
        parser.add_argument(
            "-u",
            "--username",
            dest="username",
            help="Provide a valid username/identifier for module being executed. \
                 Can either be a single username, comma-seperated list of users, or a file.",
        )
        parser.add_argument(
            "-w",
            "--wordlist",
            dest="wordlist",
            help="Provide a file path, directory of files, or a HTTP URL to a wordlist.",
        )
        parser.add_argument(
            "-d",
            "--delay",
            dest="delay",
            type=int,
            default=5,
            help="Provide the number of seconds the program delays as each password is tried",
        )

        # TODO: config logging

        # parse arguments, store interally, and return
        args = parser.parse_args()
        cls._args = args
        return cls._args

    @property  # type: ignore
    def combos(self) -> str:
        """
        When combos property is called, the path to the combination file is returned.
        """
        return self._combo_path

    @combos.setter
    def combos(self, path: str) -> None:
        """
        Given a path to a combo file, parse out colon-seperated user/pass combinations.

        :type path: path to combination list
        """

        if not os.path.isfile(path):
            raise BruteException("combo path is not valid")

        # initialize combo dict
        self._combo_dict: t.Dict[str, str] = {}

        # initialize path
        self._combo_path: str = os.path.abspath(path)
        with open(self._combo_path, "r") as combofile:
            for line in combofile.readlines():
                user, pwd = line.split(":")
                self._combo_dict[user] = pwd

    @property  # type: ignore
    def username(self) -> t.Union[t.Optional[str], t.List[str]]:
        """
        When username property is called, the path to username file is returned if available,
        otherwise the list of usernames
        """
        if hasattr(self, "_username_path"):
            return self._username_path

        return self._usernames

    @username.setter
    def username(self, username: t.Optional[str]) -> None:
        """
        Instantiates username from either a single username input, a comma-seperated list,
        or a path to a file.

        :type username: represents input to be parsed
        """

        # skip if none, since combos list must be set
        if not username:
            return

        # initialize usernames list
        self._usernames: t.List[str] = []

        if os.path.isfile(username):
            self._username_path = os.path.abspath(username)
            with open(self._username_path, "r") as userfile:
                self._usernames += userfile.readlines()
        else:
            self._usernames = username.split(",")

    @property  # type: ignore
    def wordlist(self) -> str:
        """
        When the wordlist property is called, the path is returned instead
        of the private wordlist pool.
        """
        return self._wordlist_path

    @wordlist.setter
    def wordlist(self, path: t.Optional[str]) -> None:
        """
        Instantiates the wordlist pool from a path, whether a single file or dir.

        :type path: file or directory inode with wordlists
        """

        # skip if none, since combo list must be set
        if not path:
            return

        # TODO: check for HTTP link

        # initialize path to wordlists for display purposes
        self._wordlist_path = os.path.abspath(path)

        # initialize corpus pool for wordlists
        self._wordlist = []

        # enumerate directory and initialize pool with all files
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if os.path.isfile(filename):
                    with open(os.path.join(path, filename), "r") as wordfile:
                        self._wordlist += wordfile.readlines()

        # otherwise read file normally
        elif os.path.isfile(path):
            with open(path, "r") as wordfile:
                self._wordlist += wordfile.readlines()
        else:
            raise BruteException("cannot parse out wordlists from path")

    @property
    def success(self) -> t.Any:
        """
        Constructs a success response to check against in order to deem authentication with the
        target successful. This exists as a property method rather than a direct attribute, since
        responses might be more complex and dynamic than a static response string.
        """
        raise NotImplementedError("must be implemented by module or module parent")

    def init(self) -> None:
        """
        Initializes necessary objects, environment, etc. before starting the execution loop.
        """
        raise NotImplementedError("must be implemented by module or module parent")

    def sanity(self):
        """
        Defines a sanity check to perform before execution, such as sending a single request
        to determine availability / uptime. Should return an zero integer status to inform the
        execution routine that the service is available.
        """
        raise NotImplementedError("must be implemented by module or module parent")

    def brute(self, username: str, pwd_guess: str):
        """
        Defines a single authorization request against the target service. This method
        should be implemented by the user in order to represent how the request is
        initialized with a user/pwd combo and sent, and should return a status message to check.

        :type username: current username to guess.
        :type pwd_guess: represents the password guess currently loaded to test.
        """
        raise NotImplementedError("must be implemented by module or module parent")

    def run(self) -> None:
        """
        Runs the full bruteforce execution. First, `init` is called to setup the environment,
        and a sanity-check is optionally imposed. The main execution loop is called, with the
        implemented `brute()` method called per word in the wordlist to authenticate.

        The user should NOT re-implement run() unless the service being tested
        deviates from specification greatly.
        """

        # initialize the environment for bruteforcing
        self.log.good("[*] Calling initialization routine [*]")
        self.init()

        # run a sanity-check in order to ensure that the service is available
        # TODO: change out exception block for something safer
        try:
            if self.sanity() != 0:
                raise BruteException(
                    "Target service failed sanity check, may not be available."
                )
        except NotImplementedError:
            self.log.warn("[*] Skipping the sanity-check, not implemented [*]")

        # if the combos argument is specified, run against those permutations instead
        if len(self._combo_dict) != 0:
            for user, pwd in self._combo_dict.items():
                pwd = pwd.strip("\n")
                try:
                    resp = self.brute(user, pwd)
                    if self.success == resp:
                        self.log.auth_success(user, pwd)
                    else:
                        self.log.auth_fail(user, pwd)

                    # sleep and then request again
                    time.sleep(self.delay)

                except Exception as error:
                    raise BruteException(f"Caught runtime exception: `{error}`")

            return

        # bruteforce execution loop: send a single authentication request per word, and
        # check to see if the strings set in success/fail are in the response.
        for word in self._wordlist:
            word = word.strip("\n")
            try:
                resp = self.brute(self.username, word)  # type: ignore
                if self.success == resp:
                    self.log.auth_success(self.username, word)
                else:
                    self.log.auth_fail(self.username, word)

                # sleep and then request again
                time.sleep(self.delay)

            except Exception as error:
                raise BruteException(f"Caught runtime exception: `{error}`")
