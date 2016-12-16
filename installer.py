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
def linux_build():

    print O + "[*] Updating..." + W
    sleep(1.5)
    os.system("sudo apt-get update")
    os.system("sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev")
    os.system("sudo easy_install greenlet")
    os.system("sudo easy_install gevent")
    print O + "[*] Installing essential packages... [*]" + W
    sleep(1.5)
    os.system("sudo apt-get install python-pip python-setuptools python-selenium firefox-esr firefoxdriver")
    print O + "[*] Installing pip modules [*]" + W
    sleep(1.5)
    os.system("sudo pip install -r requirements.txt")
    print G + "[!] Done installing dependences! [!]" + O
    print "[*] Make symlinks and installation directories [*]" + W
    os.system("mkdir /opt/brut3k1t")
    os.system("cp -R src/ /opt/brut3k1t && cp brut3k1t.py  /opt/brut3k1t && cp run.sh /opt/dedsploit && cp run.sh /usr/bin/brut3k1t && chmod +x /usr/bin/brut3k1t")


# OS X / Darwin
def osx_build():
    print O + "[*] Installing Homebrew [*]" + W
    sleep(1.5)
    os.system("""/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" """)
    os.system("brew install python selenium-server-standalone")
    os.system("sudo wget https://bootstrap.pypa.io/get-pip.py")
    os.system ("sudo python get_pip.py")
    print O + "[*] Installing pip modules [*]" + W
    sleep(1.5)
    os.system("sudo pip install -r requirements.txt")
    print G + "[!] Done installing dependences! [!]" + O
    print"[*] Make symlinks and installation directories [*]"
    os.system("mkdir /opt/brut3k1t")
    os.symlink("/usr/bin/brut3k1t", "/opt/brut3k1t/brut3k1t.py")

print installer_head

while True:
    print "Select an Operating System"
    print "=============================="
    print "(1) Unix/Linux-based Distros"
    print "(2) Mac OS X / Darwin"
    print "=============================="
    getos = raw_input()
    if getos == "1":
        linux_build()
        break
    elif getos == "2":
        osx_build()
        break
    sys.exit(0)
