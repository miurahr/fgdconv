#!/bin/sh
set -e

export chroot="$PWD/xenial"
mkdir -p "$chroot$PWD"
sudo apt-get -qq update
sudo apt-get install -y debootstrap
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8
sudo debootstrap xenial "$chroot"
sudo mount --rbind "$PWD" "$chroot$PWD"
sudo mount --rbind /dev/pts "$chroot/dev/pts"
sudo mount --rbind /proc "$chroot/proc"
sudo su -c 'echo "deb http://archive.ubuntu.com/ubuntu xenial universe" >> xenial/etc/apt/sources.list'
sudo chroot "$chroot" locale-gen en_US.UTF-8
sudo chroot "$chroot" dpkg-reconfigure locales
sudo chroot "$chroot" apt-get update
sudo chroot "$chroot" apt-get install -y software-properties-common python-software-properties
sudo chroot "$chroot" add-apt-repository -y ppa:ubuntugis/ppa
sudo chroot "$chroot" apt-get update
sudo chroot "$chroot" apt-get install -y libxml2-dev libgdal-dev python2.7 python2.7-dev python-pip python-pip-whl python3 python3-wheel build-essential python3-pip python3.5-dev python-virtualenv python3-virtualenv
# libgdal-dev 2.1.0

