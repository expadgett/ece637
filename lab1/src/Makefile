# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: ImageReadWriteExample SurrogateFunctionExample SolveExample firlpf firsf iirf

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o randlib.o qGGMRF.o solve.o

ImageReadWriteExample: ImageReadWriteExample.o $(OBJ) 
	$(CC) $(CFLAGS) -o ImageReadWriteExample ImageReadWriteExample.o $(OBJ) -lm
	mv ImageReadWriteExample $(BIN)

SurrogateFunctionExample: SurrogateFunctionExample.o $(OBJ) 
	$(CC) $(CFLAGS) -o SurrogateFunctionExample SurrogateFunctionExample.o $(OBJ) -lm
	mv SurrogateFunctionExample $(BIN)

SolveExample: SolveExample.o $(OBJ) 
	$(CC) $(CFLAGS) -o SolveExample SolveExample.o $(OBJ) -lm
	mv SolveExample $(BIN)

firlpf: firlpf.o $(OBJ)
	$(CC) $(CFLAGS) -o firlpf firlpf.o $(OBJ) -lm
	mv firlpf $(BIN)
    
firsf: firsf.o $(OBJ)
	$(CC) $(CFLAGS) -o firsf firsf.o $(OBJ) -lm
	mv firsf $(BIN)

iirf: iirf.o $(OBJ)
	$(CC) $(CFLAGS) -o iirf iirf.o $(OBJ) -lm
	mv iirf $(BIN)

