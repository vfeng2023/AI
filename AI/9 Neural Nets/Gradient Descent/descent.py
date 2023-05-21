import numpy as np
import sys
def minimizefunction(func):
    if func == "A":
        def f1(x,y):
            dfdx = 8*x-3*y+24
            dfdy = -3*x+4*y-20
            return dfdx,dfdy
        return f1
    else:
        def f2(x,y):
            dfdx = 2*(x-y*y)
            dfdy = 2*(-2*x*y+2*y*y*y+y-1)
            return dfdx,dfdy
        return f2

def gradientDescent(funct):
    currX = 0
    currY = 0
    vec = [currX,currY]
    if funct == "A":
        descentrate = 0.001 # for A
    else:
        descentrate = 0.01 # for B
    gradient = minimizefunction(funct)
    gradX,gradY = gradient(vec[0],vec[1])
    mag = np.linalg.norm(np.array([gradX,gradY]))
    while mag > 10**(-8):
        
        print("Vector: ",vec,end=", ")
        
        gradX,gradY = gradient(vec[0],vec[1])
        print("gradient: <",gradX,",",gradY,">")
        vec[0] = vec[0]-gradX * descentrate
        vec[1] =vec[1]-gradY * descentrate
        mag = np.linalg.norm(np.array([gradX,gradY]))
whichone = sys.argv[1]
gradientDescent(whichone)