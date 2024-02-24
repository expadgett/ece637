import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import colormaps 
import matplotlib
from PIL import Image
import sys
from utils import read_data, svdData, scaled, projPlot, dispalySynth

if __name__== '__main__':
    X=read_data()
    global_mean=X.mean(axis=1, keepdims=True)
    print(global_mean)
