struct pixel {
    int m,n; /* m=row, n=col */
};

typedef struct node {
    struct pixel pixel;
    struct node *next;
}node ;

void ConnectedNeighbors(
    struct pixel s,
    double T,
    unsigned char **img,
    int width,
    int height,
    int *M,
    struct pixel c[4]); 

void ConnectedSet(
    struct pixel s,
    double T,
    unsigned char **img,
    int width,
    int height,
    int ClassLabel,
    unsigned int **seg,
    int *NumConPixels);
