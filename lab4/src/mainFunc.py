import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import colormaps 
import matplotlib
from PIL import Image
import sys
from subfunctions import histogram, equalize, Fs, editedImage, stretch 


if __name__== '__main__':
    image=sys.argv[1]
    operation=sys.argv[2]

    im = Image.open(image)

    # Display image object by PIL.
    im.show(title='image')
    x = np.array(im)
    print(x.shape)
    # # Show gray scaled image and save it
    # plt.figure(2)
    # plt.imshow(x, cmap=plt.cm.gray)
    # grayname=f"gray"+image+".png"
    # graytitle="Gray Scaled "+image
    # plt.title(graytitle)
    # plt.savefig(grayname)

    # #find histogram of image and save it
    # title=image+" Histogram"
    # fname=f"hist_"+image+".png"
    # histogram(x,title,fname,True)
    print(operation)
    if (operation==1): #equalization
        print("entered equalization")
        #find cdf of image
        cdftitle="CDF of "+image
        cdfname=f"cdf_"+image+".png"
        Y=Fs(x, cdftitle, cdfname, True)

        #equalize image
        eqtitle=image+" Equalized Histogram2"
        eqname=f"equailzed_hist2_"+image+".png"
        Z=equalize(x, eqtitle, eqname,True)

        eqim="Equalized Image2"
        eqimname=f"equalize2_"+image+".png" 
        editedImage(Z, eqim, eqimname,True)
    else: #(operation==2): #stretch
        print("entered stretch")
        shisttitle="Contrast Stretch Histogram"
        shistname="stretch_hist"+image+".png"
        T1=min(x.flatten())
        T2=max(x.flatten())
        print("T1: "+str(T1)+" T2: "+str(T2))
        s=stretch(x, T1, T2, shisttitle, shistname)
        print(s.shape)
        sim=np.reshape(s,x.shape)
        stitle="Contrast Stretch Image"
        sname=f"stretch_"+image+".png"
        editedImage(sim, stitle,sname, True)