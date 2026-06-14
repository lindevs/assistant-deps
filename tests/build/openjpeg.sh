#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="-DCMAKE_TOOLCHAIN_FILE=$PWD/cmake/toolchain-$1.cmake"

DIR=$PWD/build/lib/openjpeg/$1
if [[ ! -d $DIR ]]; then
  git clone https://github.com/uclouvain/openjpeg.git --depth=1 --branch=v2.5.4 $DIR
  cd $DIR && git apply $WORKDIR/tests/patch/openjpeg/1_update_cmake_config.patch
  cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$DIR/install/ref \
    -DBUILD_SHARED_LIBS=OFF -DBUILD_CODEC=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON $ARCH_OPTS
  cmake --build build -j$(nproc)
  cmake --install build
  rm -rf $DIR/install/ref/lib/pkgconfig
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t openjp2
cmake --install build/test/$1 --component openjp2
