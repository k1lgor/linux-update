#!/bin/python3

from time import sleep
import os

from pip import main


def update():
    """Update method"""

    print('''
        =====================
        Updating has begun...
        =====================
        ''')
    os.system("yum check-update -y")
    sleep(2)
    os.system("yum clean all && yum update -y")
    sleep(2)
    os.system("echo 3 > /proc/sys/vm/drop_caches")


def main():
    """Checks if you run it as sudo or not"""
    if os.geteuid() != 0:
        exit('''
            ERROR ==============
            ERROR Run it as root
            ERROR ==============
            ''')
    else:
        update()
        print('''
            ========================
            Updating has finished...
            ========================
            ''')


if __name__ == '__main__':
    main()
