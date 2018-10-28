#define CPICLIB_EXPORTS
#include "edge_detection.h"

#include <math.h>


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
