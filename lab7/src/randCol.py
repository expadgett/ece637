import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

if __name__== '__main__':
    image=sys.argv[1]
    name=sys.argv[2]
    
    #Read in a segmentation TIFF image
    im=Image.open(image)

    #Import image data inot numpy array
    x=np.array(im)

    #obtain number of segmentaiton area
    N=np.max(x)

    #Randomly set color map
    cmap=mpl.colors.ListedColormap(np.random.rand (N+1,3))
    plt.imshow(x, cmap=cmap, interpolation='none')
    plt.colorbar()
    plt.title(image)
    plt.savefig(name)