# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: section1 section2

clean:
	/bin/rm *.o $(BIN)/*

OBJ = area_fill.o tiff.o allocate.o randlib.o qGGMRF.o solve.o 

section1: section1.o $(OBJ)
	$(CC) $(CFLAGS) -o section1 section1.o $(OBJ) -lm
	mv section1 $(BIN)

section2: section2.o $(OBJ)
	$(CC) $(CFLAGS) -o section2 section2.o $(OBJ) -lm
	mv section2 $(BIN)
