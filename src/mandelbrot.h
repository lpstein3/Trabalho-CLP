#ifndef MANDELBROT_H
#define MANDELBROT_H

#ifdef __cplusplus
extern "C" {
#endif

void compute_mandelbrot(int width, int height,
                        double centerX, double centerY,
                        double zoom, int maxIter,
                        unsigned char* output);

#ifdef __cplusplus
}
#endif

#endif