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
# print(perceptron(step,(1,1),-1.5,(1,0)))
myN = int(sys.argv[1])
myW = ast.literal_eval(sys.argv[2])
myB = float(sys.argv[3])

print(check(myN,myW,myB))