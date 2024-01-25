import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import math

def betterSpecAnaly(x, N,winSize):
    height=x.shape[0]
    width=x.shape[1]
    hstart=math.floor((height-(5*N))/2)
    wstart=math.floor((width-(5*N))/2)
    Z=np.zeros((N,N))

    upRtCn=[]
    winx=winy=int(math.sqrt(winSize))//2
    for i in range(1,winx):
        for j in range(1,winy):
            l=hstart+(i-1)*N
            m=wstart+(j-1)*N 
            upRtCn.append(tuple((l,m)))

    W=np.outer(np.hamming(N),np.hamming(N))
    pow=np.zeros((N,N))
    for (i, j) in upRtCn:
       print(i, j)
       z=x[i:i+N, j:j+N]
       z=W * z
       Z=(1/N**2)*np.abs(np.fft.fft2(z))**2
       Z=np.fft.fftshift(Z)
    #    pow+=np.fft.fftshift((1/N**2)*np.abs(np.fft.fft2(z))**2)
       pow+=Z
       
    pow*=(1/winSize) 
    logpow=np.log(pow)
    
    # Z=np.log(Z/winSize)
    print(pow.shape)
    return logpow

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # a = b = np.linspace(-np.pi, np.pi, N)
    # X, Y = np.meshgrid(a, b)

    # surf = ax.plot_surface(X, Y, Z, cmap=plt.cm.coolwarm)

    # ax.set_xlabel('$\\mu$ axis')
    # ax.set_ylabel('$\\nu$ axis')
    # ax.set_zlabel('Z Label')

    # fig.colorbar(surf, shrink=0.5, aspect=5)

    # plt.show()

def plotSpecAnalyse(S, windowSize, plotTitle="", savePlot="", showPlot=True):
    u = v = np.linspace(-np.pi, np.pi, windowSize)
    us, vs = np.meshgrid(u, v)
    
    fig = plt.figure(figsize=(15, 6))
    if plotTitle:
        plt.title(plotTitle, color="blue", fontsize=10)
    ax = plt.gca()
    ax.set_axis_off()

    ax = fig.add_subplot(121, projection="3d")
    surf = ax.plot_surface(us, vs, S, cmap="coolwarm")
    ax.set_xlabel(r"$\mu$ axis", color="red")
    ax.set_ylabel(r"$\nu$ axis", color="red")
    ax.set_title(r"$\log S(\mu, \nu)$", color="red", fontsize=12)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax = fig.add_subplot(122)
    cont = ax.contourf(us, vs, S, cmap="coolwarm")
    ax.set_xlabel(r"$\mu$ axis", color="red")
    ax.set_ylabel(r"$\nu$ axis", color="red")
    ax.set_title(r"$\log S(\mu, \nu)$", color="red", fontsize=12)

    if savePlot:
        plt.savefig(savePlot, bbox_inches="tight")
    
    if showPlot:
        plt.show()