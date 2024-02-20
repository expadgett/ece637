import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import colormaps 
import matplotlib
from PIL import Image
import sys
from subfunctions import histogram, equalize, Fs, editedImage, stretch, gamma, norGamma
from numpy import matlib as mb


if __name__== '__main__':
    image=sys.argv[1]
    image2=sys.argv[3]
    glvl=int(sys.argv[2])
    im = Image.open(image)
    im2=Image.open(image2)    
    # Display image object by PIL.
    im.show(title='image')
    x = np.array(im)
    x2=np.array(im2)
    print(x.shape)
    g1=-(np.log(2)/(np.log(glvl/255)))
    g2=float(sys.argv[4])

    print(g1)
    G=gamma(x, g1)
    ctitle="Gamma Corrected Image with gray level="+str(glvl)+" and gamma="+str(np.round(g1,4))
    cname="gcor"+str(g1)+image+".png"
    editedImage(G+1, ctitle, cname, True)
    ntitle="Gamma Corrected for 1.5 with gray level="+str(glvl)+" and gamma="+str(np.round(g1, 4))
    nname=f"gama15"+str(g1)+".png"
    Gnorm=norGamma(x2,g1,g2)
    editedImage(Gnorm+1, ntitle, nname, True)


