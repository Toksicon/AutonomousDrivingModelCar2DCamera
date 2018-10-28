#pragma once
#include "export.h"


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
