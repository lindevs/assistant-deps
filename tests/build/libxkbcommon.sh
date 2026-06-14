#!/bin/bash

WORKDIR=$PWD

[ "$1" != native ] && ARCH_OPTS="--cross-file cross.txt"

DIR=$PWD/build/lib/libxkbcommon/$1
if [[ ! -d $DIR ]]; then
  cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=/usr/local
  cmake --build build/test/$1 -j$(nproc) -t Xau xcb
  cmake --install build/test/$1 --component xorgproto
  cmake --install build/test/$1 --component Xau
  cmake --install build/test/$1 --component xcb

  git clone https://github.com/xkbcommon/libxkbcommon.git --depth=1 --branch=xkbcommon-1.10.0 $DIR
  cd $DIR && git apply $WORKDIR/tests/patch/libxkbcommon/1_update_meson_config.patch
  printf "[binaries]\nc='$1-linux-gnu-gcc'\npkg-config='pkg-config'\n[host_machine]\nsystem='linux'\ncpu_family='$1'\ncpu='$1'\nendian='little'" > cross.txt
  meson setup build --buildtype=release --prefix=$DIR/install/ref \
    --default-library=static --libdir=lib --datadir=/usr/share \
    -Db_ndebug=true -Denable-xkbregistry=false -Denable-tools=false $ARCH_OPTS
  meson compile -C build -j$(nproc)
  meson install -C build --strip
fi

cd $WORKDIR
cmake --preset test-$1 -DCMAKE_INSTALL_PREFIX=$DIR/install/test \
  -DDFLT_XKB_CONFIG_EXTRA_PATH=$DIR/install/ref/etc/xkb -DXLOCALEDIR=/usr/share/X11/locale
cmake --build build/test/$1 -j$(nproc) -t xkbcommon
cmake --install build/test/$1 --component xkbcommon
