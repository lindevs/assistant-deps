#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="-DCMAKE_TOOLCHAIN_FILE=$PWD/cmake/toolchain-$1.cmake -DENABLE_AVX2=OFF"
[ "$1" = aarch64 ] && ARCH_OPTS="$ARCH_OPTS -DENABLE_NEON=ON"

DIR=$PWD/build/lib/libfacedetection/$1
if [[ ! -d $DIR ]]; then
  git clone https://github.com/ShiqiYu/libfacedetection.git --depth=1 $DIR
  cd $DIR
  cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$DIR/install/ref \
    -DBUILD_SHARED_LIBS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON $ARCH_OPTS
  cmake --build build -j$(nproc)
  cmake --install build
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t facedetection
cmake --install build/test/$1 --component facedetection
