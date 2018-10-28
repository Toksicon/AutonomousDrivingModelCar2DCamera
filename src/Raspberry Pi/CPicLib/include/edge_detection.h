#pragma once
#include "export.h"

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
extern CPICLIB_EXPORT void sobel_operator(
    uint8_t* image, uint_t width, uint_t height,
    uint8_t* out);


/**
 * Creates an image with applied Canny Edge Detector to the given image.
 * 
 * @param image     Image data: (height * width) pixels * 1 (grayscale)
 * @param width     Image width
 * @param height    Image height
 * 
 * @param out       The new image with (height * width) pixels * 1 (grayscale).
 */
extern CPICLIB_EXPORT void canny_edge_detection(
    uint8_t* in, uint_t width, uint_t height,
    const int tmin, const int tmax,
    const float sigma,
    uint8_t* out);
