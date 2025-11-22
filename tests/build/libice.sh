#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="--host $1-linux-gnu"

DIR=$PWD/build/lib/libice/$1
if [[ ! -d $DIR ]]; then
  cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=/usr/local
  cmake --install build/test/$1 --component xorgproto
  cmake --install build/test/$1 --component xtrans

  git clone https://gitlab.freedesktop.org/xorg/lib/libice.git --depth=1 --branch=libICE-1.1.1 $DIR
  mkdir $DIR/build && cd $DIR/build
  ../autogen.sh --prefix=$DIR/install/ref $ARCH_OPTS
  make -j$(nproc) CFLAGS='-static -fPIC -O3 -DNDEBUG'
  make install
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t ICE
cmake --install build/test/$1 --component ICE
