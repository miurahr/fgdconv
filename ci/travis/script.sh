#!/bin/sh
set -e
export chroot="$PWD"/xenial
export LC_ALL=en_US

sudo chroot "$chroot" sh -c "cd $PWD && tox"
