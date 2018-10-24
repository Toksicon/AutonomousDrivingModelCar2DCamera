#define CPICLIB_EXPORTS
#include "cpiclib.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <time.h>


static contrast_line_t create_contrast_line(uint_t length)
{
    contrast_line_t line;
    line.data = malloc(length * sizeof(float));
    line.length = length;

    return line;
}

static void delete_contrast_line(contrast_line_t line)
{
    free(line.data);
}


float contrast(uint8_t* rgb1, uint8_t* rgb2)
{
    // https://en.wikipedia.org/wiki/Euclidean_distance
    uint8_t dr = rgb1[0] - rgb2[0];
    uint8_t dg = rgb1[1] - rgb2[1];
    uint8_t db = rgb1[2] - rgb2[2];

    return ((dr * dr) + (dg * dg) + (db * db));
}

contrast_line_t line_contrast(pixel_line_t pixel_line)
{
    contrast_line_t contrast_line = create_contrast_line(pixel_line.length - 1);

    for (uint_t i = 0; i < pixel_line.length - 1; i++)
    {
        contrast_line.data[i] = contrast(pixel_line.data + i, pixel_line.data + i + 1);
    }

    return contrast_line;
}

uint_t resolve_row_mid(pixel_line_t pixel_line)
{
    contrast_line_t contrast_line = line_contrast(pixel_line);

    // use the highest contrast values with largest distance
    const uint_t CONTRAST_PROBES = 4;
    float highest_contrasts[] = { 0.0f, 0.0f, 0.0f, 0.0f };
    uint_t highest_contrast_pixels[] = { 0, 0, 0, 0 };

    for (uint_t i = 0; i < contrast_line.length; i++)
    {
        for (uint_t j = 0; j < CONTRAST_PROBES; j++)
        {
            if (contrast_line.data[i] > highest_contrasts[j])
            {
                highest_contrasts[j] = contrast_line.data[i];
                highest_contrast_pixels[j] = i;
                break;
            }
        }
    }

    delete_contrast_line(contrast_line);

    // printf("\nhighest_contrast: %u [%f], %u [%f], %u [%f], %u [%f]\n",
    //     highest_contrast_pixels[0], highest_contrasts[0],
    //     highest_contrast_pixels[1], highest_contrasts[1],
    //     highest_contrast_pixels[2], highest_contrasts[2],
    //     highest_contrast_pixels[3], highest_contrasts[3]
    // );

    uint_t left_pixel = pixel_line.length - 1;
    uint_t right_pixel = 0;

    for (uint_t i = 0; i < CONTRAST_PROBES; i++)
    {
        if (highest_contrasts[i])
        {
            uint_t pixel = highest_contrast_pixels[i];

            if (left_pixel > pixel)
            {
                left_pixel = pixel;
            }

            if (right_pixel < pixel)
            {
                right_pixel = pixel;
            }
        }
    }

    // printf("L: %u, R: %u, ", left_pixel, right_pixel);
    return (left_pixel + (right_pixel - left_pixel) / 2);
}


uint_t* resolve_mid(uint8_t* image, uint_t width, uint_t height)
{
    clock_t t1, t2;
    t1 = clock();
    
    // printf("%u %u %u", image[0][0][0], image[0][0][1], image[0][0][2]);

    uint_t* mids = malloc(sizeof(uint_t) * height);

    for (uint_t y = 0; y < height; y++)
    {
        pixel_line_t pxline;
        pxline.data = &(image[y * width]);
        pxline.length = width;

        mids[y] = resolve_row_mid(pxline);
        // printf("M: %u\n", mids[y]);
    }

    t2 = clock();
    float diff = ((float)(t2 - t1) / CLOCKS_PER_SEC);
    printf("Time: %.3fs\n", diff);

    return mids;
}
