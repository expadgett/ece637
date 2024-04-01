#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "area_fill.h"
#include "typeutil.h"

void addEnd(node **tail, node **new, struct pixel pixel){
    (*new)->pixel=pixel;
    (*new)->next=NULL;
    (*tail)->next=*new;
    *tail=*new;
}

void removeHead(node **head, node **new){
    *new=(*head)->next;
    free(*head);
    (*head)=*new;

}


void ConnectedNeighbors(
    struct pixel s,
    double T, 
    unsigned char **img,
    int width,
    int height,
    int *M, 
    struct pixel c[4]){
    *M=0;
    if ((s.m-1)>=0 && abs(img[s.m][s.n]-img[s.m-1][s.n])<=T){
        c[*M].m=s.m-1;
        c[*M].n=s.n;
        (*M)++;

    }
    if ((s.m+1)< height  && abs(img[s.m][s.n]-img[s.m+1][s.n])<=T){
        c[*M].m=s.m+1;
        c[*M].n=s.n;
        (*M)++;
    }
    if ((s.n-1)>=0 && abs(img[s.m][s.n]-img[s.m][s.n-1])<=T){
        c[*M].m=s.m;
        c[*M].n=s.n-1;
        (*M)++;
    }
    if ((s.n+1)<width && abs(img[s.m][s.n]-img[s.m][s.n+1])<=T){
        c[*M].m=s.m;
        c[*M].n=s.n+1;
        (*M)++;

    }
    
    }

void ConnectedSet(
    struct pixel s,
    double T,
    unsigned char **img,
    int width,
    int height,
    int ClassLabel,
    unsigned int **seg,
    int *NumConPixels) {
    int M; 
    struct node *head, *tail, *new;
    struct pixel c[4];

    (*NumConPixels)=0;

    //keep track of pixels with a linked list
    head=(struct node *)malloc(sizeof(struct node));
    head->pixel.m=s.m;
    head->pixel.n=s.n;
    head->next=NULL;
    tail = head;
    int loopcount=0;
    while (head !=NULL ){
        loopcount++;
        if (seg[head->pixel.m][head->pixel.n]!=ClassLabel){
            seg[head->pixel.m][head->pixel.n]=ClassLabel; //put s0 into the list of pixels to search through
            (*NumConPixels)++; //increase the counter for number of pixels that are connected
            ConnectedNeighbors(head->pixel, T, img, width, height, &M, c); //look for connected pixels
            for (int i=0; i<M; i++){ //iterate through the pixels that were searched
                if (seg[c[i].m][c[i].n]!=ClassLabel){ //if 
                    new=(struct node*)malloc(sizeof(struct node));
                    addEnd(&tail, &new, c[i]);
                    // next=(struct node *)malloc(sizeof(struct node));
                    // next->pixel.m=c[i].m;
                    // next->pixel.n=c[i].n;
                    // next->next=NULL;

                    // tail->next=next;
                    // tail=next;

                }
            }
        }
        removeHead(&head, &new);
        // next=head->next;
        // free(head);
        // head=next;
    }
}