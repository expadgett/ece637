import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import colormaps 
import matplotlib
from PIL import Image
import sys
from utils import read_data, svdData, scaled, projPlot, dispalySynth

if __name__== '__main__':
    X= read_data()
    muHat=X.mean(axis=-1, keepdims=True)
    nfolder=12
    nalpha=26
    U, D, V=svdData((X-muHat)/np.sqrt(nfolder*nalpha-1))
    top=12
    Utop=U[:,:top]
    scaled(Utop)
    nchar=4
    Yconcat=U.conj().T @ (X[:,:nchar]-muHat)
    projPlot(Yconcat)
    vecImg = X[:, 0].reshape((-1,1))
    m=[1, 5, 10, 15, 20, 30]
    dispalySynth(vecImg, muHat, U, m)

