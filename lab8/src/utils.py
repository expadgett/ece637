import numpy as np
from matplotlib import pyplot as plt
import sys
from PIL import Image
import sympy
import os
import scipy


def threshold(im,T):
    c=im.shape[0]
    r=im.shape[1]
    tim=np.zeros([im.shape[0], im.shape[1]])
    for m in range(c):
        for n in range(r):
            if im[m][n]>T:
                tim[m][n]=255
            else:
                tim[m][n]=0
    return tim


def RMSE(tim, im):
    c=im.shape[0]
    r=im.shape[1]
    if tim.dtype==np.uint8 or im.dtype==np.uint8:
        f=im.clip(0,255).astype(np.double)
        b=tim.clip(0,255).astype(np.double)
    else:
        f=im
        b=tim
    return np.sqrt(np.square(f-b).sum()/(r*c))

def fidelity(tim, im):
    tg=ungamma(tim, 2.2)
    img=ungamma(im, 2.2)
    lt=lpf(tg, 7, 2)
    lim=lpf(img, 7, 2)
    btilde=255*pow((lt/255), (1/3))
    ftilde=255*pow((lim/255), (1/3))
    c=btilde.shape[0]
    r=btilde.shape[1]
    return RMSE(btilde, ftilde)

def ungamma(im, gamma):
    corrected=np.zeros([im.shape[0],im.shape[1]])
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            corrected[i][j]=255*pow((im[i][j]/255), gamma)
    return corrected

def lpf(im, ksize, sigma):
    lpfdx=ksize//2
    print(ksize)
    sq=np.square(range(-lpfdx, lpfdx+1)).reshape([ksize, 1])
    print(sq)
    sq=sq+sq.T
    print(sq)
    kernel=np.exp(-sq/(2*sigma))
    kernel/=kernel.sum()
    ky=kernel.shape[0]
    kx=kernel.shape[1]
    dy=ky//2
    dx=kx//2
    im_out=np.zeros([im.shape[0], im.shape[1]])
    im_out[:dy, :]=im[:dy, :]
    im_out[-dy:, :]=im[-dy:,:]
    im_out[:,:dx]=im[:,:dx]
    im_out[:,:-dx]=im[:,:-dx]
    for i in range(dy, im.shape[0]-dy):
        for j in range(dx, im.shape[1]-dx):
            im_out[i][j]=(im[i-dy:i-dy+ky, j-dx:j-dx+kx]*kernel).sum()
    return im_out

def dither(im, size):
    H, W=im.shape
    b=np.zeros_like(im, dtype=np.uint8)
    IN=[[1, 2], [3, 0]]
    for j in range(size):
        I2N=np.block([[4*IN+1, 4*IN+2],[4*IN+3, 4*IN+4]])
        IN=I2N
    return I2N
    
    
