import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import colormaps 
import matplotlib
from PIL import Image
import sys
from utils import read_data2
from pca import class_PCA, alphabet

if __name__== '__main__':
    train, ftrain=read_data2("training_data")
    test, ftest=read_data2("test_data")
    classify=class_PCA(neig=10)
    classify.fit(train)
    for opt in ["rk", "rwc", "rwcdiag", "id","rkdiag"]:
        pred = classify.predict(test, option=opt)
        for s,t in list(zip(alphabet,pred[0])):
            if s!=t:
                print([s,t])



                