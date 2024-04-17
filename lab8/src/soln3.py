import numpy as np 
from matplotlib import pyplot as plt 
import sys
from PIL import Image
import sympy
import os 
import scipy

from utils import threshold, RMSE, fidelity, idx_mat, dither, ungamma

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

    x=ungamma(x, 2.2)
    b2=dither(x, 2)
    rmse2=RMSE(b2, x)
    fid2=fidelity(b2,x)
    print(rmse2)
    print(fid2)
    dith2=Image.fromarray(b2.astype(np.uint8))
    dith2.save("dith2_house.tif")

    
    b4=dither(x, 4)
    rmse4=RMSE(b4, x)
    fid4=fidelity(b4,x)
    dith4=Image.fromarray(b4.astype(np.uint8))
    dith4.save("dith4_house.tif")
    print(rmse4)
    print(fid4)

    b8=dither(x, 8)
    rmse8=RMSE(b8, x)
    fid8=fidelity(b8,x)
    dith8=Image.fromarray(b8.astype(np.uint8))
    dith8.save("dith8_house.tif")

    print(rmse8)
    print(fid8)