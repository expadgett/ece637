import numpy as np 
from matplotlib import pyplot as plt 
import sys
from PIL import Image
import sympy
import os 
import scipy

from utils import threshold, RMSE, fidelity, idx_mat, dither, ungamma, diff_error

if __name__== '__main__':
    #Load data
    im=sys.argv[1]
    gx=np.array(Image.open(os.path.join('bin', im)))
    T=127
    tx=(threshold(gx, T))
    thresh_im=Image.fromarray(tx)
    thresh_im.save("t_house.tif")
    rmse=RMSE(tx, gx)
    print("RMSE: ", rmse)
    fid=fidelity(tx, gx)
    print("FID: ", fid)

    x=ungamma(gx, 2.2)
    b2=dither(x, 2)
    rmse2=RMSE(b2, gx)
    fid2=fidelity(b2,gx)
    print("RMSE2: ",rmse2)
    print("FID2: ", fid2)
    dith2=Image.fromarray(b2.astype(np.uint8))
    dith2.save("dith2_house.tif")

    
    b4=dither(x, 4)
    rmse4=RMSE(b4, gx)
    fid4=fidelity(b4,gx)
    dith4=Image.fromarray(b4.astype(np.uint8))
    dith4.save("dith4_house.tif")
    print("RMSE4: ", rmse4)
    print("FID4: ",fid4)

    b8=dither(x, 8)
    rmse8=RMSE(b8, gx)
    fid8=fidelity(b8,gx)
    dith8=Image.fromarray(b8.astype(np.uint8))
    dith8.save("dith8_house.tif")

    print("RMSE8: ", rmse8)
    print("FID8: ",fid8)

    b_error=diff_error(x, T)
    ermse=RMSE(b_error,gx)
    efid=fidelity(b_error, gx)
    print("ERMSE: ", ermse)
    print("EFID: ", efid)
    diffe=Image.fromarray(b_error.astype(np.uint8))
    diffe.save("diffise_error_house.tif")