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


////////////////////////////////////////////////////////////
// Operators


/**
 * Generic kernel operator.
 * For detailed implementations see the Sobel and Prewitt Operators.
 * 
 * @param image     Image data: (height * width) pixels * 1 (grayscale)
 * @param width     Image width
 * @param height    Image height
 * 
 * @param kernel_x  Operator x-kernel (float[9])
 * @param kernel_y  Operator y-kernel (float[9])
 * 
 * @param out       The new image with (height * width) pixels * 1 (grayscale).
 */
extern CPICLIB_EXPORT void kernel_operator(
    uint8_t* image, uint_t width, uint_t height,
    float* kernel_x, float* kernel_y,
    uint8_t* out);


/**
 * Creates an image with applied Prewitt operator to the given image.
 * 
 * @param image     Image data: (height * width) pixels * 1 (grayscale)
 * @param width     Image width
 * @param height    Image height
 * 
 * @param out       The new image with (height * width) pixels * 1 (grayscale).
 */
extern CPICLIB_EXPORT void prewitt_operator(
    uint8_t* image, uint_t width, uint_t height,
    uint8_t* out);


/**
 * Creates an image with applied Sobel operator to the given image.
 * 
 * @param image     Image data: (height * width) pixels * 1 (grayscale)
 * @param width     Image width
 * @param height    Image height
 * 
 * @param out       The new image with (height * width) pixels * 1 (grayscale).
 */
CPICLIB_EXPORT void sobel_operator(
    uint8_t* image, uint_t width, uint_t height,
    uint8_t* out);


// Operators
////////////////////////////////////////////////////////////
// Detections


/**
 * Detects mids of the road for a given count of samples.
 * 
 * @param image     Image data: (height * width) pixels * 1 (grayscale)
 * @param width     Image width
 * @param height    Image height
 * @param samples   Amount of samples to take from the image (samples < (height - 2))
 * 
 * @param out       The list of mids (y, x) of the road.
 *                  Length equals the amount of the samples.
 *                  e. g. samples = 5, len(out) == 10
 */
extern CPICLIB_EXPORT void detect_mid(uint8_t* image, uint_t width, uint_t height, uint_t samples, uint_t* out);


// Detections
////////////////////////////////////////////////////////////
// Transformations


/**
 * Creates a grayscaled image from a rgb image.
 * 
 * @param image     Image data: (height * width) pixels * 3 (RGB)
 * @param width     Image width
 * @param height    Image height
 * 
 * @param out       The new image with (height * width) pixels * 1 (grayscale).
 */
extern CPICLIB_EXPORT void rgb_to_grayscale(uint8_t* image, uint_t width, uint_t height, uint8_t* out);


// Transformations
////////////////////////////////////////////////////////////
