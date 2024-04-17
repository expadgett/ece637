import numpy as np 
from matplotlib import pyplot as plt 
import sys
from PIL import Image
import sympy
import os 
import scipy

from utils import threshold, RMSE, fidelity, dither

if __name__== '__main__':
    #Load data
    im=sys.argv[1]
    x=np.array(Image.open(os.path.join('bin', im)))
    T=127
    tx=(threshold(x, T))
    thresh_im=Image.fromarray(tx)
    thresh_im.save("t_house.tif")
    rmse=RMSE(tx, x)
    print(rmse)
    fid=fidelity(tx, x)
    print(fid)
    print(dither(x, 2))
