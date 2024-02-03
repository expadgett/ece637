import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import colormaps 
import matplotlib
from PIL import Image
import sys


if __name__== '__main__':
    image=sys.argv[1]
    im = Image.open(image)

    # Display image object by PIL.
    im.show(title='image')
    print("image")
    x = np.array(im)
    print("after x")

    # Display numpy array by matplotlib.
    # plt.imshow(x, cmap="gray")
    # print("after imshow")
    # plt.title('Image')
    # gname=f"gray_kids.png"
    # plt.savefig(gname)
    plt.hist(x.flatten(), bins=np.linspace(0, 255, 256))
    plt.title("Gray Scale race.tif Histogram")
    plt.show()
    # # fname=f"race_hist.png"
    # # plt.savefig(fname)