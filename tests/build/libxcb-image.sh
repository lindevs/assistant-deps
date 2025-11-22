#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="--host $1-linux-gnu"

DIR=$PWD/build/lib/libxcb-image/$1
if [[ ! -d $DIR ]]; then
  cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=/usr/local
  cmake --build build/test/$1 -j$(nproc) -t Xau xcb xcb-util
  cmake --install build/test/$1 --component xorgproto
  cmake --install build/test/$1 --component Xau
  cmake --install build/test/$1 --component xcb
  cmake --install build/test/$1 --component xcb-util

  git clone https://gitlab.freedesktop.org/xorg/lib/libxcb-image.git --depth=1 --branch=xcb-util-image-0.4.1 $DIR
  git clone https://gitlab.freedesktop.org/xorg/util/xcb-util-m4.git --depth=1 $DIR/m4
  rm -rf $DIR/.gitmodules
  cd $DIR && git apply $WORKDIR/tests/patch/libxcb-image/1_skip_tests.patch
  mkdir $DIR/build && cd $DIR/build
  ../autogen.sh --prefix=$DIR/install/ref $ARCH_OPTS
  make -j$(nproc) CFLAGS='-static -fPIC -O3 -DNDEBUG'
  make install
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t xcb-image
cmake --install build/test/$1 --component xcb-image
