#!/bin/python3

from time import sleep
import os
import sys


def arch():
    os.system("yes | pacman -Syyu")
    sleep(2)
    os.system("yes | pacman -Scc")


def debian():
    os.system("apt update && apt dist-upgrade -y")
    sleep(2)
    os.system("apt autoclean && apt autoremove -y")
    sleep(2)
    os.system("apt purge $(dpkg -l | grep '^rc' | awk '{print $2}')")


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
    distro = ''
    if os.system("cat /etc/os-release | grep -i arch &> /dev/null") == 0:
        distro = 'arch'
    if os.system("cat /etc/os-release | egrep -iw 'debian|ubuntu|kali' &> /dev/null") == 0:
        distro = 'debian'
    if os.system("cat /etc/os-release | grep -i rhel &> /dev/null") == 0:
        distro = 'rhel'
    if os.system("cat /etc/os-release | grep -i fedora &> /dev/null") == 0:
        distro = 'fedora'
    if os.system("cat /etc/os-release | grep -i suse &> /dev/null") == 0:
        distro = 'suse'
    os.system("echo 3 > /proc/sys/vm/drop_caches")

    if distro == 'arch':
        arch()
    elif distro == 'debian':
        debian()
    elif distro == 'rhel':
        rhel()
    elif distro == 'fedora':
        fedora()
    elif distro == 'suse':
        suse()


# def clear_swap():
#     if os.system("blkid | grep swap &> /dev/null") == 0:
#         os.system("swapoff -a && swapon -a")


if __name__ == '__main__':
    # if os.geteuid() != 0:
    #     exit('''
    #         ERROR ==============
    #         ERROR Run it as root
    #         ERROR ==============
    #         ''')
    # else:
    update_distro()
    # clear_swap()
