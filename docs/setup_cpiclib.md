# CPicLib Setup

The C library for image processing (CPicLib) implements the algorithms used in C99 with the standard library. There are no dependencies to other libraries.

CMake and a C99 compiler are required to compile the library. (GCC, Clang or MinGW, no Visual Studio)

## 1) Create and enter build directory

Create and enter a build directory in the `CPicLib` (under `src/Raspberry Pi`) directory:

```bash
mkdir build
cd build
```

## 2) Generate Makefiles

Use CMake in the build directory to generate Makefiles for the desired platform:

```bash
cmake ... -G <generator-name>
```

A complete list of available generators can be found at cmake -h.
Recommendation

    Windows: cmake ... -G "MinGW Makefiles"
    *nix: cmake... -G "Unix Makefiles"

## 3) Compiling the library

Build library in the build directory:

```bash
cmake --build .
```

After that, there should be a shared library file called `cpiclib.dll` or `cpiclib.so` (depending on the platform) in the build directory.
Optional

The library can be tested with the following script:

```bash
python __init__.py
```
