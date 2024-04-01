import matplotlib
import matplotlib.pyplot as plt 
import numpy as np 

def plotvsLamda(datas, labels, title, save, show=True):
    lam=np.linspace(400,700,31, endpoint=True)
    for data, label, color in list(zip(datas, labels,['r','g','b'])):
        plt.plot(lam, data, c=color, label=label)

    plt.xlabel(r"$\lambda$ wavelength (nm)")
    plt.title(title)
    plt.xlim([400,700])
    plt.ylim([0, None])
    plt.tight_layout()
    plt.legend()
    if save:
        plt.savefig(save)
    if show:
        plt.show()

def plotParaChromaticity(X,Y,Z):
    tot=X+Y+Z
    x=np.divide(X,tot)
    y=np.divide(Y,tot)
    plt.plot(x,y, 'r', label="x,y chromaticities")
    plt.xlim([0,1])
    plt.ylim([0,1]) 
    # plt.title("Chromaticity Diagram")

def plotChrom(RGB, label, color):
    print(RGB)
    x=[RGB[0][0], RGB[1][0], RGB[2][0]]
    y=[RGB[0][1], RGB[1][1], RGB[2][1]]
    text=['R','G','B']
    plt.scatter(x,y,color=color)
    for X,Y,T in list(zip(x,y,text)):
        plt.annotate(T, (X,Y))
    plt.plot(x+[x[0]], y+[y[0]], color=color, label=label)

def estM(D, RGB):
    XYZ_wp=np.array([[D[0]/D[1]], [1], [D[2]/D[1]]])
    k_rgb=np.linalg.inv(RGB.T) @ XYZ_wp
    return RGB * np.diag(k_rgb)

def render(R, S, x, y, z, D, RGB, gamma):
    I = R*S
    X = I @ x
    Y = I @ y
    Z = I @ z
    M=estM(D, RGB)
    rgb=np.stack((X,Y,Z), axis=2) @ np.linalg.inv(M).T
    rgb= 255* rgb.clip(0,1)
    f=lambda t: round(255*pow(t/255, 1./gamma))
    F=np.vectorize(f)
    return F(rgb).astype(np.uint8)

def plotColDiag(EE, RGB, gamma):
    M=estM(EE, RGB)
    # M=RGB @ np.identity(3)
    print(M)
    rX=np.linspace(0, 1, 200+1, endpoint=True)
    rY=rX
    X, Y= np.meshgrid(rX, rY)
    Z=1-Y-X
    f = lambda e: np.array([1,1,1]) if (e[0]<0 or e[1]<0 or e[2]<0) else e 
    XYZ=np.stack((X,Y,Z), axis=2) @ np.linalg.inv(M) 
    rgb=np.array([list(map(f, row)) for row in XYZ])
    fG=lambda t: pow(t, 1./gamma)
    fGam=np.vectorize(fG)
    rgb_im=fGam(rgb)
    # print(rgb)
    plt.imshow(rgb_im, origin='lower', extent=[0,1,0,1])
    # plt.show()