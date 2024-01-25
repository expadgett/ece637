import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import math

def betterSpecAnalyse(x, windowSize, nWindows, showWindow=False, saveWindow=""):
    xCenter = x.shape[0]//2
    yCenter = x.shape[1]//2

    nWindowsx = nWindowsy = int(math.sqrt(nWindows))//2
    print(nWindowsx)
    startIndices = []
    for i in range(-nWindowsx, nWindowsx+1):
        for j in range(-nWindowsy, nWindowsy+1):
            startI = int(xCenter + (i-0.5)*windowSize)
            startJ = int(yCenter + (j-0.5)*windowSize)
            startIndices.append(tuple((startI, startJ)))
    print(startIndices)
    if showWindow:
        a = Image.fromarray(x).convert("RGB")
        draw = ImageDraw.Draw(a)
        for (i, j) in startIndices:
            draw.rectangle((j, i, j+windowSize, i+windowSize), outline=(255, 0, 0), width=2)
        
        plt.imshow(np.array(a).astype(np.uint8))
        plt.axis("off")
        if saveWindow:
            plt.savefig(saveWindow, bbox_inches="tight")
        
        plt.show()


    W = np.outer(np.hamming(windowSize), np.hamming(windowSize))

    powerSpec = np.zeros((windowSize, windowSize))

    for (i, j) in startIndices:
        print(i, j)
        z = x[i:i+windowSize, j:j+windowSize]
        z = W * z

        Z = (1/windowSize**2)*np.abs(np.fft.fft2(z))**2
        Z = np.fft.fftshift(Z)
        powerSpec += Z

    powerSpec *= (1/nWindows)
    logPowerSpec = np.log(powerSpec)

    return logPowerSpec
    

def specAnalyse(x, windowSize, showWindow=False):
    i = 99
    j = 99
    z = x[i:i+windowSize, j:j+windowSize]

    if showWindow:
        a = Image.fromarray(x).convert("RGB")
        draw = ImageDraw.Draw(a)
        draw.rectangle((j, i, j+windowSize, i+windowSize), outline=(255, 0, 0), width=2)
        plt.imshow(np.array(a).astype(np.uint8), cmap="gray")
        plt.axis("off")
        plt.show()


    powerSpec = (1/windowSize**2)*np.abs(np.fft.fft2(z))**2
    powerSpec = np.fft.fftshift(powerSpec)

    logPowerSpec = np.log(powerSpec)

    return logPowerSpec


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
