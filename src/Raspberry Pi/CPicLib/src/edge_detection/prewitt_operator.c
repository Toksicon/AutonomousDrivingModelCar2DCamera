#define CPICLIB_EXPORTS
#include "edge_detection.h"


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
