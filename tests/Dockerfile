FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y curl ca-certificates \
    && curl -sSo /etc/apt/trusted.gpg.d/kitware-key.asc https://apt.kitware.com/keys/kitware-archive-latest.asc \
    && echo "deb https://apt.kitware.com/ubuntu/ jammy main" > /etc/apt/sources.list.d/kitware.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
        git gcc g++ make ninja-build cmake python3 \
        autoconf automake pkg-config xutils-dev xtrans-dev libtool gperf bison \
        gcc-aarch64-linux-gnu libc6-dev-arm64-cross \
        gcc-riscv64-linux-gnu libc6-dev-riscv64-cross \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/bin/bash"]
