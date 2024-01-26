import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import math

def specAnal(x, N):
    i = 99
    j = 99

    z = x[i:N+i, j:N+j]

    # Compute the power spectrum for the NxN region.
    Z = (1/N**2)*np.abs(np.fft.fft2(z))**2

    # Use fftshift to move the zero frequencies to the center of the plot.
    Z = np.fft.fftshift(Z)

    # Compute the logarithm of the Power Spectrum.
    Zabs = np.log(Z)
    return Zabs


def betterSpecAnaly(x, N,winSize):
    height=x.shape[1]
    width=x.shape[0]
    hstart=math.floor((height-(5*N))/2)
    wstart=math.floor((width-(5*N))/2)
    psf=np.zeros((N,N))

    W=np.outer(np.hamming(N),np.hamming(N))
 
    for j in range (1,6):
        for i in range(1,6):
            starj=hstart+(i-1)*N
            stari=wstart+(j-1)*N
            z=x[stari:stari+N, starj:starj+N]
            z=z*W
            Z=(1/N**2)*np.abs(np.fft.fft2(z))**2
            Z=np.fft.fftshift(Z)
            psf+=Z

    logpsf=np.log(psf/25) 
    return logpsf

def plotPSF(Z, N, title="", save="", show=True):

    a = b = np.linspace(-np.pi, np.pi, N)
    X, Y = np.meshgrid(a, b)

    fig = plt.figure(figsize=(16,8))
    if title:
        plt.title(title)
    ax=plt.gca()
    ax.set_axis_off()

    ax = fig.add_subplot(121, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=plt.cm.coolwarm)
    ax.set_xlabel('$\\mu$ axis')
    ax.set_ylabel('$\\nu$ axis')
    ax.set_zlabel('Z Label')
    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax=fig.add_subplot(122)
    cont=ax.contourf(X,Y,Z, cmap=plt.cm.coolwarm)
    ax.set_xlabel('$\\mu$ axis')
    ax.set_ylabel('$\\nu$ axis')

    if save:
        plt.savefig(save)
    if show:
        plt.show()

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