import numpy as np 
from matplotlib import pyplot as plt 
from utils import plotvsLamda

if __name__== '__main__':
    #Load data
    data=np.load('data.npy', allow_pickle=True)[()]
    #List keys of dataset
    data.keys()
    print(data.keys())
    x=data['x'][0]
    y=data['y'][0]
    z=data['z'][0]
    illum1=data['illum1'][0]
    illum2=data['illum2'][0]
    A_inv=[[0.243, 0.856, -0.044],[-0.391, 1.165, 0.087],[0.01, -0.008, 0.563]]
    lms= A_inv @ np.vstack([x,y,z])
    l0=lms[0]
    m0=lms[1]
    s0=lms[2]
    plotvsLamda([x,y,z],['x0','y0','z0'],r"Color matching Function for X, Y, Z", 'result/clrmatchxyz.png')
    plotvsLamda([l0,m0,s0],['l0','m0','s0'], r"Color Matching for l0, m0, s0", 'result/clrmatchlms.png')
    plotvsLamda([illum1, illum2],['D65','Flurorescent Light'], r"Spectrum D65 and Flourescent Light vs Wavelength",'result/illuminants.png')
    

