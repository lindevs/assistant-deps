#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="-DCMAKE_TOOLCHAIN_FILE=$PWD/cmake/toolchain-$1.cmake"

DIR=$PWD/build/lib/libwebp/$1
if [[ ! -d $DIR ]]; then
  git clone https://github.com/webmproject/libwebp.git --depth=1 --branch=v1.6.0 $DIR
  cd $DIR
  cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$DIR/install/ref \
    -DWEBP_BUILD_CWEBP=OFF -DWEBP_BUILD_DWEBP=OFF -DWEBP_BUILD_GIF2WEBP=OFF -DWEBP_BUILD_IMG2WEBP=OFF \
    -DWEBP_BUILD_VWEBP=OFF -DWEBP_BUILD_WEBPINFO=OFF -DWEBP_BUILD_WEBPMUX=OFF -DWEBP_BUILD_EXTRAS=OFF $ARCH_OPTS
  cmake --build build -j$(nproc)
  cmake --install build
  rm -rf $DIR/install/ref/lib/pkgconfig
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t webp
cmake --install build/test/$1 --component webp
