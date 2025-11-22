#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="--host $1-linux-gnu --enable-malloc0returnsnull"

DIR=$PWD/build/lib/libx11/$1
if [[ ! -d $DIR ]]; then
  cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=/usr/local
  cmake --build build/test/$1 -j$(nproc) -t Xau xcb
  cmake --install build/test/$1 --component xorgproto
  cmake --install build/test/$1 --component Xau
  cmake --install build/test/$1 --component xcb

  git clone https://gitlab.freedesktop.org/xorg/lib/libx11.git --depth=1 --branch=libX11-1.8.9 $DIR
  mkdir $DIR/build && cd $DIR/build
  ../autogen.sh --prefix=$DIR/install/ref $ARCH_OPTS
  make -j$(nproc) CFLAGS='-static -fPIC -O3 -DNDEBUG'
  make install
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test \
  -DXCMSDIR=$DIR/install/ref/share/X11 \
  -DXERRORDB=$DIR/install/ref/share/X11/XErrorDB \
  -DXKEYSYMDB=$DIR/install/ref/share/X11/XKeysymDB \
  -DXLOCALEDIR=$DIR/install/ref/share/X11/locale \
  -DXLOCALELIBDIR=$DIR/install/ref/lib/X11/locale
cmake --build build/test/$1 -j$(nproc) -t X11
cmake --install build/test/$1 --component X11
