#define CPICLIB_EXPORTS
#include "ridge_detection.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>


static uint_t detect_row_mid(uint8_t* row, uint_t width, uint_t mid)
{
    float threshold = 50.f;
    mid = width/2;

    uint8_t left_pixel_contrast = 0;
    uint_t left_pixel = width / 2;

    uint8_t right_pixel_contrast = 0;
    uint_t right_pixel = width / 2;

    // ignore left pixel row
    for (uint_t i = mid; i > 0; i--)
    {
        uint8_t px_contrast = row[i];

        if (px_contrast > left_pixel_contrast)
        {
            left_pixel = i;
            left_pixel_contrast = px_contrast;
        }
    }

    // ignore right pixel row
    for (uint_t i = mid; i < width - 1; i++)
    {
        uint8_t px_contrast = row[i];

        if (px_contrast > right_pixel_contrast)
        {
            right_pixel = i;
            right_pixel_contrast = px_contrast;
        }
    }

    if (((right_pixel - left_pixel) < 50)
        || (right_pixel_contrast <= threshold)
        || (left_pixel_contrast <= threshold))
    {
        // printf("! -> L: %u<%u>, R: %u<%u> \n", left_pixel, left_pixel_contrast, right_pixel, right_pixel_contrast);
        return -1;
    }

    // printf("L: %u, R: %u \n", left_pixel, right_pixel);
    return (left_pixel + (right_pixel - left_pixel) / 2);
}


void detect_mid(
    uint8_t* image, uint_t width, uint_t height,
    uint_t samples,
    uint_t* out)
{
    if (samples == 0)
    {
        fprintf(stderr, "detect_mid called without samples!\n");
        return;
    }

    float nth_sample = height / (float)samples;
    uint_t last_mid = width / 2;

    for (uint_t i = 1; i < samples; i++)
    {
        uint_t line = ((uint_t)(nth_sample * i));
        uint_t mid = detect_row_mid(image + line * width, width, last_mid);
        out[i * 2] = mid;
        out[i * 2 + 1] = line;

        if (mid >= 0)
        {
            // printf("last_mid = %u\n", mid);
            last_mid = mid;
        }
    }
}
