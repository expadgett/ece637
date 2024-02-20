
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import colormaps 
import matplotlib
from PIL import Image
import sys
from subfunctions import histogram, equalize, Fs, editedImage, stretch 
from numpy import matlib as mb


if __name__== '__main__':
    glvl=int(sys.argv[1])

    xgray=glvl*np.ones((16,256))
    funit=np.array([[255, 255, 0, 0],[255, 255, 0 , 0], [0 , 0, 255, 255],[ 0, 0, 255, 255]])
    xcheck=mb.repmat(funit, 4, 4*16)
    xunit=np.vstack((xcheck, xgray))
    x=mb.repmat(xunit, 8, 1)
    title="Checker Board Image with gray level="+str(glvl)
    fname=f"checkerboard{glvl}.png"
    editedImage(x+1, title, fname, True)

    

    xgray=glvl*np.ones((32*2,512*2))
    funit=np.array([[255, 255, 0, 0],[255, 255, 0 , 0], [0 , 0, 255, 255],[ 0, 0, 255, 255]])
    xcheck=mb.repmat(funit, 8*2, 16*16)
    xunit=np.vstack((xcheck, xgray))
    x=mb.repmat(xunit, 32, 4)
    title="Checker Board Image 1024 with gray level="+str(glvl)
    fname=f"checkerboard1024{glvl}.png"
    editedImage(x+1, title, fname, True)

    
