#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 18:54:16 2021

@author: Wenrui Li
"""

import numpy as np                 # Numpy is a library support computation of large, multi-dimensional arrays and matrices.
from PIL import Image              # Python Imaging Library (abbreviated as PIL) is a free and open-source additional library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats.
import matplotlib.pyplot as plt    # Matplotlib is a plotting library for the Python programming language.
import math

# Read in a gray scale TIFF image.
im = Image.open('img04g.tif')
print('Read img04.tif.')
print('Image size: ', im.size)

# Display image object by PIL.
im.show(title='image')

# Import Image Data into Numpy array.
# The matrix x contains a 2-D array of 8-bit gray scale values. 
x = np.array(im)
print('Data type: ', x.dtype)

# Display numpy array by matplotlib.
plt.imshow(x, cmap=plt.cm.gray)
plt.title('Image')
print("size: ", im.size)
# Set colorbar location. [left, bottom, width, height].
cax =plt.axes([0.9, 0.15, 0.04, 0.7]) 
plt.colorbar(cax=cax)
plt.show()

#define size
N =64

#define X from image
X = np.double(x)

#define hamming window
W=np.outer(np.hamming(N),np.hamming(N))

#get dimensions
height=im.size[0]
width=im.size[1]

# find center of image
hstart=math.floor((height-(5*N))/2)
wstart=math.floor((width-(5*N))/2)
print(hstart)
print(wstart)
#initalize Z to 0s that are appropriate size
Z=np.zeros((N,N))
for i in range(1,6):
    for j in range(1,6):
        l=np.arange(hstart+(i-1)*N, hstart+i*N)
        m=np.arange(wstart+(j-1)*N, wstart+j*N)
        z=X[m,l] 
        Z=np.fft.fftshift((1/N**2)*np.abs(np.fft.fft2(z*W))**2)+Z
        # Z=Z+np.log((1/N**2)*np.power(np.abs(np.fft.fftshift(np.fft.fft2(np.multiply(z,W)))),2))
        # Z=Z+np.fft.fftshift(np.abs(np.power(np.fft.fft2(np.multiply(z,W))),2)*(1/N**2))
        # Z=Z+np.fft.fftshift((1/N**2)*np.abs(np.fft.fft2(np.multiply(z,W)))**2)
#average        
Zabs=np.log(Z/25)

# Plot the result using a 3-D mesh plot and label the x and y axises properly. 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
a = b = np.linspace(-np.pi, np.pi, num = N)
X, Y = np.meshgrid(a, b)

surf = ax.plot_surface(X, Y, Zabs, cmap=plt.cm.coolwarm)

ax.set_xlabel('$\\mu$ axis')
ax.set_ylabel('$\\nu$ axis')
ax.set_zlabel('Z Label')

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
