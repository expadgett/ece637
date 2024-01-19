
#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

#define fheight 9
#define fwidth 9
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
  struct TIFF_img input_img, output_img;
  double red, green, blue; //initialise red, green, blue matrices for each layer of the image
 
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
  
  /* FIR LPF
    Define h[m,n]*/
  double h[fheight][fwidth];
  for (int i=0; i<fheight; i++){
    for (int j=0; j<fwidth; j++){
      h[i][j]=1.0/81;
    }
  }
  
  /* set up structure for output image */
  /* to allocate a full color image use type 'c' */
  get_TIFF ( &output_img, input_img.height, input_img.width, 'c' );

  /*filter image using h*/
  for (int i=0; i<input_img.height; i++){
    for (int j=0; j<input_img.width; j++){ //initalize red, green, blue to 0 before filteing for 0 padding to satisfy free boundary
      red=0.0;
      green=0.0;
      blue=0.0;
      for (int m=0; m<=fheight; m++){
        for (int n=0; n<=fwidth; n++){
          if (i-m<input_img.height&& i-m>=0 && j-n<input_img.width && j-n>=0){ //ie if the row/column edited in the matrix is in the image
            red+=h[m][n]*input_img.color[0][i-m][j-n]; //red is the first layer
            green+=h[m][n]*input_img.color[1][i-m][j-n]; //green is the second layer
            blue+=h[m][n]*input_img.color[2][i-m][j-n]; //blue is the third layer
          
          }   
        }
      output_img.color[0][i][j]=clipped(red);
      output_img.color[1][i][j]=clipped(green);
      output_img.color[2][i][j]=clipped(blue);
      }
    }
  }


    
  /* open color image file */
  if ( ( fp = fopen ( "lpfimage.tif", "wb" ) ) == NULL ) {
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

