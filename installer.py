from time import sleep
import os, sys, signal

def handler(signal, frame):
    print R + "Interrupted! Stopping..." + W
    sys.exit(1)

signal.signal(signal.SIGINT, handler)


# Global variables for color
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray

installer_head = """
  ___________________
< brut3k1t installer! >
  -------------------
         \   ^__^
          \  (oo)\_______
             (__)\       )\/
                 ||----w |
                 ||     ||
    """

# Unix/Linux-based distros
def kali_build():

    print O + "Updating Repositories..." + W
    sleep(1.5)
    os.system("sudo apt-get update")
    print O + "Installing essential packages..." + W
    sleep(1.5)
    os.system("sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-setuptools")
    os.system("sudo apt-get install python-selenium")
    os.system("sudo apt-get install firefoxdriver")
    print O + "Installing pip modules" + W
    sleep(1.5)
    os.system("sudo pip install -r requirements.txt")
    print G + "Done installing dependences!" + O
    #print "Making symlinks and installation directories..." + W
    #os.system("mkdir /opt/brut3k1t")
    #os.system("cp -R src/ /opt/brut3k1t && cp brut3k1t.py  /opt/brut3k1t && cp run.sh /opt/brut3k1t && cp run.sh /usr/bin/brut3k1t && chmod +x /usr/bin/brut3k1t")

def ubuntu_build():
    print O + "Updating Repositories..." + W
    sleep(1.5)
    os.system("sudo add-apt-repository universe")
    os.system("sudo apt-get update")
    print O + "Installing essential packages..." + W
    sleep(1.5)
    os.system("sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-setuptools")
    os.system("sudo apt-get install python-pip") # result of universe repo
    print O + "Installing pip modules" + W
    sleep(1.5)
    os.system("sudo pip install -r requirements.txt")


# OS X / Darwin
def osx_build():
    print O + "Installing Homebrew..." + W
    sleep(1.5)
    os.system("""/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" """)
    os.system("brew install Caskroom/cask/firefox")
    os.system("sudo easy_install pip")
    print O + "Installing pip modules" + W
    sleep(1.5)
    os.system("sudo easy_install selenium")
    # If Crytography returns errorS
    os.system("brew install libffi")
    os.system("sudo pip install -r requirements.txt")
    print G + "[!] Done installing dependences! [!]" + O


print installer_head

while True:
    print "Select an Operating System"
    print "=============================="
    print "(1) Kali Linux x32/x64"
    print "(2) Ubuntu / Parrot OS i386"
    print "(3) Ubuntu / Parrot OS amd64"
    print "(4) Mac OS X / Darwin"
    print "=============================="
    print ""
    getos = raw_input(">> ")
    if getos == "1":
        kali_build()
        break
    elif getos == "2":
        ubuntu_build()
        print O + "Getting GeckoDriver" + W
        sleep(1.5)
        os.system("cd deps && sudo tar -xvf geckodriver-v0.11.1-linux32.tar.gz && sudo mv geckodriver /usr/bin ")
        print G + "Done installing dependences!" + O
        break
    elif getos == "3":
        ubuntu_build()
        print O + "Getting GeckoDriver" + W
        sleep(1.5)
        os.system("cd deps && sudo tar -xvf geckodriver-v0.11.1-linux64.tar.gz && sudo mv geckodriver /usr/bin ")
        print G + "Done installing dependences!" + O
        break
    elif getos == "4":
        osx_build()
        break
    else:
        continue
