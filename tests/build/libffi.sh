#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="--host $1-linux-gnu"

DIR=$PWD/build/lib/libffi/$1
if [[ ! -d $DIR ]]; then
  git clone https://github.com/libffi/libffi.git --depth=1 --branch=v3.5.2 $DIR
  mkdir $DIR/build && cd $DIR
  ./autogen.sh
  cd $DIR/build
  ../configure --prefix=$DIR/install/ref --disable-docs --disable-shared --without-gcc-arch $ARCH_OPTS
  make -j$(nproc) CFLAGS='-static -fPIC -O3 -DNDEBUG'
  make install
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t ffi
cmake --install build/test/$1 --component ffi
