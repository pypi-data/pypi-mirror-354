import sys
import os
import pickle as pk
import time

from .drawings import *
from .scores import *
from .utils import *
from .algorithm import *


__version__ = "2.6.1"
version = "2.6.1"
bar_color1 = 'darkturquoise'

def love():
    """
    A simple demo.
    """
    x = np.hstack([np.linspace(-1,-0.99,10),np.linspace(-0.99,0.99,100),np.linspace(0.99,1,10)])

    y1 = np.sqrt(1-x**2)+np.abs(x)
    plt.plot(x,y1,color='r',linestyle='--',linewidth=2)

    y2 = -np.sqrt(1-x**2)+np.abs(x)
    plt.plot(x,y2,color='r',linestyle='--',linewidth=2)
    plt.fill_between(x, y1, y2, facecolor='pink')
    plt.title(r'$y=\left|x\right| \pm \sqrt{1-x^2}$')
    plt.show()

def demo(show=True):
    """
    A simle demo for a China map
    """
    m = map()
    m.load("china", facecolor='red', linewidth=0.9)
    if show:
        m.show()
    return m

    
