<p align="center">
    <h1> brute </h1>
    <a href="https://github.com/ex0dus-0x/brute/issues"><img src="https://img.shields.io/github/issues/ex0dus-0x/brute.svg" alt="Github forks"></img></a>
    <a href="https://raw.githubusercontent.com/ex0dus-0x/brute/master/LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></img></a>

</p>

Crowd-sourced credential stuffing engine built for security professionals

## Introduction

__brute__ is a Python-based library framework and engine that enables security professionals to rapidly construct bruteforce / credential stuffing attacks. It features both a multi-purpose command-line application (`brute`), and a software library that can be used in tandem to quickly generate standalone module scripts for attack.

You can use __brute__ to:

* Quickly launch an attack with the `brute` CLI with an included module (ie. SMTP server, or a Twitter account)
* Use the CLI to generate a module, which you can then run as a standalone script, or incorporate as part of your local module registry
* Use community modules from the global registry to "crowdsource" your attacks (NOTE: global registry is WIP)

### What can you do with it?

* Rapidly test publicly leaked credential corpora against multiple services.
* Construct PoC scripts quickly to test rate-limiting for authentication systems.
* Launch an active credential reuse campaign as part of an OSINT profile.

## Features

* __Functional__ - works out-of-the-box with 7 default modules for attacks on both network protocols and web-based services
* __Simple to use__ - launch an attack or implement an attack module in minutes and fewer lines of code!
* __Plugin manager__ - implement your own attack modules, and upload them to the local and global registry, or pull others from the community.
* __Logging facilities__ - incorporate dumped logs into a logging pipeline / SIEM.

## Usage

`brute` is built for Python 3.7+, and should work with any platform, preferably macOS/Linux.

To use `brute`, you can either install through `pip`:

```
$ pip install brute --user
```

or build locally:

```
$ git clone https://github.com/ex0dus-0x/brute
$ cd brute/
$ python3 setup.py install
```

### CLI Usage

```
usage: brute [-h] [--list_modules] [--add_module ADD_MODULE] [--new_module NEW_MODULE] [-m MODULE] [-u USERNAME] [-w WORDLIST]
             [-a ADDRESS] [-p PORT] [-d DELAY]

crowd-sourced credential stuffing engine

optional arguments:
  -h, --help            show this help message and exit

Module Management:
  --list_modules        List out the currently available modules in the local registry.
  --add_module ADD_MODULE
                        Add a new module to the local registry.
  --new_module NEW_MODULE
                        Given a specifier (type/name), initializes a new module plugin script to current dir.

Launching an Attack:
  -m MODULE, --module MODULE
                        Provide a valid module to be executed.
  -u USERNAME, --username USERNAME
                        Provide a valid username/identifier for module being executed
  -w WORDLIST, --wordlist WORDLIST
                        Provide a file path or directory to a wordlist
  -a ADDRESS, --address ADDRESS
                        Provide host address for specified service. Required for certain protocols
  -p PORT, --port PORT  Provide port for host address for specified service. If not specified, will be automatically set as default.
  -d DELAY, --delay DELAY
                        Provide the number of seconds the program delays as each password is tried
```

To interact with the modules in your local registry, you can do the following:

```
# show all modules in registry
$ brute --list_modules

# create a new plugin script
$ brute --new_module web/mysite

# .. edit it with functionality
$ vim mysite.py

# now you can run it normally ...
$ python3 mysite.py --username test --wordlist wordlist.txt

# .. or add it to the registry and use it with the cli
$ brute --add_module mysite.py
$ brute -m mysite --username test --wordlist wordlist.txt
```

### Library

(TODO)

## Contributing

If you have any proposed changes, please make a pull request or issue!

brute was designed as a pragmatic approach towards credential stuffing and reuse. In no way does it endorse malicious hacking. Please do not support the use of this code as a method of advancing black-hat activites.

## License

[MIT](https://codemuch.tech/license.txt)
