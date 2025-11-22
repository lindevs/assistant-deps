#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="--host $1-linux-gnu"

DIR=$PWD/build/lib/libxtrans/$1
if [[ ! -d $DIR ]]; then
  git clone https://gitlab.freedesktop.org/xorg/lib/libxtrans.git --depth=1 --branch=xtrans-1.4.0 $DIR
  mkdir $DIR/build && cd $DIR/build
  ../autogen.sh --prefix=$DIR/install/ref $ARCH_OPTS
  make install
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --install build/test/$1 --component xtrans
