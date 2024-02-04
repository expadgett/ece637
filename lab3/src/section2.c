
#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"
#include "area_fill.h"

void error(char *name);

int main (int argc, char **argv) 
{
  FILE *fp;
  struct TIFF_img input_img;
  unsigned int **seg;
  struct pixel s;
  double T;
  int connectedNum,  i, j;
  char image_name[100];


//   if ( argc != 4) error( argv[0] );

  /* open image file */
  if ( ( fp = fopen ( argv[1], "rb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file %s\n", argv[1] );
    exit ( 1 );
  }

  /* read image */
  if ( read_TIFF ( fp, &input_img ) ) {
    fprintf ( stderr, "error reading file %s\n", argv[1] );
    exit ( 1 );
  }

  /* close image file */
  fclose ( fp );

  /* check the type of image data */
  if ( input_img.TIFF_type != 'g' ) {
    fprintf ( stderr, "error:  image must be gray scale\n" );
    exit ( 1 );
  }

  seg = (unsigned int **)get_img(input_img.width,input_img.height,sizeof( unsigned int));
  int SegmentLabel=1;
  sscanf(argv[2], "%lf", &T);
  for (int i=0; i<input_img.height; i++){
    for (int j=0; j<input_img.width; j++){
      if(seg[i][j]==0){
        s.m=i;
        s.n=j;
        ConnectedSet(s, T, input_img.mono, input_img.width,input_img.height, SegmentLabel, seg, &connectedNum);
        if (connectedNum>100){
          SegmentLabel++;
        }
        else{
          ConnectedSet(s, T, input_img.mono, input_img.width,input_img.height,0, seg, &connectedNum);
        }
      }
    }
  }
  printf("Number of segments: %d \n", SegmentLabel-1);
  for (i=0; i<input_img.height; i++){
    for (j=0; j<input_img.width; j++){
        // printf("%d \n", seg[i][j]);
        input_img.mono[i][j]=seg[i][j];
    }
  }

  free_img( (void**)seg );

  sprintf(image_name, "segmented%f.tif",T);
  /* open output image file */
  if ( ( fp = fopen ( image_name, "wb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file output.tif\n");
    exit ( 1 );
  }

  /* write output image */
  if ( write_TIFF ( fp, &input_img) ) {
    fprintf ( stderr, "error writing TIFF file \n" );
    exit ( 1 );
  }

  /* close green image file */
  fclose ( fp );
    

  /* de-allocate space which was used for the images */
  free_TIFF ( &(input_img) );
  

  return(0);
}

