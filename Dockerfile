FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    git \
    zip \
    unzip \
    pkg-config \
    build-essential \
    cmake \
    ninja-build \
    clang-format \
    cppcheck \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-tk \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | BINDIR=/usr/local/bin sh
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

RUN git config --global --add safe.directory /project

ENV PATH="/usr/local/bin:/root/.local/bin:$PATH"

WORKDIR /project

