import numpy as np 
from matplotlib import pyplot as plt 
from utils import plotParaChromaticity, plotChrom 

if __name__== '__main__':
    #Load data
    data=np.load('data.npy', allow_pickle=True)[()]
    #List keys of dataset
    x=data['x'][0]
    y=data['y'][0]
    z=data['z'][0]
    plotParaChromaticity(x,y,z)
    D65=[0.3127, 0.3290, 0.3583]
    EE=[0.3333, 0.3333, 0.3333]
    RGB_CIE=[[0.73467, 0.26533, 0.0],[0.27376, 0.71741, 0.00883],[0.16658, 0.00886, 0.82456]]
    RGB709=[[0.64, 0.33, 0.03],[0.3, 0.6, 0.1],[0.15, 0.06, 0.79]]
    plotChrom(RGB_CIE,"RGB CIE", color='g')
    plotChrom(RGB709, "RGB 709", color='b')
    plt.scatter(D65[0], D65[1], label="D65")
    plt.scatter(EE[0], EE[1], label="EE")
    plt.legend()
    plt.savefig("result/chromaticity.png")
    plt.show()
    