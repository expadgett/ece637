from typing import Any
import numpy as np
import math
from PIL import Image    
import matplotlib.pyplot as plt
from string import ascii_lowercase as alphabet
import os
# The following are strings used to assemble the data file names
datadir='training_data'    # directory where the data files reside
dataset=['arial','bookman_old_style','century','comic_sans_ms','courier_new',
  'fixed_sys','georgia','microsoft_sans_serif','palatino_linotype',
  'shruti','tahoma','times_new_roman']
datachar='abcdefghijklmnopqrstuvwxyz'

def read_data():
    """
        Read in all these training images into columns of a single matrix X.
    
        Returns:
            X: Image column matrix.
    
    """

    Rows=64    # all images are 64x64
    Cols=64
    n=len(dataset)*len(datachar)  # total number of images
    p=Rows*Cols   # number of pixels

    X=np.zeros((p,n))  # images arranged in columns of X
    k=0
    for dset in dataset:
        for ch in datachar:
            fname='/'.join([datadir,dset,ch])+'.tif'
            im=Image.open(fname)
            img = np.array(im)
            X[:,k]=np.reshape(img,(1,p))
            k+=1
    return X

def read_data2(dir):
    height=64
    width=64
    _, folders, _ = list(os.walk(dir))[0]
    folders.sort()
    data=np.zeros((len(folders), len(alphabet), height, width))
    for i, folder in enumerate(folders):
        for j, char in enumerate(alphabet):
            data[i][j]=np.array(Image.open(os.path.join(dir, folder, char+'.tif')))
    return data, folders

def read_test_data():
    Rows=64
    Cols=64
    n=len(dataset)*len(datachar)
    p=Rows*Cols
    X=np.zeros((p,n))
    k=0
    for dset in dataset:
        for ch in datachar:
            fname='/'.join(['veranda',ch])+'.tif'
            im=Image.open(fname)
            img=np.array(im)
            X[:,k]=np.reshape(img, (1,p))
            k+=1
    return X


def div(x):
    t=math.floor(math.sqrt(x)+1e-6)
    while x%t!=0:
        t-=1
    return t, x//t

def scaled(eigvec, height=64, width=64):
    if (height*width==eigvec.shape[0]):
        neig=eigvec.shape[-1]
        rs, cs = div(neig)
        fig, ax = plt.subplots(rs,cs)
        if rs==1:
            ax=[ax]
        if cs==1:
            for e in ax:
                ax = [[e]]
        for i, vec in enumerate(eigvec.T):
            r, c = i//cs, i%cs
            vmax, vmin = vec.max(), vec.min()
            vec = (vec-vmin)/(vmax-vmin)
            ax[r][c].imshow(vec.reshape((height, width)), cmap="gray", interpolation="none")
            ax[r][c].set_title("eigenvector {}".format(i+1))
            ax[r][c].grid(False)
        plt.tight_layout()
        plt.savefig('result/scaled.png')
        plt.show()
    else:
        print("failed!")

def projPlot(Y, rcoef=10):
    nchar=Y.shape[-1]
    for char, proj in list(zip(alphabet[:nchar], Y.T)):
        plt.plot(range(1, rcoef+1), proj[:rcoef],label=char)
    plt.legend()
    plt.xlim([1, rcoef])
    plt.title("first {} projection coefficient for first {} letters".format(rcoef,nchar))
    plt.xlabel("Index of Coefficient")
    plt.ylabel("Projection Coefficient")
    plt.tight_layout()
    plt.savefig("result/projection.png")
    plt.show()

def dispalySynth(vec, muHat, U, listEig, height=64, width=64):
    cs, rs = div(len(listEig))
    fig, ax = plt.subplots(rs, cs)
    ax= [ax] if rs==1 else ax
    ax = [[e] for e in ax] if cs==1 else ax
    
    for i, neig in enumerate(listEig):
        Utop=U[:, :neig]
        r, c = i//cs, i%cs
        Y=Utop.conj().T @ (vec-muHat)
        imSynth = Utop @ Y+muHat
        ax[r][c].imshow(imSynth.reshape((height, width)), cmap="gray", interpolation="none")
        ax[r][c].set_title(r"synthesize with m={}".format(neig))
    plt.tight_layout()
    plt.savefig("result/synthesized.png")
    plt.show()

def svdData(X):
    U, D, Vh = np.linalg.svd(X, full_matrices=False)
    return U, D, Vh.conj().T

# display samples of the training data
def display_samples(X,ch):
    """
    Display samples.

    Args:
    X (ndarray) : Image column matrix.
    ch (char) : A char 'a'~'z'.

    Returns:

    """
    ind = ord(ch)-ord('a')
    fig, axs = plt.subplots(3, 4)
    for k in range(len(dataset)):
        img=np.reshape(X[:,26*(k-1)+ind],(64,64))

        axs[k//4,k%4].imshow(img,cmap=plt.cm.gray, interpolation='none') 
        axs[k//4,k%4].set_title(dataset[k])

def plot_data(x, title, save, show=False):
    plt.figure()
    plt.scatter(x[0], x[1], s=3)
    plt.axis("equal")
    plt.title(title)
    plt.xlabel("1st Component")
    plt.ylabel("2nd Component")
    name=f"output"+str(save)+".png"
    if save:
        plt.savefig(name)
    if show:
        plt.show()

def gen(R, mu=None, N=1000):
    dim=R.shape[0]
    D, V =np.linalg.eig(R)
    print(mu)
    if mu is None:
        return V @ np.diag(np.sqrt(D)) @ np.random.randn(dim, N)
    return V @ np.diag(np.sqrt(D)) @ np.random.randn(dim, N) +mu

def estParams(X):
    N =X.shape[-1]
    mu= X.mean(axis=-1, keepdims=True)
    R= ((X-mu) @ (X-mu).T)/(N-1)
    return R, mu

def decorr(X, R, mu=None):
    if mu is not None:
        X-=mu
    D, V =np.linalg.eig(R)
    return V.T @ X

def whiten(X, R, mu=None):
    if mu is not None:
        X-=mu
    D, V =np.linalg.eig(R)
    return np.diag(1./np.sqrt(D))@ (V.T @ X)

