#!/bin/python3

from time import sleep
import os


def update():
    """Update method"""

    print('''
        =====================
        Updating has begun...
        =====================
        ''')
    os.system("zypper refresh")
    sleep(2)
    os.system("zypper update -y && zypper cc -a")
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
