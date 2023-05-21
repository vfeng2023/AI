import math
import numpy as np
import sys
def eval_function(func):
    """
    FUnctions which is being asked to be evaluated
    """
    if func == "A":
        def f1(x,y):
            return 4*x*x - 3*x*y + 2*y*y + 24*x -20*y
        return f1
    else:
        def f2(x,y):
            return (1-y) * (1-y) + (x-y*y)*(x-y*y)
        return f2
def minimizefunction(func):
    """
    Returns a reference to a function that will evaluate gradient at (x,y)
    """
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

"""Red extension"""
def one_d_minimize(f,left,right,tolerance):
    """
    Finds x,y loc for function f which will produce minimum value
    """
    if right-left < tolerance:
        return left

    else:
        dist = right-left
        newLeft = left + dist/3
        newRight = right - dist/3
        funcAtNewLeft = f(newLeft)
        funcAtNewRight = f(newRight)
        if funcAtNewLeft > funcAtNewRight:
            return one_d_minimize(f,newLeft,right,tolerance)
        else:
            return one_d_minimize(f,left,newRight,tolerance)
# def funct(x):
#     return math.sin(x) + math.sin(3*x) + math.sin(4*x)

# result = one_d_minimize(funct,-1,0,10**-8)
def eval_on_grad(x0,y0,gradX,gradY,funct):
    """
    Returns a function which evaluates the gradient extension line at distance l in direction of gradient from x0,y0
    """
    def make_funct(l):
        newX = x0-l*gradX
        newY = y0-l*gradY
        return funct(newX,newY)
    return make_funct

def gradientDescent(funct):
    """
    Funct refers to the letter A or B
    """
    currX = 0
    currY = 0
    vec = [currX,currY]
    # initial gradient value
    gradient = minimizefunction(funct)
    gradX,gradY = gradient(vec[0],vec[1])
    mag = np.linalg.norm(np.array([gradX,gradY]))
    while mag > 10**(-8):
        
        print("Vector: ",vec,end=", ")
        # gradient
        gradX,gradY = gradient(vec[0],vec[1])
        print("gradient: <",gradX,",",gradY,">")
        # gets the specified function
        myFunction = eval_function(funct)
        # returns a customized function which evaluates along line going through x0,y0 in direction of gradient
        optFunct = eval_on_grad(vec[0],vec[1],gradX,gradY,myFunction)
        # minimizes using above function (NOTE: subtracting lambda because rate of greatest descent)
        descentrate = one_d_minimize(optFunct,0,1,10**-8)

        # adds the optimal descent rate to vectors
        vec[0] = vec[0]-gradX * descentrate
        vec[1] =vec[1]-gradY * descentrate
        # calculates magnitude of the vector
        mag = np.linalg.norm(np.array([gradX,gradY]))
# functionToMin = minimizefunction("A")
whichone = sys.argv[1]
gradientDescent(whichone)
