#ifndef _MEDFILT_H_
#define _MEDFILT_H_
void error(char*name);
unsigned int filt(struct TIFF_img input, int i, int j);
unsigned int** medfilt(struct TIFF_img input_img);
#endif