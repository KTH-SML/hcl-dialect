FROM ubuntu:22.04

ARG LLVM_VERSION="15.0.7"

RUN apt-get update && \
    apt-get install -y \
        cmake \
        g++ \
        gcc \
        git \
        make \
        python3-build \
        python3-dev \
        python3-pip \
        python3-virtualenv \
        wget \ 
        xz-utils \
        && \
    rm -r /var/lib/apt/lists/*

WORKDIR /tmp
RUN wget "https://github.com/llvm/llvm-project/releases/download/llvmorg-$LLVM_VERSION/llvm-project-$LLVM_VERSION.src.tar.xz" && \
    tar -xf "llvm-project-$LLVM_VERSION.src.tar.xz" && \
    rm "llvm-project-$LLVM_VERSION.src.tar.xz" && \
    mv "llvm-project-$LLVM_VERSION.src" /llvm-project

WORKDIR /llvm-project/build
RUN pip install -r ../mlir/python/requirements.txt && \
    cmake ../llvm \
        -DCMAKE_BUILD_TYPE=Release \
        -DLLVM_ENABLE_PROJECTS=mlir \
        -DLLVM_TARGETS_TO_BUILD=Native \
        -DLLVM_ENABLE_ASSERTIONS=ON \
        -DLLVM_INSTALL_UTILS=ON \
        -DMLIR_ENABLE_BINDINGS_PYTHON=ON \
        && \
    make -j`nproc`

WORKDIR /
COPY . /hcl-dialect

WORKDIR /hcl-dialect/build
RUN cmake .. \
        -DMLIR_DIR=/llvm-project/build/lib/cmake/mlir \
        -DPYTHON_BINDING=ON \
        -DOPENSCOP=OFF \
        && \
    make -j`nproc` && \
    cp -rL tools/hcl/python_packages . && \
    python3 -m build \
        --wheel \
        -o ./dist \
        python_packages/hcl_core

CMD install --mode=666 -Dt /dist ./dist/* 
