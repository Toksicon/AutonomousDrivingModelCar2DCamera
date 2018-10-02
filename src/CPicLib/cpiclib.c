#define CPICLIB_EXPORTS
#include "cpiclib.h"

#include <stdio.h>
#include <math.h>


static float normalize_color(float color)
{
    color /= 255;

    if (color <= 0.03928f)
    {
        return (color / 12.92f);
    }

    return pow((color + 0.055) / 1.055, 2.4f);
}

float luminanace(float r, float g, float b)
{
    float a[] = {
        normalize_color(r),
        normalize_color(g),
        normalize_color(b)
    };
    
    return a[0] * 0.2126f + a[1] * 0.7152f + a[2] * 0.0722f;
}

float contrast(rgb_color_t rgb1, rgb_color_t rgb2)
{
    return (luminanace(rgb1.r, rgb1.g, rgb1.b) + 0.05f) / (luminanace(rgb2.r, rgb2.g, rgb2.b) + 0.05f);
}
