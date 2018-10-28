#pragma once
#include <stdio.h>
#include <stdlib.h>

#include <stdint.h>
#include <stdbool.h>
#include <inttypes.h>

#ifdef WIN32
    #ifdef CPICLIB_EXPORTS
        #define CPICLIB_EXPORT __declspec(dllexport)
    #else
        #define CPICLIB_EXPORT __declspec(dllimport)
    #endif
#else
    #define CPICLIB_EXPORT
#endif


#ifndef uint_t
#define uint_t unsigned int
#endif
