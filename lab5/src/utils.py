import numpy as np
from PIL import Image    
import matplotlib.pyplot as plt

# The following are strings used to assemble the data file names
datadir='.'    # directory where the data files reside
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

def estimateParams(X):
    N, mu = X.shape[-1], X.mean(axis=-1, keepdims=True)
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
