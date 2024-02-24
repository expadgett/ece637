
from typing import Any
import numpy as np
import math
from PIL import Image    
import matplotlib.pyplot as plt
from string import ascii_lowercase as alphabet
import os
from utils import svdData, estParams
class class_PCA:
    def __init__(self, neig=10):
        self.nfolder=12
        self.alphabet=alphabet
        self.nchar=26
        self.neig=neig
        self.height=None
        self.width=None
        self.globalmu = None
        self.A=None
        self.ps=None
        self.R_wc=None
    
    def fit(self, train):
        self.nfolder, self.nchar, self.height, self.width = train.shape
        X=np.reshape(train, (self.nfolder*self.nchar, self.height*self.width)).T 
        self.globalmu=X.mean(axis=-1, keepdims=True)
        U, D, V = svdData((X-self.globalmu)/math.sqrt((12*26)-1))
        self.A=U[:, :self.neig].conj().T
        self.ps= [None] * self.nchar
        self.R_wc=np.zeros((self.neig, self.neig))
        for idx, char in enumerate(self.alphabet[:self.nchar]):
            x=train[:, idx].reshape(self.nfolder, -1).T
            y=self.A @(x-self.globalmu)
            R, mu=estParams(y)
            self.ps[idx]={"mu":mu, "cv":R, "icov":np.linalg.inv(R), "ldcov":np.log(np.linalg.det(R))}
            self.R_wc+=R
        self.R_wc/=self.nchar
        self.invR_wc=np.linalg.inv(self.R_wc)

    def predict(self, test, option=None):
        print(option)
        data_shape=list(test.shape)
        X=np.reshape(test, (-1, self.height*self.width)).T 
        Y=self.A @ (X-self.globalmu)
        pred=np.empty((Y.shape[-1],), dtype='str')
        pred[:]=' '
        if option is None or option =="rk":
            f=lambda y, i: (y-self.ps[i]["mu"]).T @ self.ps[i]["icov"] @ (y-self.ps[i]["mu"]) + self.ps[i]["ldcov"]
        elif option =="rkdiag":
            f=lambda y, i: (y-self.ps[i]["mu"]).T @np.linalg.inv(np.diag(np.diag(self.ps[i]["cv"]))) @ (y-self.ps[i]["mu"]) + np.log(np.linalg.det(np.diag(np.diag(self.ps[i]["cv"]))))
        elif option=="rwc":
            f=lambda y,i : (y-self.ps[i]["mu"]).T @ self.invR_wc @ (y-self.ps[i]["mu"])
        elif option=="rwcdiag":
            f=lambda y, i: (y-self.ps[i]["mu"]).T @ np.linalg.inv(np.diag(np.diag(self.R_wc))) @ (y-self.ps[i]["mu"])
        elif option=="id":
            f=lambda y, i:(y-self.ps[i]["mu"]).T @(y-self.ps[i]["mu"])
        else: 
            print("error")
        for idx, y in enumerate(Y.T):
            y=y.reshape((-1,1))
            id_pred=min(range(self.nchar), key=lambda i:f(y,i))
            pred[idx]=self.alphabet[id_pred]
        return pred.reshape(data_shape[:-2])