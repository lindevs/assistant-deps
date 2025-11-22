#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="--host $1-linux-gnu"

DIR=$PWD/build/lib/libxcb-util/$1
if [[ ! -d $DIR ]]; then
  cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=/usr/local
  cmake --build build/test/$1 -j$(nproc) -t Xau xcb
  cmake --install build/test/$1 --component xorgproto
  cmake --install build/test/$1 --component Xau
  cmake --install build/test/$1 --component xcb

  git clone https://gitlab.freedesktop.org/xorg/lib/libxcb-util.git --depth=1 --branch=xcb-util-0.4.1 $DIR
  git clone https://gitlab.freedesktop.org/xorg/util/xcb-util-m4.git --depth=1 $DIR/m4
  rm -rf $DIR/.gitmodules
  mkdir $DIR/build && cd $DIR/build
  ../autogen.sh --prefix=$DIR/install/ref $ARCH_OPTS
  make -j$(nproc) CFLAGS='-static -fPIC -O3 -DNDEBUG'
  make install
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t xcb-util
cmake --install build/test/$1 --component xcb-util
