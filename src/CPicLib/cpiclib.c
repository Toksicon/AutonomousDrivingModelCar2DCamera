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


float contrast(rgb_color_t rgb1, rgb_color_t rgb2)
{
    // https://en.wikipedia.org/wiki/Euclidean_distance
    byte_t dr = rgb1.r - rgb2.r;
    byte_t dg = rgb1.g - rgb2.g;
    byte_t db = rgb1.b - rgb2.b;

    return ((dr * dr) + (dg * dg) + (db * db));
}

contrast_line_t line_contrast(pixel_line_t pixel_line)
{
    contrast_line_t contrast_line = create_contrast_line(pixel_line.length - 1);

    for (uint_t i = 0; i < pixel_line.length - 1; i++)
    {
        contrast_line.data[i] = contrast(pixel_line.data[i], pixel_line.data[i + 1]);
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

    // printf("\nhighest_contrast: %u, %u, %u, %u\n",
    //     highest_contrast_pixels[0],
    //     highest_contrast_pixels[1],
    //     highest_contrast_pixels[2],
    //     highest_contrast_pixels[3]
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

uint_t* resolve_mid(image_t image, uint_t samples)
{
    clock_t t1, t2;
    t1 = clock();

    uint_t* mids = malloc(sizeof(uint_t) * image.height);

    for (uint_t y = 0; y < image.height; y++)
    {
        for (uint_t x = 0; x < image.width; x++)
        {
            rgb_color_t pixel = image.data[y * image.width + x];

            // printf("(%u,\t%u,\t%u)\t", pixel.r, pixel.g, pixel.b);
        }

        pixel_line_t pxline;
        pxline.data = &(image.data[y * image.width]);
        pxline.length = image.width;

        mids[y] = resolve_row_mid(pxline);
        // printf("M: %u\n", mids[y]);
    }

    t2 = clock();
    float diff = ((float)(t2 - t1) / CLOCKS_PER_SEC);
    printf("Time: %.3fs\n", diff);

    return mids;
}

