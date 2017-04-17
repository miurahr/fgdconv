#!/bin/sh
set -e

export chroot="$PWD/xenial"
mkdir -p "$chroot$PWD"
sudo apt-get -qq update
sudo apt-get install -y debootstrap
export LC_ALL=en_US
sudo debootstrap xenial "$chroot"
sudo mount --rbind "$PWD" "$chroot$PWD"
sudo mount --rbind /dev/pts "$chroot/dev/pts"
sudo mount --rbind /proc "$chroot/proc"
sudo su -c 'echo "deb http://archive.ubuntu.com/ubuntu xenial universe" >> xenial/etc/apt/sources.list'
sudo chroot "$chroot" apt-get update
sudo chroot "$chroot" apt-get install -y software-properties-common python-software-properties
sudo chroot "$chroot" add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
sudo chroot "$chroot" apt-get update
sudo chroot "$chroot" apt-get install -y libxml2-dev libgdal-dev python2.7 python2.7-dev python-pip python-pip-whl python3 python3-wheel build-essential python3-pip python3.5-dev python-virtualenv python3-virtualenv
# libgdal-dev 2.1.0
