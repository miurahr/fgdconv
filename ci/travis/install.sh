#!/bin/sh
set -e
export chroot="$PWD"/xenial
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8

sudo -H chroot "$chroot" sh -c "cd $PWD && pip install --upgrade pip"
sudo -H chroot "$chroot" sh -c "cd $PWD && pip install tox"
sudo -H chroot "$chroot" sh -c "cd $PWD && pip install coveralls"
