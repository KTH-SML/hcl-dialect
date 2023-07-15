# Copyright HeteroCL authors. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import pathlib
import setuptools

def recursive_iterdir(path):
    for child in path.iterdir():
        if child.is_dir():
            yield from recursive_iterdir(child)
        else:
            yield child

def collect_package_data(**kwargs):
    package_data = {}
    all = []
    for pkg, dir in kwargs.items():
        pkg_path = pkg.replace('.', '/')
        data = recursive_iterdir(pathlib.Path(f'{pkg_path}/{dir}'))
        data = map(lambda p: p.relative_to(pkg_path), data)
        data = map(str, data)
        data = filter(lambda s: s not in all, data)
        data = list(data)
        package_data[pkg] = data
        all += data
    return package_data

def setup():

    setuptools.setup(
        name="hcl_mlir",
        description="HCL-MLIR: A HeteroCL-MLIR Dialect for Heterogeneous Computing",
        version="0.1",
        author="HeteroCL",
        setup_requires=[],
        install_requires=['numpy'],
        packages=setuptools.find_namespace_packages(
            include=['hcl_mlir*'],
        ),
        include_package_data=True,
        package_data=collect_package_data(**{'hcl_mlir._mlir_libs._mlir': '.',
                                             'hcl_mlir._mlir_libs': '.'}),
        url="https://github.com/cornell-zhang/hcl-dialect",
        python_requires=">=3.6",
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Scientific/Engineering :: Accelerator Design",
            "Operating System :: OS Independent",
        ],
        zip_safe=True,
    )


if __name__ == "__main__":
    setup()
