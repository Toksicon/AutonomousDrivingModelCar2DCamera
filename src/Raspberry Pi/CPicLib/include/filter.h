#pragma once
#include "export.h"

#define MAX_BRIGHTNESS 255

// C99 doesn't define M_PI (GNU-C99 does)
#ifndef M_PI
#define M_PI 3.14159265358979323846264338327
#endif


extern CPICLIB_EXPORT void convolution(
    const uint8_t* in, uint8_t* out, const float* kernel,
    const int nx, const int ny, const int kn,
    const bool normalize);


extern CPICLIB_EXPORT void gaussian_filter(
    const uint8_t* in, uint8_t* out,
    const int nx, const int ny,
    const float sigma);


/**
 * Creates a grayscaled image from a rgb image.
 * 
 * @param image     Image data: (height * width) pixels * 3 (RGB)
 * @param width     Image width
 * @param height    Image height
 * 
 * @param out       The new image with (height * width) pixels * 1 (grayscale).
 */
extern CPICLIB_EXPORT void grayscale_filter(
    uint8_t* in, uint_t width, uint_t height,
    uint8_t* out);