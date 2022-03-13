#!/bin/bash

echo '██╗  ██╗ ██╗██╗      ██████╗  ██████╗ ██████╗ '
echo '██║ ██╔╝███║██║     ██╔════╝ ██╔═══██╗██╔══██╗'
echo '█████╔╝ ╚██║██║     ██║  ███╗██║   ██║██████╔╝'
echo '██╔═██╗  ██║██║     ██║   ██║██║   ██║██╔══██╗'
echo '██║  ██╗ ██║███████╗╚██████╔╝╚██████╔╝██║  ██║'
echo '╚═╝  ╚═╝ ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝'

if [ $EUID -ne 0 ]; then
	echo 'ERROR ==================='
	echo '====>    Run it as root'
	echo 'ERROR ==================='
	exit 1
fi

DISTRO=''

checking_distro() {
	grep -i arch /etc/os-release &>/dev/null
	if [ $? -eq 0 ]; then
		DISTRO=arch
	fi

	egrep -iw 'debian|ubuntu|kali' /etc/os-release &>/dev/null
	if [ $? -eq 0 ]; then
		DISTRO=debian
	fi

	grep -i rhel /etc/os-release &>/dev/null
	if [ $? -eq 0 ]; then
		DISTRO=rhel
	fi

	grep -i suse /etc/os-release &>/dev/null
	if [ $? -eq 0 ]; then
		DISTRO=suse
	fi

	grep -i fedora /etc/os-release &>/dev/null
	if [ $? -eq 0 ]; then
		DISTRO=fedora
	fi

	grep -i slackware /etc/os-release &>/dev/null
	if [ $? -eq 0 ]; then
		DISTRO=slackware
	fi

	grep -i gentoo /etc/os-release &>/dev/null
	if [ $? -eq 0 ]; then
		DISTRO=gentoo
	fi
}

install_updates() {
	echo '************************'
	echo 'Updating linux...'
	echo '************************'
	case $DISTRO in
	'arch')
		yes | pacman -Syyu
		yes | pacman -Scc
		echo 3 >/proc/sys/vm/drop_caches
		;;
	'debian')
		apt update
		apt dist-upgrade -y
		apt autoclean
		apt autoremove -y
		dpkg -s aptitude &>/dev/null
		if [ $? -ne 0 ]; then
			sudo apt install -y aptitude
		fi
		aptitude purge ~c -y
		echo 3 >/proc/sys/vm/drop_caches
		;;
	'rhel')
		yum check-update -y
		yum clean all
		yum update -y
		echo 3 >/proc/sys/vm/drop_caches
		;;
	'suse')
		zypper refresh
		zypper update -y
		zypper cc -a
		echo 3 >/proc/sys/vm/drop_caches
		;;
	'fedora')
		dnf upgrade -y
		dnf clean all
		;;
		# 'slackware')
		# 	slackpkg update
		# 	slackpkg upgrade slackpkg
		# 	slackpkg new-config
		# 	slackpkg upgrade aaa_glibc-solibs
		# 	slackpkg install-new
		# 	slackpkg upgrade-all
		# 	slackpkg clean-system
		# 	;;
		# 'gentoo')
		# 	emaint -a sync
		# 	emerge --ask --verbose --update --deep --newuse @world
		# 	emerge --depclean --ask --verbose
		# 	;;
	esac
}

clear_swap() {
	sudo blkid | grep swap &>/dev/null
	if [ $? -eq 0 ]; then
		swapoff -a && swapon -a
	fi
}

checking_distro
install_updates
clear_swap
