
from random import random
import numpy as np
import math
# OLD FUNCTIONS
import ast
import sys
"""
These define the cannonical representation of a boolean function
"""
def cannonicalrep(bits,curr,allreps):
    if len(curr) == bits:
        allreps.append(curr)
        return
    cannonicalrep(bits,curr+(1,),allreps)
    cannonicalrep(bits,curr+(0,),allreps)
    
def truth_table(bits,n):
    """
    Builds the truth table from number of bits and n the canonical integer representation
    returns - list of tuple in form of input_vector,output_state
    """
    allreps = []
    myTT = []
    cannonicalrep(bits,tuple(),allreps)
    for k in range(len(allreps)-1,-1,-1):
        myTT.append((allreps[k],n%2))
        n//=2
    myTT.reverse()
    return myTT
def pretty_print_tt(table):
    print("Input",end="\t "*len(table[0][0]))
    print("Result: ",end="\t\n")
    for combo,val in table:
        for c in combo:
            print(c,end="\t")
        print("\t",val)

# newTable = truth_table(3,128)
# pretty_print_tt(newTable)
"""
Code modeling preceptrons
"""

def step(num):
    if num > 0:
        return 1
    else:
        return 0

def perceptron(A,w,b,x):
    dotproduct = 0
    for k in range(len(x)):
        dotproduct += w[k]*x[k]
    dotproduct += b
    return A(dotproduct)

def check(n,w,b):
    tt = truth_table(len(w),n)
    total = len(tt)
    correct = 0
    for vector,result in tt:
        perOut = perceptron(step,w,b,vector)
        if perOut == result:
            correct += 1
    return correct/total

"""
Part 2 Training perceptrons
"""
def dot(w,x):
    res = 0
    for wval,xval in zip(w,x):
        res += (wval * xval)
    return res


def updateW(w,delta,x):
    newW = tuple()
    for coeff,inp in zip(w,x):
        newW += (coeff + delta * inp,)
    return newW
def train(tt,A,w,b):
    """
    For each value in truth table, updates weight and bias scalars
    """


    for in_vector, value in tt:
        prediction = perceptron(A,w,b,in_vector)
        delta = value - prediction
        w = updateW(w,delta,in_vector)
        b = b + delta
    return w,b


def eval_accuracy(A,w,b,tt):
    total = len(tt)
    correct = 0
    for in_vector,val in tt:
        if perceptron(A,w,b,in_vector) == val:
            correct += 1
    return correct/total

def model_boolean(bits,n):
    currW = tuple(0 for i in range(bits))
    currB = 0
    table = truth_table(bits,n)
    for epoch in range(100):
        newW, newB = train(table,step,currW,currB)
        if currW == newW and currB == newB:
            currW = newW
            currB = newB
            break
        else:
            currW = newW
            currB = newB

    acc = eval_accuracy(step,currW,currB,table)
    return currW,currB,acc


# print(model_boolean(4,32768))
# PART 1 model XOR network

def pnet(inp):
    """
    Input should be a tuple
    basically, go through all the weight vectors, multiply by result, then go to next layer
    output = A()
    XOR HAPPENS HERE
    """
    vectorized_step = np.vectorize(step)
    w1 = np.array([[1,-1],[1,-2]])
    w2 = np.array([[1],[2]])
    weights = [None,w1,w2]
    
    b1 = np.array([0,3])
    b2 = np.array([-2])
    biases = [None,b1,b2]

    curr_result = np.array(inp)
    for layer in range(1,len(biases)):
        result = vectorized_step(curr_result@weights[layer] + biases[layer])
        curr_result = result
    return curr_result

"""
Test part 1
"""
# tt = truth_table(2, 6)
# for input_pair,val in tt:
#     myOutput = pnet(input_pair)[0]
#     print(myOutput==val)
"""
Part 2 pnet
"""
def pnetpt2(x,y,A):
    vectorized_A = np.vectorize(A)
    w1 = np.array([[-1,1,1,-1],[-1,-1,1,1]])
    w2 = np.array([1,2,3,4])
    weight_list = [None,w1,w2]

    blayer1 = np.array([1,1,1,1])
    blayer2 = np.array([-9])
    bias_vectors = [None,blayer1,blayer2]
    curr_result = np.array([x,y])
    for i in range(1,len(weight_list)):
        myResult = vectorized_A(curr_result@weight_list[i] + bias_vectors[i])
        # print(myResult)
        curr_result = myResult

    return curr_result


