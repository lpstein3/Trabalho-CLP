#include "mandelbrot.h"
#include <math.h>

// Mapeia iteração para cor RGB com um gradiente que realça as "chamas"
static void color_map(int iter, int maxIter, unsigned char* r, unsigned char* g, unsigned char* b) {
    if (iter == maxIter) {
        *r = *g = *b = 0; // preto para dentro do conjunto
        return;
    }
    double t = (double)iter / maxIter;
    // Gradiente personalizado para dar um aspecto de fogo
    *r = (unsigned char)(9 * (1 - t) * t * t * t * 255);
    *g = (unsigned char)(15 * (1 - t) * (1 - t) * t * t * 255);
    *b = (unsigned char)(8.5 * (1 - t) * (1 - t) * (1 - t) * t * 255);
}

/**
 * Função exportada para o Python.
 * Calcula o fractal Burning Ship para a região especificada.
 */
void compute_mandelbrot(int width, int height,
                        double centerX, double centerY,
                        double zoom, int maxIter,
                        unsigned char* output) {
    // Define a região do plano complexo baseada no centro e zoom
    double xmin = centerX - 1.5 / zoom;
    double xmax = centerX + 1.5 / zoom;
    double ymin = centerY - 1.5 / zoom;
    double ymax = centerY + 1.5 / zoom;

    double stepX = (xmax - xmin) / width;
    double stepY = (ymax - ymin) / height;

    for (int py = 0; py < height; py++) {
        double cy = ymin + py * stepY;
        for (int px = 0; px < width; px++) {
            double cx = xmin + px * stepX;

            // Inicializa z = 0 + 0i
            double zx = 0.0, zy = 0.0;
            int iter = 0;

            // Burning Ship: aplica valor absoluto a zx e zy a cada iteração
            while (iter < maxIter && (zx*zx + zy*zy) < 4.0) {
                double tmp_zx = fabs(zx);
                double tmp_zy = fabs(zy);
                double tmp = tmp_zx * tmp_zx - tmp_zy * tmp_zy + cx;
                zy = 2.0 * tmp_zx * tmp_zy + cy;
                zx = tmp;
                iter++;
            }

            unsigned char r, g, b;
            color_map(iter, maxIter, &r, &g, &b);

            int idx = (py * width + px) * 3;
            output[idx] = r;
            output[idx+1] = g;
            output[idx+2] = b;
        }
    }
}