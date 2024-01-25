import numpy as np
from PIL import Image
from src.SpectrumAnalysis import specAnalyse, betterSpecAnalyse, plotSpecAnalyse
import sys

if __name__ == '__main__':
    image_path = sys.argv[1]
    im = Image.open(image_path)

    x = np.array(im).astype(np.double)

    windowSizes = [64, 128, 256]
    
    for windowSize in windowSizes:
        normalSpec = specAnalyse(x, 
                                 windowSize=windowSize, 
                                 showWindow=False)
        
        plotFileName = f"outs/specAnal_{windowSize}.png"
        
        plotTitleName = f"log power spectrum, window size = {windowSize}"
        
        plotSpecAnalyse(normalSpec, 
                     windowSize, 
                     plotTitleName, 
                     plotFileName)
    
    windowSize = 64
    nWindows = 25
    saveWindowFile = "outs/windows.png"
    
    betterSpec = betterSpecAnalyse(x, 
                                   windowSize=windowSize, 
                                   nWindows=nWindows, 
                                   showWindow=False, 
                                   saveWindow=saveWindowFile)
    
    plotTitle = f"log power spectrum after averaging over {nWindows} windows"
    plotFileName = f"outs/betterSpecAnal_{windowSize}.png"
    plotSpecAnalyse(betterSpec, windowSize, plotTitle, plotFileName)