import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from src.SpectrumAnalysis import betterSpecAnalyse, plotSpecAnalyse

if __name__ == '__main__':
    im_shape = (512, 512)
    x = np.random.uniform(-0.5, 0.5, im_shape)
    x_scaled = 255*(x + 0.5)

    im_x = Image.fromarray(x_scaled.astype(np.uint8))
    im_x.save("outs/x_scaled.png")

    y = np.zeros(im_shape)
    pole = 0.99

    for i in range(im_shape[0]):
        for j in range(im_shape[1]):
            if (i == 0) or (j == 0):
                y[i, j] = 0
            else:
                y[i, j] = 3*x[i, j] + pole*(y[i-1, j] + y[i, j-1]) - pole*pole*(y[i-1, j-1])


    plt.imshow((y+127), cmap=plt.cm.gray)
    ax = plt.gca()
    ax.set_axis_off()
    im_y = Image.fromarray((y+127).astype(np.uint8))
    # im_y.save("outs/y_scaled.png")
    plt.savefig("outs/y_scaled.png", bbox_inches="tight")
    # plt.show()

    windows = 25

    windowSize = 64

    logPowerSpectral = betterSpecAnalyse(y, windowSize, windows)
    
    plotTitle = f"log power spectrum of IID Uniform Random Variables"
    plotFilename = f"outs/uniPowerSpectral_{windowSize}.png"
    plotSpecAnalyse(logPowerSpectral, windowSize, plotTitle, plotFilename)
