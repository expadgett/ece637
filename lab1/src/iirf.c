
#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

void error(char *name);
uint8_t clipped (double pixel){ //restrict values to less than 255 and greater than 0 like in example
  uint8_t color_pixel;
  if (pixel>255){
    color_pixel=255;
  }
  else if (pixel<0){
    color_pixel=0;
  }
  else{
    color_pixel=(uint8_t)pixel; //cast to uint8_t 
  }
  return color_pixel;
}
 

int main (int argc, char **argv) 
{
  FILE *fp;
  double **red, **green, **blue;
  struct TIFF_img input_img, output_img;

  if ( argc != 2 ) error( argv[0] );

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
  if ( input_img.TIFF_type != 'c' ) {
    fprintf ( stderr, "error:  image must be 24-bit color\n" );
    exit ( 1 );
  }
  
  /* set up structure for output image */
  /* to allocate a full color image use type 'c' */
  get_TIFF ( &output_img, input_img.height, input_img.width, 'c' );
  
  red = (double **)get_img(input_img.width,input_img.height,sizeof(double));
  green = (double **)get_img(input_img.width,input_img.height,sizeof(double));
  blue = (double **)get_img(input_img.width,input_img.height,sizeof(double));
  
  /*filter image using h*/
  for (int i=0; i<input_img.height; i++){
    for (int j=0; j<input_img.width; j++){ //initalize red, green, blue to 0 before filteing for 0 padding to satisfy free boundary
      red[i][j]+=0.01*input_img.color[0][i][j];
      green[i][j]+=0.01*input_img.color[1][i][j];
      blue[i][j]+=0.01*input_img.color[2][i][j];
      if (j>0){
        red[i][j]+=0.9*red[i][j-1];
        green[i][j]+=0.9*green[i][j-1];
        blue[i][j]+=0.9*blue[i][j-1];
      }
      if (i>0){
       red[i][j]+=0.9*red[i-1][j]; 
       green[i][j]+=0.9*green[i-1][j]; 
       blue[i][j]+=0.9*blue[i-1][j]; 
      }
      if (j>0 && i>0){
      red[i][j]+=(-0.81)*(red[i-1][j-1]);
      green[i][j]+=(-0.81)*(green[i-1][j-1]);
      blue[i][j]+=(-0.81)*(blue[i-1][j-1]);
      }
      }
    }

  for (int i=0; i<input_img.height; i++){
    for (int j=0; j<input_img.width; j++){
      output_img.color[0][i][j]=clipped(red[i][j]);
      output_img.color[1][i][j]=clipped(green[i][j]);
      output_img.color[2][i][j]=clipped(blue[i][j]);
    }
  }
  
  /* open color image file */
  if ( ( fp = fopen ( "iir.tif", "wb" ) ) == NULL ) {
      fprintf ( stderr, "cannot open file color.tif\n");
      exit ( 1 );
  }
    
  /* write color image */
  if ( write_TIFF ( fp, &output_img ) ) {
      fprintf ( stderr, "error writing TIFF file %s\n", argv[2] );
      exit ( 1 );
  }
    
  /* close color image file */
  fclose ( fp );

  /* de-allocate space which was used for the images */
  free_TIFF ( &(input_img) );
  free_TIFF ( &(output_img) );

  return(0);
}

void error(char *name)
{
    printf("usage:  %s  image.tiff \n\n",name);
    printf("this program reads in a 24-bit color TIFF image.\n");
    printf("It then horizontally filters the green component, adds noise,\n");
    printf("and writes out the result as an 8-bit image\n");
    printf("with the name 'green.tiff'.\n");
    printf("It also generates an 8-bit color image,\n");
    printf("that swaps red and green components from the input image");
    exit(1);
}

