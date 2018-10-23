cmake_minimum_required(VERSION 3.10)
project(CPicLib)

set(LIB_SOURCES cpiclib.c)

add_library(cpiclib SHARED ${LIB_SOURCES})
include_directories(./include)

# add_executable(cpic ${TEST_SOURCES})
