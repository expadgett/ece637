import numpy as np
from matplotlib import pyplot as plt
import sys
from PIL import Image
import sympy
import os
import scipy
from scipy.ndimage import convolve

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
    kernel=kernel_gauss(7,2)
    lt=convolve(tg, kernel, mode='nearest')
    lim=convolve(img, kernel, mode='nearest')
    btilde=255*pow((lt/255), (1/3))
    ftilde=255*pow((lim/255), (1/3))
    return RMSE(btilde, ftilde)

def ungamma(im, gamma):
    corrected=np.zeros([im.shape[0],im.shape[1]])
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            corrected[i][j]=255*pow((im[i][j]/255), gamma)
    return corrected

def kernel_gauss(ksize, sigma):
    lpfdx=ksize//2
    sq=np.square(range(-lpfdx, lpfdx+1)).reshape([ksize, 1])
    sq=sq+sq.T
    kernel=np.exp(-sq/(2*sigma))
    kernel/=kernel.sum()
    return kernel

def idx_mat(size):
    I2=[[1,2],[3,0]]
    k=4*np.ones((2,2), dtype=int)
    I=0
    for j in range(size.bit_length()-1):
        I=np.kron(k,I)+np.kron(I2, np.ones_like(I, dtype=int))
    return I

def dither(x, N):
    H, W=x.shape
    b=np.zeros_like(x, dtype=np.uint8)
    print(idx_mat(N))
    T=255*((idx_mat(N)+0.5)/(N*N))
    for i in range(0, H):
        for j in range(0, W):
            m=i%N
            n=j%N
            if x[i,j]>T[m,n]:
                b[i, j]=255
            else:
                b[i,j]=0
    return b
    
def diff_error(x, T):
    g101=3/16 
    g10=5/16
    g11=1/16
    g01=7/16
    h=x.shape[0]
    w=x.shape[1]
    e=np.zeros(x.shape)
    b=np.zeros(x.shape)
    ftilde=np.zeros(w)
    for j in range(1,w):
        e[0, j]=x[0, j]+g01*e[0,j-1]
        b[0, j]=255*(e[0,j]>T)
        e[0,j]=e[0,j]-b[0,j]
    for k in range(1,h):
        ftilde[1:-1]=g101*e[k-1, 2:]+g10*e[k-1, 1:-1]+g11*e[k-1, :-2]
        ftilde[-1]=g10*e[k-1, -1]+g11*e[k-1,-2]
        e[k, 0]=x[k,0]+g10*e[k-1, 0]+g101*e[k-1, 1]
        b[k,0]=255*(e[k,0]>T)
        e[k,0]=e[k,0]-b[k,0]
        for j in range(1,w):
            e[k,j]=x[k,j]+g01*e[k,j-1]+ftilde[j]
            b[k,j]=255*(e[k,j]>T)
            e[k,j]=e[k,j]-b[k,j]

    return b