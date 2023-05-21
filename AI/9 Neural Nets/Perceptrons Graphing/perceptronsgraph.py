import ast
import sys
import matplotlib.pyplot as plt
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

plt.xlim(-2,2)
plt.ylim(-2,2)
plt.grid()
BITS = 2
totalfunc = 2 ** (2**BITS)
for i in range(totalfunc):
    w,b,acc = model_boolean(BITS,i)
    tt = truth_table(BITS,i)
    plt.title("Boolean function number {num}".format(num=i))
    # plt.clf()
    # create the points map
    xstart = -2
    while xstart < 2:
        ystart = -2
        while ystart < 2:
            val = perceptron(step,w,b,(xstart,ystart))
            ystart += 0.1
            if val > 0:
                plt.plot([xstart],[ystart],marker="o",markersize=1,markerfacecolor="green",markeredgecolor="green")
            else:
                plt.plot([xstart],[ystart],marker="o",markersize=1,markerfacecolor="red",markeredgecolor="red")
        xstart += 0.1


    # create the truth table value map
    for inp,val in tt:
        in1,in2 = inp
        if val > 0:
            plt.plot([in1],[in2],marker="o",markersize=5,markerfacecolor="green",markeredgecolor="black")
        else:
            plt.plot([in1],[in2],marker="o",markersize=5,markerfacecolor="red",markeredgecolor="black")
    print("Here")
    plt.show()
