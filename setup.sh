#!/bin/bash

libs=(all xorgproto libxau libxcb libxcb-render-util libxcb-wm libxcb-keysyms libxcb-util libxcb-image libxcb-cursor \
      libxtrans libice libsm libxdmcp libx11 zlib)

archs=(all native aarch64 riscv64)

if [[ ! $1 =~ ^(build-image|test)$ ]]; then
  echo 'Available commands: build-image, test'
  exit 1
fi

if [[ -n "$2" && ! " ${libs[*]} " =~ " $2 " ]]; then
  echo "Available libraries: ${libs[*]}"
  exit 1
fi

if [[ -n "$3" && ! " ${archs[*]} " =~ " $3 " ]]; then
  echo "Available architectures: ${archs[*]}"
  exit 1
fi

if [[ $1 == build-image ]]; then
  docker build -t lindevs-assistant-deps tests

  exit 0
fi

if [[ $1 == test ]]; then
  for lib in "${libs[@]}"; do
    [[ ($2 != all && $lib != $2) || $lib == all ]] && continue
    for arch in "${archs[@]}"; do
      [[ ($3 != all && $arch != $3) || $arch == all ]] && continue
      docker run -it --rm -v ./:/app lindevs-assistant-deps -c "python3 tests/test.py $lib $arch"
    done
  done
  sudo chown -R $USER:$USER build

  exit 0
fi
