#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="-DCMAKE_TOOLCHAIN_FILE=$PWD/cmake/toolchain-$1.cmake"

DIR=$PWD/build/lib/zlib/$1
if [[ ! -d $DIR ]]; then
  git clone https://github.com/madler/zlib.git --depth=1 --branch=v1.3.1 $DIR
  cd $DIR
  cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$DIR/install/ref \
    -DZLIB_BUILD_EXAMPLES=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON $ARCH_OPTS
  cmake --build build -j$(nproc)
  cmake --install build
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t z
cmake --install build/test/$1 --component z
