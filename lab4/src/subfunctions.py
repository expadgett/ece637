import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import colormaps 
import matplotlib
from PIL import Image
import math


def histogram(x, title, save, show=False):
    plt.figure(3)
    plt.hist(x.flatten(), bins=np.linspace(0, 255, 256))
    plt.title(title)
    plt.xlabel("Bin Number")
    plt.ylabel("Number of Pixels")
    if save:
        plt.savefig(save)
    if show:
        plt.show()


def Fs(x, title, save, show=True):
    Xs=plt.hist(x.flatten(), bins=np.linspace(0, 255, 256))
    Y=np.cumsum(Xs[0])/np.sum(Xs[0])
    plt.figure(4)
    plt.plot(Y)
    plt.title(title)
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Fs")
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    return Y

def equalize(Y, title, save, show=True):
    histx,bins = np.histogram(Y.flatten(), np.linspace(0,255,256), density=True)
    cdf=np.cumsum(histx)
    t=np.floor(255*cdf).astype(np.uint8)

    Z=np.zeros(Y.shape)

    for i in range (Y.shape[0]):
        for j in range (Y.shape[1]):
            Z[i][j]=t[Y[i][j]]
    plt.figure(5)
    plt.hist(Z.flatten(), bins=np.linspace(0,255,256))
    plt.xlim((0,255))
    plt.title(title)
    plt.xlabel("Bin Number")
    plt.ylabel("Number of Pixels")
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    return Z
    

    # Ymin=np.min(Y.flatten())
    # Ymax=np.max(Y.flatten())
    # Z=255*((Y.flatten()-Ymin)/(Ymax-Ymin)) 
    # plt.figure(5)
    # plt.hist(Z.flatten(), bins=np.linspace(0, 255, 256))
    # plt.title(title)
    # plt.xlabel("Bin Number")
    # plt.ylabel("Number of Pixels")
    # if save:
    #     plt.savefig(save)
    # if show:
    #     plt.show()
    
    # return np.uint8(Z)

def editedImage(x, title, save, show=True):
    print("entered edited image")
    plt.figure(6)
    plt.imshow(x, cmap="gray")
    plt.title(title)
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    
def stretch(x, T1, T2, title, save, show=True):
    s=np.zeros(len(x.flatten()))
    X=x.flatten()
    for i in range (0, len(X)):
        if (X[i]<=T1):
            s[i]=0
        elif (X[i]>=T2):
            s[i]=255
        else:
            s[i]=math.floor(255/(T2-T1)*(X[i]-T1))
    plt.figure(5)
    plt.hist(s.flatten(), bins=np.linspace(0, 255, 256))
    plt.title(title)
    plt.xlabel("Bin Number")
    plt.ylabel("Number of Pixels")
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    return s

def clip(x):
    if (x>255):
        x=255
    elif (x<0):
        x=0
    return x

def gamma(x, g):
    size=x.shape
    cor=np.zeros(x.shape)
    for i in range(0, size[0]):
        for j in range (1, size[1]):
            cor[i,j]=255*(x[i,j]/255)**(1/g)
            clip(cor[i,j]) 

    return cor

def norGamma(x, g1, g2):
    size=x.shape
    cor=np.zeros(x.shape)
    for i in range(0, size[0]):
        for j in range (1, size[1]):
            cor[i,j]=255*(x[i,j]/255)**(g2/g1)
            clip(cor[i,j])

    return cor