#define CPICLIB_EXPORTS
#include "cpiclib.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>


////////////////////////////////////////////////////////////
// Operators


void kernel_operator(
    uint8_t* image, uint_t width, uint_t height,
    float* kernel_x, float* kernel_y,
    uint8_t* out)
{
    // apply the x and y kernel to the image
    for (uint_t y = 0; y < height; y++)
    {
        for (uint_t x = 0; x < width; x++)
        {
            uint_t offset = (y * width + x);

            if ((x == 0) || (x == (width - 1)) || (y == 0) || (y == (height - 1)))
            {   // corner pixels are black
                out[offset] = 0;
            }
            else
            {   // apply the kernels for non corner pixels

                double pixel_x = (
                      (kernel_x[0] * image[offset - width - 1])
                    + (kernel_x[1] * image[offset - width])
                    + (kernel_x[2] * image[offset - width + 1])

                    + (kernel_x[3] * image[offset - 1])
                    + (kernel_x[4] * image[offset])
                    + (kernel_x[5] * image[offset + 1])

                    + (kernel_x[6] * image[offset + width - 1])
                    + (kernel_x[7] * image[offset + width])
                    + (kernel_x[8] * image[offset + width + 1])
                );

                double pixel_y = (
                      (kernel_y[0] * image[offset - width - 1])
                    + (kernel_y[1] * image[offset - width])
                    + (kernel_y[2] * image[offset - width + 1])

                    + (kernel_y[3] * image[offset - 1])
                    + (kernel_y[4] * image[offset])
                    + (kernel_y[5] * image[offset + 1])

                    + (kernel_y[6] * image[offset + width - 1])
                    + (kernel_y[7] * image[offset + width])
                    + (kernel_y[8] * image[offset + width + 1])
                );

                // the new pixel is found by its neighbors
                out[offset] = (uint8_t)ceil(sqrt((pixel_x * pixel_x) + (pixel_y * pixel_y)));
            }
        }
    }
}


void prewitt_operator(
    uint8_t* image, uint_t width, uint_t height,
    uint8_t* out)
{
    float kernel_x[9] = {
        -1,  0,  1,
        -1,  0,  1,
        -1,  0,  1
    };

    float kernel_y[9] = {
        -1, -1, -1,
         0,  0,  0,
         1,  1,  1
    };

    kernel_operator(image, width, height, kernel_x, kernel_y, out);
}


void sobel_operator(
    uint8_t* image, uint_t width, uint_t height,
    uint8_t* out)
{
    float kernel_x[9] = {
        -1,  0,  1,
        -2,  0,  2,
        -1,  0,  1
    };

    float kernel_y[9] = {
        -1, -2, -1,
         0,  0,  0,
         1,  2,  1
    };

    kernel_operator(image, width, height, kernel_x, kernel_y, out);
}


// Operators
////////////////////////////////////////////////////////////
// Detections


static uint_t detect_row_mid(uint8_t* row, uint_t width)
{
    float threshold = 50.f;

    uint_t left_pixel = width;
    uint_t right_pixel = 0;

    for (uint_t i = 0; i < width; i++)
    {
        float px_contrast = row[i];

        if (px_contrast > threshold)
        {
            if (left_pixel > i)
            {
                left_pixel = i;
            }
            else
            {
                right_pixel = i;
            }
        }
    }

    if ((right_pixel - left_pixel) < 50)
    {
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

    for (uint_t i = 1; i < samples; i++)
    {
        uint_t line = ((uint_t)(nth_sample * i));
        out[i * 2] = line;
        out[i * 2 + 1] = detect_row_mid(image + line * width, width);
    }
}


// Detections
////////////////////////////////////////////////////////////
// Transformations


void rgb_to_grayscale(
    uint8_t* image, uint_t width, uint_t height,
    uint8_t* out)
{
    for (uint_t i = 0; i < (width * height * 3); i += 3)
    {
        // Formula to convert RGB values into grayscale
        out[i/3] = 0.35 * image[i]       //   0.35 * red
                 + 0.50 * image[i + 1]   // + 0.50 * green
                 + 0.15 * image[i + 2];  // + 0.15 * blue
    }
}


// Transformations
////////////////////////////////////////////////////////////
