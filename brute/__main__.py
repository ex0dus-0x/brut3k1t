#!/usr/bin/env python3
"""
__main__.py

    Main CLI entry point to the `brute` application, which provides
    an interface for selecting attack modules, or incorporating new ones.
"""
import os
import argparse

import brute.manager
import brute.logger

# for our CLI, we just want to print normally.
logger = brute.logger.BruteLogger(__name__)


def main():
    print("""
  _                _   _____
 | |__  _ __ _   _| |_|___ /
 | "_ \| "__| | | | __| |_ \
 | |_) | |  | |_| | |_ ___) |
 |_.__/|_|   \__,_|\__|____/
    security-oriented bruteforce/credential stuffing framework.
""")

    parser = argparse.ArgumentParser(description="Security-oriented bruteforce/credential-stuffing framework")

    # defines the module management argument group to interact with attack modules.
    module = parser.add_argument_group("Module Management")
    module.add_argument(
        "--list_modules", dest="list_modules",
        help="List out the currently available modules in the local registry."
    )
    module.add_argument(
        "--add_module", dest="add_module",
        help="Add a new module to the local registry."
    )
    module.add_argument(
        "--new_module", dest="new_module",
        help="Given a specifier (type/name), initializes a new module plugin script to current dir."
    )

    # defines the attack argument group, which provisions a module for an actual attack.
    attack = parser.add_argument_group("Launching an Attack")
    attack.add_argument(
        "-m", "--module", dest="module",
        help="Provide a valid username/hashstring for service/protocol/hashcrack being executed."
    )
    attack.add_argument(
        "-u", "--username", dest="username",
        help="Provide a valid username/hashstring for service/protocol/hashcrack being executed"
    )
    attack.add_argument(
        "-w", "--wordlist", dest="wordlist",
        help="Provide a wordlist or directory to a wordlist"
    )
    attack.add_argument(
        "-a", "--address", dest="address",
        help="Provide host address for specified service. Required for certain protocols"
    )
    attack.add_argument(
        "-p", "--port", type=int, dest="port",
        help="Provide port for host address for specified service. If not specified, will be automatically set"
    )
    attack.add_argument(
        "-d", "--delay", type=int, dest="delay", default=5,
        help="Provide the number of seconds the program delays as each password is tried"
    )
    args = parser.parse_args()

    # startup our manager to interact with module registry
    manager = brute.manager.BruteManager()

    # handle module-management arguments and exit after
    if args.list_modules:
        print(manager.stats)
        exit(0)

    if args.new_module:
        (modtype, name) = args.new_module.split("/")
        if not modtype in manager.modtypes:
            logger.error("Module type `{}` not recognized!".format(modtype))
            exit(1)

        manager.new_module(modtype, name)
        exit(0)

    if args.add_module:
        modpath = os.path.abspath(args.add_module)
        manager.add_module(modpath)
        exit(0)


    # Specify mandatory options.
    man_options = ['username', 'wordlist']
    for m in man_options:
        if not args.__dict__[m]:
            parser.print_help()
            logger.error("[!] You have to specify a username AND a wordlist! [!]")
            exit(1)

    # Detect if service arg is provided
    if args.module is None:
        logger.error("[!] No module name specified! [!]")
        exit(1)

    # Detect is wordlist path is correct
    if os.path.exists(args.wordlist) == False:
        logger.error("[!] Wordlist not found! [!]")
        exit(1)

    # retrieve module from arguments
    _module = manager.get_module(args.module)
    if _module is None:
        logger.error("[!] No module found with name `{}`".format(args.module))

    # initialize module with parameters and run
    module = _module(
        username=args.username,
        wordlist=args.wordlist,
        delay=args.delay
    )
    module.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.error("\n[!] Keyboard Interrupt detected! Killing program... [!]")
        exit(1)