# generate 10 random points to text

# arr = []
# for k in range(10):
#     x = -1 + random() * 2
#     y = -1 + random() * 2
#     arr.append((x,y))

# arr = [(0.6,0.3)]

# for xval,yval in arr:
#     print(xval,yval,end=", ")
#     print(abs(xval) + abs(yval),end=", ")
#     print(pnetpt2(xval,yval,step)) 
#     print()

"""
Challenge 3: Circle function
"""

def pnetpt3(x,y,A,B1,B2,a):
    vectorized_A = np.vectorize(A)
    w1 = np.array([[-1,1,1,-1],[-1,-1,1,1]])
    w2 = np.array([a,a,a,a])
    weight_list = [None,w1,w2]
    
    blayer1 = np.array([B1,B1,B1,B1])
    blayer2 = np.array([B2])
    bias_vectors = [None,blayer1,blayer2]
    curr_result = np.array([x,y])
    for i in range(1,len(weight_list)):
        myResult = vectorized_A(curr_result@weight_list[i] + bias_vectors[i])
        # print(myResult)
        curr_result = myResult

    return curr_result


# generate 10 random points to text
def sigmoid(num):
    return 1/(1+math.exp(-num))
# arr = []
# for k in range(500):
#     x = -1 + random() * 2
#     y = -1 + random() * 2
#     arr.append((x,y))

# # arr = [(0.6,0.3)]
# correct = 0
# total = 0
# # print(correct/total)
# incorrectpairs = []
# B1 = 1 # between -2 and 2
# step1 = 1
# step2 = 2
# B2 = 9
# for xval,yval in arr:
#     mag = math.sqrt(xval**2 + yval **2)
#     pnetresult = pnetpt3(xval,yval,sigmoid,B1,B2)[0]
#     pnetresult = round(pnetresult)
#     # 1 = inside circle, 0 = outside
#     if (mag < 1 and pnetresult == 1) or (mag > 1 and pnetresult == 0):
#         correct += 1
#         # print(xval,yval)
#     else:
#         incorrectpairs.append((xval,yval))
#         print(tuple(round(j,ndigits=4) for j in (xval,yval)),end=" ")
#         print(pnetresult)
#     total += 1

# print(correct/total)


def optimizeBiases(B1,B2,a):
    arr = []
    for k in range(500):
        x = -1 + random() * 2
        y = -1 + random() * 2
        arr.append((x,y))

    # arr = [(0.6,0.3)]
    correct = 0
    total = 0
    # print(correct/total)
    incorrectpairs = []
    for xval,yval in arr:
        mag = math.sqrt(xval**2 + yval **2)
        pnetresult = pnetpt3(xval,yval,sigmoid,B1,B2,a)[0]
        pnetresult = round(pnetresult)
        # 1 = inside circle, 0 = outside
        if (mag < 1 and pnetresult == 1) or (mag > 1 and pnetresult == 0):
            correct += 1
            # print(xval,yval)
        else:
            incorrectpairs.append((xval,yval))
            print(tuple(round(j,ndigits=4) for j in (xval,yval)),end=" ")
            print(pnetresult)
        total += 1

    return correct/total

B1 = 2**0.5 # 0 - 4
# B2 = -4 # -4 - 0
# pairs of B1, and B2
prs = []
prs.sort(key=lambda a:a[1])
B2 = -3
# while B1 <= 4:

# for pr in prs:
#     print(pr, end=" ")
#     print(optimizeBiases(pr[0],pr[1]))


# change the weights on the and vector
#0.9853 for a appears to do the trick
# for a in range(9800,9900):
#     a = a/10000
#     print(a,end=" ")
#     print(optimizeBiases(B1,B2,a))
args = sys.argv[1:]
if len(args) == 1:
    tup = ast.literal_eval(args[0])
    print(pnet(tup)[0])
elif len(args) == 2:
    x = float(args[0])
    y = float(args[1])
    result = pnetpt2(x,y,step)[0]
    if result > 0:
        print("inside")
    else:
        print("outside")
else:
    print("Percent correct: ",optimizeBiases(B1,B2,0.9853)*100,"%")