cmake_minimum_required(VERSION 3.1)
project(CPicLib)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(LIB_SOURCES
    # filter
    src/filter/convolution.c
    src/filter/gaussian.c
    src/filter/grayscale.c

    # edge detection
    src/edge_detection/canny_edge_detection.c
    src/edge_detection/kernel_operator.c
    src/edge_detection/prewitt_operator.c
    src/edge_detection/sobel_operator.c

    # ridge detection
    src/ridge_detection/detect_mid.c
)

add_library(cpiclib SHARED ${LIB_SOURCES})
include_directories(./include)

# add_executable(cpic ${TEST_SOURCES})

set_property(TARGET cpiclib PROPERTY C_STANDARD 99)

if(CMAKE_BUILD_TYPE STREQUAL Release)
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif()