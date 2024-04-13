#include <math.h>
#include <string.h>
#include "tiff.h"
#include "allocate.h"
#include "medfilt.h"

unsigned int** medfilt(struct TIFF_img input_img){
    unsigned int ** a=(unsigned int**)get_img(input_img.width, input_img.height, sizeof(unsigned int));
    for (int i=2; i<input_img.height-2; i++){
        for (int j=2; j<input_img.width-2; j++){
            a[i][j]=filt(input_img, i, j);
        }
    }
    return a;
}

unsigned int filt(struct TIFF_img input, int i, int j){
    unsigned int s1, s2, tmp_val, y_out[25];
    unsigned int weight[25]={1, 1, 1, 1, 1, \
                             1, 2, 2, 2, 1, \
                             1, 2, 2, 2, 1, \
                             1, 1, 1, 1, 1};
    int idx=0;
    for (int m=i-2; m<i+3; m++){
        for (int n=j-2; n<j+3; n++){
            y_out[idx]=input.mono[m][n];
            idx++;
        }  
    }

    for (int m=0; m<25; m++){
        for (int n=m+1; n<25; n++){
            if (y_out[m]<y_out[n]){ //if previous is greater then move it after
                //shift through image
                tmp_val=y_out[m];
                y_out[m]=y_out[n];
                y_out[n]=tmp_val;
                //shift through weights
                tmp_val=weight[m];
                weight[m]=weight[n];
                weight[n]=tmp_val;
            }
        }
    }
    s1=weight[0];
    int tot=0;
    for (int i=0; i<25; i++){
        tot+=weight[i];
    }
    s2=tot-s1;
    int k;
    for (k=0; k<25; k++){
        if (s1>s2){
            return y_out[k];
        }
        s1+=weight[k+1];
        s2-=weight[k+1];
    }

    return y_out[k];

}