#define CPICLIB_EXPORTS
#include "cpiclib.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>


uint_t resolve_row_mid(uint8_t* row, uint_t width)
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


void sobel_operator(uint8_t* image, uint_t width, uint_t height, uint8_t* out)
{
    float sobel_x[3][3] = {
        {-1,  0,  1},
        {-2,  0,  2},
        {-1,  0,  1}
    };

    float sobel_y[3][3] = {
        {-1, -2, -1},
        { 0,  0,  0},
        { 1,  2,  1}
    };

    for (uint_t x = 1; x < width - 1; x++)
    {
        for (uint_t y = 1; y < height - 1; y++)
        {
            double pixel_x = (
                  (sobel_x[0][0] * image[((y - 1) * width + (x - 1))])
                + (sobel_x[0][1] * image[((y - 1) * width +    x   )])
                + (sobel_x[0][2] * image[((y - 1) * width + (x + 1))])

                + (sobel_x[1][0] * image[(y * width + (x - 1))])
                + (sobel_x[1][1] * image[(y * width +    x   )])
                + (sobel_x[1][2] * image[(y * width + (x + 1))])

                + (sobel_x[2][0] * image[((y + 1) * width + (x - 1))])
                + (sobel_x[2][1] * image[((y + 1) * width +    x   )])
                + (sobel_x[2][2] * image[((y + 1) * width + (x + 1))])
            );

            double pixel_y = (
                  (sobel_y[0][0] * image[((y - 1) * width + (x - 1))])
                + (sobel_y[0][1] * image[((y - 1) * width +    x   )])
                + (sobel_y[0][2] * image[((y - 1) * width + (x + 1))])

                + (sobel_y[1][0] * image[(y * width + (x - 1))])
                + (sobel_y[1][1] * image[(y * width +    x   )])
                + (sobel_y[1][2] * image[(y * width + (x + 1))])

                + (sobel_y[2][0] * image[((y + 1) * width + (x - 1))])
                + (sobel_y[2][1] * image[((y + 1) * width +    x   )])
                + (sobel_y[2][2] * image[((y + 1) * width + (x + 1))])
            );

            uint8_t val = (uint8_t)ceil(sqrt((pixel_x * pixel_x) + (pixel_y * pixel_y)));

            out[(y - 1) * (width - 2) + (x - 1)] = val;
        }
    }
}


void resolve_mid(uint8_t* image, uint_t width, uint_t height, uint_t samples, uint_t* out)
{
    if (samples < 2) {
        fprintf(stderr, "At least 2 samples required!");
        return;
    }

    uint_t* mids = malloc(sizeof(uint_t) * height);
    float nth_sample = height / (float)samples;

    // always resolve first and last line
    out[0] = 0;
    out[1] = resolve_row_mid(image, width);
    out[samples - 2] = height;
    out[samples - 1] = resolve_row_mid(image + (height - 1) * width, width);

    for (uint_t i = 1; i < samples; i++)
    {
        uint_t line = ((uint_t)(nth_sample * i));
        out[i * 2] = line;
        out[i * 2 + 1] = resolve_row_mid(image + line * width, width);
    }
    
}
