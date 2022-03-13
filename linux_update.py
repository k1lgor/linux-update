#!/bin/python3

from time import sleep
import os
import sys


def arch():
    os.system("yes | pacman -Syyu")
    sleep(2)
    os.system("yes | pacman -Scc")


def debian():
    os.system("app update && apt dist-upgrade -y")
    sleep(2)
    os.system("apt autoclean && apt autoremove -y")
    sleep(2)
    if os.system("dpkg -s aptitude &>/dev/null") != 0:
        os.system("apt install -y aptitude")
    os.system("apt aptitude purge ~c -y")


def rhel():
    os.system("yum check-update -y")
    sleep(2)
    os.system("yum clean all && yum update -y")


def fedora():
    os.system("dnf upgrade -y && dnf clean all")


def suse():
    os.system("zypper refresh && zypper update -y")
    sleep(2)
    os.system("zypper cc -a")


def update_distro():
    if os.system("cat /etc/os-release | grep -i arch &> /dev/null") == 0:
        arch()
    elif os.system("cat /etc/os-release | egrep -iw 'debian|ubuntu|kali' &> /dev/null") == 0:
        debian()
    elif os.system("cat /etc/os-release | grep -i rhel &> /dev/null") == 0:
        rhel()
    elif os.system("cat /etc/os-release | grep -i fedora &> /dev/null") == 0:
        fedora()
    elif os.system("cat /etc/os-release | grep -i suse &> /dev/null") == 0:
        suse()
    os.system("echo 3 > /proc/sys/vm/drop_caches")


# def clear_swap():
#     if os.system("blkid | grep swap &> /dev/null") == 0:
#         os.system("swapoff -a && swapon -a")


if __name__ == '__main__':
    if os.geteuid() != 0:
        exit('''
            ERROR ==============
            ERROR Run it as root
            ERROR ==============
            ''')
    else:
        update_distro()
        # clear_swap()
