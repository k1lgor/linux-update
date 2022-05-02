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
    os.system("apt update && apt dist-upgrade -y")
    sleep(2)
    os.system("apt autoclean && apt autoremove -y")
    sleep(2)
    # removes all leftover config files
    os.system("apt purge $(dpkg -l | grep '^rc' | awk '{print$2}')")
    sleep(2)
    os.system("echo 3 > /proc/sys/vm/drop_caches")


if __name__ == '__main__':
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
