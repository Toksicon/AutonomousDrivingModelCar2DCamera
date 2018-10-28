#define CPICLIB_EXPORTS
#include "filter.h"


void grayscale_filter(
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
