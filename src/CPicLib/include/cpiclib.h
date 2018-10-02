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


typedef struct
{
    float r;
    float g;
    float b;
} rgb_color_t;

extern CPICLIB_EXPORTS float luminanace(float r, float g, float b);
extern CPICLIB_EXPORTS float contrast(rgb_color_t rgb1, rgb_color_t rgb2);
