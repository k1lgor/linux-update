#!/bin/python3

from time import sleep
import os
import sys


def check_distro(distro):
    print('Checking up your distro...')
    if os.system("cat /etc/os-release | grep -i arch &> /dev/null") == 0:
        distro = 'arch'
    elif os.system("cat /etc/os-release | egrep -iw 'debian|ubuntu|kali' &> /dev/null") == 0:
        distro = 'debian'
    elif os.system("cat /etc/os-release | grep -i rhel &> /dev/null") == 0:
        distro = 'rhel'
    elif os.system("cat /etc/os-release | grep -i fedora &> /dev/null") == 0:
        distro = 'fedora'
    elif os.system("cat /etc/os-release | grep -i suse &> /dev/null") == 0:
        distro = 'suse'
    return distro


def update_distro():
    print('Updating your distro...')
    if distro == 'arch':
        os.system("yes | pacman -Syyu")
        sleep(2)
        os.system("yes | pacman -Scc")
    elif distro == 'debian':
        os.system("app update && apt dist-upgrade -y")
        sleep(2)
        os.system("apt autoclean && apt autoremove -y")
        sleep(2)
        if os.system("dpkg -s aptitude &>/dev/null") != 0:
            os.system("apt install -y aptitude")
        os.system("apt aptitude purge ~c -y")
    elif distro == 'rhel':
        os.system("yum check-update -y")
        sleep(2)
        os.system("yum clean all && yum update -y")
    elif distro == 'suse':
        os.system("zypper refresh && zypper update -y")
        sleep(2)
        os.system("zypper cc -a")
    elif distro == 'fedora':
        os.system("dnf upgrade -y && dnf clean all")
    os.system("echo 3 > /proc/sys/vm/drop_caches")


# def clear_swap():
#     if os.system("blkid | grep swap &> /dev/null") == 0:
#         os.system("swapoff -a && swapon -a")


if __name__ == '__main__':
    distro = ''
    if os.geteuid() != 0:
        exit('''
            ERROR ==============
            ERROR Run it as root
            ERROR ==============
            ''')
    else:
        check_distro(distro)
        update_distro(distro)
        # clear_swap()
