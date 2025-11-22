#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="-DCMAKE_TOOLCHAIN_FILE=$PWD/cmake/toolchain-$1.cmake"

DIR=$PWD/build/lib/libpng/$1
if [[ ! -d $DIR ]]; then
  cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=/usr/local
  cmake --build build/test/$1 -j$(nproc) -t z
  cmake --install build/test/$1 --component z

  git clone https://github.com/pnggroup/libpng.git --depth=1 --branch=v1.6.50 $DIR
  cd $DIR
  cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$DIR/install/ref \
    -DPNG_SHARED=OFF -DPNG_TESTS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON $ARCH_OPTS
  cmake --build build -j$(nproc)
  cmake --install build
  rm -rf $DIR/install/ref/include/libpng16 $DIR/install/ref/lib/pkgconfig
  mv $DIR/install/ref/lib/libpng16.a $DIR/install/ref/lib/libpng.a
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t png
cmake --install build/test/$1 --component png
