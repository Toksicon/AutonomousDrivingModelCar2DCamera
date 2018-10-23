#pragma once


#ifdef WIN32
    #ifdef CPICLIB_EXPORTS
        #define CPICLIB_EXPORT __declspec(dllexport)
    #else
        #define CPICLIB_EXPORT __declspec(dllimport)
    #endif
#else
    #define CPICLIB_EXPORT
#endif


typedef unsigned char byte_t;

#ifndef uint_t
#define uint_t unsigned int
#endif

#ifndef true
#define true 1
#endif

#ifndef false
#define false 0
#endif

#ifndef bool_t
#define bool_t byte_t
#endif


typedef struct
{
    byte_t r;
    byte_t g;
    byte_t b;
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
extern CPICLIB_EXPORT uint_t* resolve_mid(image_t image, uint_t samples);
