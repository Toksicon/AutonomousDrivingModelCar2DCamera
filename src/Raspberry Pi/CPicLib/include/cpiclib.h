#pragma once

#include <stdint.h>
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


// out size: (samples * 2)
extern CPICLIB_EXPORT void resolve_mid(uint8_t* image, uint_t width, uint_t height, uint_t samples, uint_t* out);


// out size: (height - 2) * (width - 2)
extern CPICLIB_EXPORT void sobel_operator(uint8_t* image, uint_t width, uint_t height, uint8_t* out);

// out size: width * height
// image size: width * height * 3 for RGB values
extern CPICLIB_EXPORT void rgb_to_grayscale(uint8_t* image, uint_t width, uint_t height, uint8_t* out);