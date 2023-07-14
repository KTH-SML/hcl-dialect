FROM alpine:3.17

ARG LLVM_VERSION="15.0.7"

WORKDIR /tmp
RUN apk add --no-cache xz wget
RUN wget "https://github.com/llvm/llvm-project/releases/download/llvmorg-$LLVM_VERSION/llvm-project-$LLVM_VERSION.src.tar.xz" && \
    tar -xf "llvm-project-$LLVM_VERSION.src.tar.xz" && \
    rm "llvm-project-$LLVM_VERSION.src.tar.xz" && \
    mv "llvm-project-$LLVM_VERSION.src" /llvm-project

WORKDIR /llvm-project/build
RUN apk add --no-cache git gcc g++ make cmake python3-dev py3-pip
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
RUN pip install build && \ 
    cmake .. \
        -DMLIR_DIR=/llvm-project/build/lib/cmake/mlir \
        -DPYTHON_BINDING=ON \
        -DOPENSCOP=OFF \
        && \
    make -j`nproc` && \
    cp -rL tools/hcl/python_packages python_packages && \
    touch python_packages/hcl_core/hcl_mlir/dialects/__init__.py && \
    touch python_packages/hcl_core/hcl_mlir/_mlir_libs/_mlir/__init__.py && \
    python3 -m build \
        --wheel \
        -o ./dist \
        python_packages/hcl_core

CMD install --mode=666 -Dt /dist ./dist/* 
