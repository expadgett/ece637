import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import sys
import math
from specAnalFunctions import betterSpecAnaly, plotPSF, specAnal

if __name__== '__main__':
    image=sys.argv[1]
    show=sys.argv[2]
    # # Read in a gray scale TIFF image.
    # im = Image.open(image)
    # print('Read'+str(image))
    # print('Image size: ', im.size)

    # # Display image object by PIL.
    # im.show(title='image')

    # # Import Image Data into Numpy array.
    # # The matrix x contains a 2-D array of 8-bit gray scale values. 
    # x = np.array(im)
    # print('Data type: ', x.dtype)

    # # Display numpy array by matplotlib.
    # plt.imshow(x, cmap=plt.cm.gray)
    # plt.title('Image')
    # print("size: ", im.size)
    # # Set colorbar location. [left, bottom, width, height].
    # cax =plt.axes([0.9, 0.15, 0.04, 0.7]) 
    # plt.colorbar(cax=cax)
    # plt.show()

    # x = np.array(im).astype(np.double)
    # Ns=[64, 128,256]
    # for i in Ns:
    #     psf=specAnal(x, i)
    #     title=f"PSF with window: {i}"
    #     fname=f"psf{i}.png"
    #     plotPSF(psf,i,title, fname, show)
        
    # N=64 
    # betterPsf=betterSpecAnaly(x, N, 25)
    # plotPSF(betterPsf, N, "Section 1.3 PSF Plot", "psf_25.png", show)

    #Part 2
    N=64
    size=(512,512)
    x=np.random.uniform(-0.5,0.5,size)
    x_scaled=255*(x+0.5)
    img=Image.fromarray(x_scaled.astype(np.uint8))
    img.save("scaled_random_img.png")

    y=np.zeros(size)
    for i in range(size[0]):
        for j in range(size[1]):
            if (i==0) or (j==0):
                y[i,j]=0
            else:
                y[i,j]=3*x[i,j]+0.99*(y[i-1,j]+y[i,j-1])-0.9801*(y[i-1,j-1])

    shiftedy=y+127    
    plt.imshow(shiftedy,cmap=plt.cm.gray)
    # ax=plt.gca()
    # ax.set_axis_off()
    # imgy=Image.fromarray(shiftedy.astype(np.uint8))
    # plt.savefig("scaled_y.png")
    # print(y.shape)
    
    a=b= np.linspace(-np.pi, np.pi, N)
    X, Y = np.meshgrid(a, b)

    S_y=np.log((1/12)*(np.abs(3/((1-0.99*(np.exp(-1j*X)))*(1-0.99*np.exp(-1j*Y))))**2))
    Stitle=f"Theoretical Y magnitude"
    Sname=f"theoretical_y.png"
    plotPSF(S_y, N, Stitle, Sname, True)

    # fig=plt.figure(figsize=(16,8))
    # ax=plt.gca()
    # ax.set_axis_off()
    # ax=fig.add_subplot(121, projection='3d')
    # surf = ax.plot_surface(X, Y, S_y, cmap=plt.cm.coolwarm)
    # ax.set_xlabel('$\\mu$ axis')
    # ax.set_ylabel('$\\nu$ axis')
    # ax.set_zlabel('Z Label')
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    
    # ax.fig.add_subplot(122)
    # cont=ax.contourf(X,Y,S_y, cmap=plt.cm.coolwarm)
    # ax.set_xlabel('$\\mu$ axis')
    # ax.set_ylabel('$\\nu$ axis')
    # plt.title("Theoretical Y Magnitude")
    # plt.savefig("theoretical_y.png")
    # plt.show()

    ypsfbetter=betterSpecAnaly(y,N, 25)
    ytitle=f"PSF of Y"
    yname=f"ypsf_better.png"
    plotPSF(ypsfbetter,N, ytitle,yname,True)




