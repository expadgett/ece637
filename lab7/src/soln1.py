import numpy as np 
from matplotlib import pyplot as plt 
import sys
from PIL import Image
import sympy
import os 
import scipy


if __name__== '__main__':
    #Load data
    im=sys.argv[1]
    y=np.array(Image.open(os.path.join('bin', 'img14g.tif')))
    x=np.array(Image.open(os.path.join('bin', im)))
    m=int(np.floor(y.shape[0]/20))
    n=int(np.floor(y.shape[1]/20))
    N=m*n
    # print(m)
    # print(n)
    # print(N)
    i=0

    Z=np.zeros((N,49))
    Y=np.zeros(N)
    r=0
    c=0
    for j in range(1,m+1):
        for k in range(1,n+1):
            startx=20*j-4
            endx=20*j+3
            starty=20*k-4
            endy=20*k+3
            Z[i]=np.reshape( x[startx:endx, starty:endy],(1,49))
            Y[i]=y[20*j-1, 20*k-1]
            i=i+1

    # print(i)
    # print(Z)
    # print(Y)
    # print(Y.shape[1])
    R_zz=(Z.T @ Z)/N
    r_zy=(Z.T @ Y)/N
    # theta_star=np.divide(r_zy,R_zz).reshape(7,7)
    theta=np.linalg.solve(R_zz,r_zy).reshape(7, 7)
    print(theta.round(decimals=4).T)

    kx=theta.shape[0]
    ky=theta.shape[1]
    dx=kx//2
    dy=ky//2
    y_out=np.zeros((x.shape[0], x.shape[1]))
    y_out[:dy,:]=x[:dy,:]
    y_out[-dy:,:]=x[-dy:,:]
    y_out[:,:dx]=x[:,:dx]
    y_out[:,:-dx]=x[:,:-dx]
    for i in range(dy, x.shape[0]-dy):
        for j in range(dx, x.shape[1]-dx):
            y_out[i][j]=(x[i-dy:i-dy+ky, j-dx:j-dx+kx]*theta.T).sum()
    filtered_img=Image.fromarray(y_out.clip(0,255).astype(np.uint8))
    filtered_img.show()
    filtered_img.save('filtered_'+im)

