import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import math
from specAnalFunctions import betterSpecAnaly, plotSpecAnalyse

if __name__== '__main__':
    # Read in a gray scale TIFF image.
    im = Image.open('img04g.tif')

    x = np.array(im).astype(np.double)
    N=64
    spec=betterSpecAnaly(x, N, 25)
    plotSpecAnalyse(spec, N)