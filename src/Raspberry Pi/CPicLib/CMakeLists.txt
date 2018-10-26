cmake_minimum_required(VERSION 3.1)
project(CPicLib)

set(LIB_SOURCES src/cpiclib.c)

add_library(cpiclib SHARED ${LIB_SOURCES})
include_directories(./include)

# add_executable(cpic ${TEST_SOURCES})

set_property(TARGET cpiclib PROPERTY C_STANDARD 99)