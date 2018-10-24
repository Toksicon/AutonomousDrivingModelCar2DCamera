#pragma once

#include <stdint.h>
#include <inttypes.h>


#ifdef WIN32
    #ifdef CPICLIB_EXPORTS
        #define CPICLIB_EXPORT __declspec(dllexport)
    #else
        #define CPICLIB_EXPORT __declspec(dllimport)
    #endif
#else
    #define CPICLIB_EXPORT
#endif


#ifndef uint_t
#define uint_t unsigned int
#endif


typedef struct
{
    uint8_t r;
    uint8_t g;
    uint8_t b;
} rgb_color_t;

typedef struct
{
    rgb_color_t* data;
    uint_t length;
} pixel_line_t;

typedef struct
{
    rgb_color_t* data;
    uint_t width;
    uint_t height;
} image_t;

typedef struct
{
    float* data;
    uint_t length;
} contrast_line_t;

extern CPICLIB_EXPORT float contrast(rgb_color_t rgb1, rgb_color_t rgb2);

extern CPICLIB_EXPORT uint_t* resolve_mid(uint8_t* image, uint_t width, uint_t height);
extern CPICLIB_EXPORT uint_t* test(uint8_t* row, uint_t width);
