#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="--host $1-linux-gnu"

DIR=$PWD/build/lib/libxcb/$1
if [[ ! -d $DIR ]]; then
  cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=/usr/local
  cmake --build build/test/$1 -j$(nproc) -t Xau
  cmake --install build/test/$1 --component xorgproto
  cmake --install build/test/$1 --component Xau

  git clone https://gitlab.freedesktop.org/xorg/proto/xcbproto.git --depth=1 /tmp/xcbproto
  (cd /tmp/xcbproto && ./autogen.sh --prefix=/usr/local $ARCH_OPTS && make install)

  git clone https://gitlab.freedesktop.org/xorg/lib/libxcb.git --depth=1 --branch=libxcb-1.17.0 $DIR
  mkdir $DIR/build && cd $DIR/build
  ../autogen.sh --prefix=$DIR/install/ref $ARCH_OPTS
  make -j$(nproc) CFLAGS='-static -fPIC -O3 -DNDEBUG'
  make install
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t xcb
cmake --install build/test/$1 --component xcb
