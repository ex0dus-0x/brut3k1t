"""
base.py
"""

import os
import typing as t
import dataclasses


class BruteException(Exception):
    """
    Defines a custom exception class for the Brute* objects
    """
    pass


@dataclasses.dataclass
class BruteBase(object):
    """
    Root base dataclasses.dataclass to inherit properties and methods
    for instantiation of a Brute module. Contains the most basic
    attributes and methods needed to operate, and should be inherited
    by a parent bruteforce object, not directly by modules.
    """

    # name of the target undergoing testing, primarily used for
    # identification and display.
    name: str

    # target username, or any fixed identifier (ie hash) necessary for bruteforcing.
    username: t.Optional[str]

    # wordlist is a placeholder attribute that is replaced by the wordlist property method. When
    # called, _wordlist_path is returned, but when set, the _wordlist pool is populated from a given path.
    wordlist: str
    _wordlist_path: str = dataclasses.field(init=False, repr=False)
    _wordlist: t.List[str] = dataclasses.field(init=False, repr=False)

    # latency between each request, default is 5 sec.
    delay: int = 5

    # log to store per request transaction. Can be dumped for further analysis.
    # TODO: custom logging
    log: t.Dict[str, str] = dataclasses.field(default_factory=dict)


    def __repr__(self) -> str:
        return "{}".format(self.name)


    @property
    def wordlist(self) -> str:
        """
        When the wordlist property is called, the path is returned instead
        of the private wordlist pool.
        """
        return self._wordlist_path


    @wordlist.setter
    def wordlist(self, path: str) -> None:
        """
        Instantiates the wordlist pool from a path, whether a single file or dir.

        :type path: file or directory inode with wordlists
        """

        # initialize path to wordlists for display purposes
        self._wordlist_path = os.path.abspath(path)

        # initialize corpus pool for wordlists
        self._wordlist = []

        # enumerate directory and initialize pool with all files
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if os.path.isfile(filename):
                    with open(os.path.join(path, filename), 'r') as f:
                        self._wordlist += f.readlines()

        # otherwise read file normally
        elif os.path.isfile(path):
            with open(path, 'r') as f:
                self._wordlist += f.readlines()
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
        Initializes necessary objects, environment, etc. before starting the bruteforce execution loop.
        """
        raise NotImplementedError("must be implemented by module or module parent")


    def sanity(self) -> int:
        """
        Defines a sanity check to perform before execution, such as sending a single request to determine availability / uptime.
        Should return an zero integer status to inform the execution routine that the service is available.
        """
        raise NotImplementedError("must be implemented by module or module parent")


    def brute(self, username: str, pwd_guess: str) -> str:
        """
        Defines a single authorization request against the target service. This methods should be implemented by the user in order
        to represent how the request is initialized with a user/pwd combo and sent, and should return a status message to check.

        :type username: username to guess. Specified if future implementation allows cracking multiple usernames at once.
        :type pwd_guess: represents the password guess currently loaded to test.
        """
        raise NotImplementedError("must be implemented by module or module parent")


    def run(self) -> None:
        """
        Runs the full bruteforce execution. First, `init` is called to setup the environment, and a sanity-check is
        optionally imposed. The main execution loop is called, with the implemented `brute()` method called per word
        in the wordlist to authenticate.

        The user should NOT re-implement run() unless the service being tested deviates from specification greatly.
        """

        # initialize the environment for bruteforcing
        self.init()

        # run a sanity-check in order to ensure that the service is available
        # TODO: change out exception block for something safer
        try:
            if self.sanity() != 0:
                raise BruteException("Target service failed sanity check, may not be available.")
        except NotImplementedError:
            print("Skipping the sanity-check, not implemented")

        # bruteforce execution loop: send a single authentication request per word, and check to see if the
        # strings set in success/fail are in the response.
        for word in self.wordlist:
            try:
                resp = self.brute()
                if self.success in resp:
                    print("Good!")
                else:
                    print("bad!")

            except Exception as e:
                raise BruteException("Caught exception {} when running bruteforce execution loop".format(e))
