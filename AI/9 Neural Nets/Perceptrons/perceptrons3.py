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

    
# BITS = int(sys.argv[1])
# N = int(sys.argv[2])
# W,B,acc = model_boolean(BITS,N)
# print("Modeled with weight vector {0} and bias scalar {1} and accuracy {2}.".format(W,B,acc))
# numFunc = 2 ** (2**BITS)
# modeled = 0

# for n in range(numFunc):
#     weight,bias, acc = model_boolean(BITS,n)
#     if abs(acc - 1) < 0.0000000001:
#         modeled += 1

# print("For {0} bits, {1} out of {2} total can be modeled correctly".format(BITS,modeled,numFunc))

def xorfunct(input_tuple):
    """
    XOR HAPPENS HERE
    """
    in1,in2 = input_tuple
    p3out = perceptron(step,(1,1),0,(in1,in2))
    p4out = perceptron(step,(-1,-2),3,(in1,in2))
    p5out = perceptron(step,(1,2),-2,(p3out,p4out))
    return p5out

# testing the xor funtion
def check_one(tt,funct):
    count = 0
    for val,actual in tt:
        result = funct(val)
        if result == actual:
            count += 1
    return count/len(tt)

myinput = sys.argv[1]
test_val = ast.literal_eval(myinput)
print(xorfunct(test_val))