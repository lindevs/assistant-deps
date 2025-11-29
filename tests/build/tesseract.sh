#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="-DCMAKE_TOOLCHAIN_FILE=$PWD/cmake/toolchain-$1.cmake"

echo "$ARCH_OPTS"

DIR=$PWD/build/lib/tesseract/$1
if [[ ! -d $DIR ]]; then
  cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=/usr/local
  cmake --build build/test/$1 -j$(nproc) -t leptonica
  cmake --install build/test/$1 --component leptonica

  git clone https://github.com/tesseract-ocr/tesseract.git --depth=1 --branch=5.5.1 $DIR
  cd $DIR && git apply $WORKDIR/tests/patch/tesseract/1_update_cmake_config.patch \
          && git apply $WORKDIR/tests/patch/tesseract/2_no_file_macro.patch
  cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$DIR/install/ref \
    -DBUILD_SHARED_LIBS=OFF -DBUILD_TRAINING_TOOLS=OFF -DDISABLE_TIFF=ON -DLEPT_TIFF_RESULT=OFF \
    -DDISABLE_ARCHIVE=ON -DDISABLE_CURL=ON -DCMAKE_POSITION_INDEPENDENT_CODE=ON $ARCH_OPTS
  cmake --build build -j$(nproc)
  cmake --install build
  rm -rf $DIR/install/ref/lib/pkgconfig
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test
cmake --build build/test/$1 -j$(nproc) -t tesseract
cmake --install build/test/$1 --component tesseract
