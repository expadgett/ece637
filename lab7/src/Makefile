# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: soln2 

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o randlib.o qGGMRF.o solve.o 

soln2: soln2.o $(OBJ)
	$(CC) $(CFLAGS) -o soln2 soln2.o $(OBJ) -lm
	mv soln2 $(BIN)
