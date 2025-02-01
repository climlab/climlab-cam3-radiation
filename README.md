# climlab-cam3-radiation

[![Build and test](https://github.com/climlab/climlab-cam3-radiation/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/climlab/climlab-cam3-radiation/actions/workflows/build-and-test.yml)

Brian Rose, University at Albany

## About

This is a stand-alone Python wrapper for the NCAR CAM3 radiation scheme.

The primary use-case is to serve as the under-the-hood radiation driver
for [climlab](https://climlab.readthedocs.io/), but it can be used as a
stand-alone model if you are familiar with the Fortran source code.
This is a lightweight wrapper that emulates the Fortran interface as closely as possible.

## Installation

Pre-built binaries for many platforms are available from [conda-forge](https://conda-forge.org).

To install in the current environment:
```
conda install climlab-cam3-radiation --channel conda-forge
```
or create a self-contained environment:
```
conda create --name my_env python=3.12 climlab-cam3-radiation --channel conda-forge
conda activate my_env
```

See below for instructions on how to build from source.

## Example usage

You can import the Fortran driver into a Python session with
```
import climlab_cam3_radiation as cam3
```

Please see the directory `climlab_cam3_radiation/tests/` directory in this repository
for working examples that set up all the necessary input arrays and call the driver.

## Building from source

Here are instructions to create a build environment (including Fortran compiler)
with conda and build using f2py.

To build:
```
conda env create --file ./ci/requirements-macos-arm64.yml
conda activate cam3_build_env
python -m pip install . --no-deps -vv
```

To run tests, do this from any directory other than the climlab-cam3-radiation repo:
```
pytest -v --pyargs climlab_cam3_radiation
```

## Version history

- Version 0.3.1 (February 2025) modernizes the build system for this package can run on Python 3.12 and above. The build now uses [meson](https://mesonbuild.com/). This version also uses gridpoint-specific values of the input parameter `eccf` (solar irradiance factor), consistent with recent changes in climlab-rrtmg.
- Version 0.2 is the first public release (April 2022).
The Python wrapper code has been extracted from
[climlab v0.7.13](https://github.com/brian-rose/climlab/releases/tag/v0.7.13).
