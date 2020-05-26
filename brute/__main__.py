#!/usr/bin/env python3
"""
__main__.py

    Main CLI entry point to the `brute` application, which provides
    an interface for selecting attack modules, or incorporating new ones.
"""

import os
import sys
import argparse

import brute.manager
import brute.logger

# for our CLI, we just want to print normally.
logger = brute.logger.BruteLogger(__name__)


def main():
    print(
        """
  _                _   _____
 | |__  _ __ _   _| |_|___ /
 | "_ \| "__| | | | __| |_ \/
 | |_) | |  | |_| | |_ ___) |
 |_.__/|_|   \__,_|\__|____/

    crowd-sourced credential stuffing engine built for security professionals
"""
    )

    parser = argparse.ArgumentParser(
        description="crowd-sourced credential stuffing engine"
    )

    # defines the module management argument group to interact with attack modules.
    module = parser.add_argument_group("Module Management")
    module.add_argument(
        "--list_modules",
        action="store_true",
        help="List out the currently available modules in the local registry.",
    )
    module.add_argument(
        "--add_module",
        dest="add_module",
        help="Add a new module to the local registry.",
    )
    module.add_argument(
        "--new_module",
        dest="new_module",
        help="Given a specifier (type/name), initialize a new module plugin.",
    )

    # defines the attack argument group, which provisions a module for an actual attack.
    attack = parser.add_argument_group("Launching an Attack")
    attack.add_argument(
        "-m", "--module", dest="module", help="Provide a valid module to be executed."
    )
    attack.add_argument(
        "-c",
        "--combo_list",
        dest="combo_list",
        help="Path to combination list (--username and --wordlist will be ignored).",
    )
    attack.add_argument(
        "-u",
        "--username",
        dest="username",
        help="Provide a valid username/identifier for module being executed",
    )
    attack.add_argument(
        "-w",
        "--wordlist",
        dest="wordlist",
        help="Provide a file path or directory to a wordlist",
    )
    attack.add_argument(
        "-a",
        "--address",
        dest="address",
        help="Provide host address for specified service. Required for certain protocols",
    )
    attack.add_argument(
        "-p",
        "--port",
        type=int,
        dest="port",
        help="Provide port for host address for specified service, otherwise default will be used",
    )
    attack.add_argument(
        "-d",
        "--delay",
        type=int,
        dest="delay",
        default=5,
        help="Provide the number of seconds the program delays as each password is tried",
    )
    args = parser.parse_args()

    # startup our manager to interact with module registry
    manager = brute.manager.BruteManager()

    # handle module-management arguments and exit after
    if args.list_modules:
        print(manager.stats)
        sys.exit(0)

    if args.new_module:
        (modtype, name) = args.new_module.split("/")
        if not modtype in manager.modtypes:
            logger.error(f"Module type `{modtype}` not recognized!")
            sys.exit(1)

        path = manager.new_module(modtype, name)
        logger.good(
            f"[*] Initialized new plugin module `{modtype}.{name}` at {path} [*]"
        )
        sys.exit(0)

    if args.add_module:
        modpath = os.path.abspath(args.add_module)
        path = manager.add_module(modpath)
        if path is None:
            logger.error("[!] Could not add new plugin to local registry [!]")
        else:
            logger.good(f"[*] Added plugin module to local registry at {path} [*]")
        sys.exit(0)

    # If a combo list path is not provided, check for fallback defaults:
    if not args.combo_list:

        # Specify mandatory options.
        man_options = ["username", "wordlist"]
        for opt in man_options:
            if not args.__dict__[opt]:
                parser.print_help()
                logger.error(
                    "[!] You have to specify a username AND a wordlist, \
                             OR a combo list! [!]"
                )
                sys.exit(1)

        # Detect is wordlist path is correct
        if not os.path.exists(args.wordlist):
            logger.error("[!] Wordlist not found! [!]")
            sys.exit(1)

    # Detect if service arg is provided
    if args.module is None:
        logger.error("[!] No module name specified! [!]")
        sys.exit(1)

    # retrieve module from arguments
    _module = manager.get_module(args.module)
    if _module is None:
        logger.error(f"[!] No module found with name `{args.module}`")

    # initialize module with all parameters and run, assuming generic type
    module = _module(
        address=args.address,
        combos=args.combo_list,
        username=args.username,
        wordlist=args.wordlist,
        delay=args.delay,
    )

    if hasattr(module, "port") and args.port:
        module.port = args.port

    module.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.error("\n[!] Keyboard Interrupt detected! Killing program... [!]")
        sys.exit(1)
