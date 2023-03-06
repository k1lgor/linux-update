#!/bin/bash

echo '██╗  ██╗ ██╗██╗      ██████╗  ██████╗ ██████╗ '
echo '██║ ██╔╝███║██║     ██╔════╝ ██╔═══██╗██╔══██╗'
echo '█████╔╝ ╚██║██║     ██║  ███╗██║   ██║██████╔╝'
echo '██╔═██╗  ██║██║     ██║   ██║██║   ██║██╔══██╗'
echo '██║  ██╗ ██║███████╗╚██████╔╝╚██████╔╝██║  ██║'
echo '╚═╝  ╚═╝ ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝'

if [ $EUID -ne 0 ]; then
    echo -e '\n** ERROR => Run me with sudo\n'
    exit 1
fi

DISTRO=''

checking_distro() {
    if grep -i arch /etc/os-release &>/dev/null; then
        DISTRO=arch

    elif egrep -iw 'debian|ubuntu|kali' /etc/os-release &>/dev/null; then
        DISTRO=debian

    elif grep -i rhel /etc/os-release &>/dev/null; then
        DISTRO=rhel

    elif grep -i suse /etc/os-release &>/dev/null; then
        DISTRO=suse

    elif grep -i fedora /etc/os-release &>/dev/null; then
        DISTRO=fedora

    elif grep -i slackware /etc/os-release &>/dev/null; then
        DISTRO=slackware

    elif grep -i gentoo /etc/os-release &>/dev/null; then
        DISTRO=gentoo

    elif grep -i alpine /etc/os-release &>/dev/null; then
        DISTRO=alpine

    elif grep -i void /etc/os-release &>/dev/null; then
        DISTRO=void
    fi
}

install_updates() {
    case $DISTRO in
    'arch')
        pacman -Syyu --noconfirm &&
            yay -Syyu --noconfirm &&
            pacman -Scc --noconfirm &&
            rm -rf /tmp/* &&
            rm -rf /var/tmp/* &&
            pacman -Rns $(pacman -Qtdq) --noconfirm &&
            echo 3 >/proc/sys/vm/drop_caches
        ;;
    'debian')
        apt update &&
            apt dist-upgrade -y &&
            apt autoclean &&
            apt autoremove -y
        if dpkg -s aptitude &>/dev/null; then
            apt install -y aptitude
        fi
        aptitude purge ~c -y &&
            echo 3 >/proc/sys/vm/drop_caches
        ;;
    'rhel')
        yum check-update -y &&
            yum update -y &&
            yum clean all &&
            package-cleanup --leaves --all &&
            package-cleanup --orphans &&
            yum autoremove -y &&
            echo 3 >/proc/sys/vm/drop_caches
        ;;
    'suse')
        zypper refresh &&
            zypper update -y &&
            zypper cc -a &&
            zypper packages --orphaned | awk '{print $4}' | xargs zypper remove -y &&
            echo 3 >/proc/sys/vm/drop_caches
        ;;
    'fedora')
        dnf upgrade -y &&
            dnf clean all &&
            dnf autoremove -y &&
            dnf remove $(dnf repoquery --extras --unneeded --quiet) -y &&
            echo 3 >/proc/sys/vm/drop_caches
        ;;
    'slackware')
        slackpkg update &&
            slackpkg upgrade-all &&
            slackpkg upgrade slackpkg &&
            slackpkg upgrade aaa_glibc-solibs &&
            slackpkg new-config &&
            slackpkg clean-system
        ;;
    'gentoo')
        emaint -a sync &&
            emerge -avuDN --with-bdeps=y @world &&
            emerge -av --depclean &&
            emerge --ask --depclean &&
            emerge --ask --depclean --exclude world &&
            emerge --ask --depclean --exclude world
        ;;
    'alpine')
        apk update &&
            apk upgrade -y &&
            apk cache clean &&
            apk autoremove -y &&
            apk fix --no-cache
        ;;
    'void')
        xbps-install -Su &&
            xbps-install -S &&
            xbps-remove -o &&
            xbps-remove -R old &&
            xbps-remove -C &&
            fstrim -av
        ;;
    esac
}

clear_swap() {
    if blkid | grep swap &>/dev/null; then
        swapoff -a && swapon -a
    fi
}

echo -e '\n** Start updating your distro...\n'
checking_distro
install_updates
clear_swap
echo -e '\n** Update has finished!!\n'
