//Compile with:
//gcc query_renderer_demo.c -lX11 -lepoxy

#include <epoxy/gl.h>
#include <epoxy/glx.h>
#include <stdio.h>
int main() {
    unsigned int value[3]; // longest return value are 3 uints
    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_VENDOR_ID_MESA, value);
    printf("PCI ID of the device vendor:  ");
    printf("%u\n", value[0]);

    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_DEVICE_ID_MESA, value);
    printf("PCI ID of the device:  ");
    printf("%u\n", value[0]);

    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_VERSION_MESA, value);
    printf("Major, minor, and patch level of the renderer implementation:  ");
    printf("%u.%u.%u\n", value[0], value[1], value[2]);

    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_ACCELERATED_MESA, value);
    printf("Boolean indicating whether or not the renderer is hardware accelerated:  ");
    printf("%u\n", value[0]);

    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_VIDEO_MEMORY_MESA, value);
    printf("Number of megabytes of video memory available to the renderer:  ");
    printf("%u\n", value[0]);

    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_UNIFIED_MEMORY_ARCHITECTURE_MESA, value);
    printf("Boolean indicating whether or not the renderer uses a unified memory architecture or has separate \"on-card\" and GART memory.:  ");
    printf("%u\n", value[0]);

    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_PREFERRED_PROFILE_MESA, value);
    printf("Bitmask of the preferred context profile for this renderer. This value is suitable to be supplied with the GLX_CONTEXT_PROFILE_MASK_ARB attribute to glXCreateContextAttribsARB:  ");
    printf("%u\n", value[0]);

    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_OPENGL_CORE_PROFILE_VERSION_MESA, value);
    printf("Maximum core profile major and minor version supported by the renderer:  ");
    printf("%u.%u\n", value[0], value[1]);

    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_OPENGL_COMPATIBILITY_PROFILE_VERSION_MESA, value);
    printf("Maximum compatibility profile major and minor version supported by the renderer:  ");
    printf("%u.%u\n", value[0], value[1]);

    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_OPENGL_ES_PROFILE_VERSION_MESA, value);
    printf("Maximum OpenGL ES 1.x major and minor version supported by the renderer:  ");
    printf("%u.%u\n", value[0], value[1]);

    glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, GLX_RENDERER_OPENGL_ES2_PROFILE_VERSION_MESA, value);
    printf("Maximum OpenGL ES 2.x or 3.x major and minor version supported by the renderer:  ");
    printf("%u.%u\n", value[0], value[1]);

    return 0;
}
