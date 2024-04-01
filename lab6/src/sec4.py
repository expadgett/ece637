import numpy as np 
from matplotlib import pyplot as plt 
from utils import plotParaChromaticity, plotChrom, estM, render
from PIL import Image

if __name__== '__main__':
    #Load data
    data=np.load('data.npy', allow_pickle=True)[()]
    #Load reflect
    reflect=np.load('reflect.npy', allow_pickle=True)[()]
    #List keys of dataset
    x=data['x'][0]
    y=data['y'][0]
    z=data['z'][0]
    illum1=data['illum1'][0]
    illum2=data['illum2'][0]
    R=reflect['R']
    D65=[0.3127, 0.3290, 0.3583]
    EE=[0.3333, 0.3333, 0.3333]
    RGB_CIE=np.array([[0.73467, 0.26533, 0.0],[0.27376, 0.71741, 0.00883],[0.16658, 0.00886, 0.82456]])
    RGB709=np.array([[0.64, 0.33, 0.03],[0.3, 0.6, 0.1],[0.15, 0.06, 0.79]])
    M=estM(D65, RGB709)
    print(M)
    rgb=render(R, illum1,  x, y, z, D65, RGB709, 2.2)
    Image.fromarray(rgb).save('result/illum1out.tif')
    rgb=render(R, illum2,  x, y, z, D65, RGB709, 2.2)
    Image.fromarray(rgb).save('result/illum2out.tif')