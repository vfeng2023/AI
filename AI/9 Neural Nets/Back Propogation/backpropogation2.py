from calendar import EPOCH
import numpy as np
import sys
import math
from collections import deque


def error(actual,predicted):
    return 0.5*(np.linalg.norm(predicted-actual))**2
def sigmoid(x):
    return 1/(1+math.exp(-x))
def diff_sigmoid(x):
    val = sigmoid(x)
    return val * (1-val)
vectorized_sig = np.vectorize(sigmoid)
vectorized_diff = np.vectorize(diff_sigmoid)
def eval_network():
    w1 = np.array([[1,-.5],[1,.5]])
    w2 = np.array([[1,2],[-1,-2]])

    Weighs = [None,w1,w2]

    b1 = np.array([[1,-1]])
    b2 = np.array([[-0.5,0.5]])
    biases = [None,b1,b2]

    inputLayer = np.array([[2,3]])
    train_set = [(np.array([[2,3]]),np.array([[0.8,1]]))]
    learn_rate = 0.1
    for epoch in range(2):
        
        
        for invector,out in train_set:
            dotProducts = [None]
            layerOutputs = [invector]
            for i in range(1,len(Weighs)):
                dot = layerOutputs[-1]@Weighs[i] + biases[i]
                myOut = vectorized_sig(dot)
                dotProducts.append(dot)
                layerOutputs.append(myOut)
                # prevLayer = myOut
            calc_eror = error(out,layerOutputs[-1])

            print("Epoch ",epoch,", error=",calc_eror)
            print("out",layerOutputs)
            # evaluate the delta N
            deltaN = vectorized_diff(dotProducts[-1]) *(out-layerOutputs[-1])
            deltaLayers = [deltaN]
            print("Dot products:",dotProducts)

            for layer in range(len(Weighs)-2,0,-1):
                deltaL = vectorized_diff(dotProducts[layer]) * (deltaLayers[-1]@Weighs[layer+1].transpose())
                deltaLayers.append(deltaL)
            deltaLayers.append(None)
            deltaLayers.reverse()
            print(len(deltaLayers))
            print(deltaLayers)
            for L in range(1,len(Weighs)):
                biases[L] = biases[L] + learn_rate * deltaLayers[L]
                Weighs[L] = Weighs[L] + learn_rate*(layerOutputs[L-1].transpose() @ deltaLayers[L])
        # calc_eror = error(out,layerOutputs[-1])
        # print("Epoch ",epoch,", error=",calc_eror)

# print(diff_sigmoid(0.1))
def evalInput(inputvector,Weighs,biases):
    invector = inputvector
    # print(invector)
    # print(out)
    # input()
    dotProducts = [None]
    layerOutputs = [invector]
    for i in range(1,len(Weighs)):
        dot = layerOutputs[-1]@Weighs[i] + biases[i]
        myOut = vectorized_sig(dot)
        dotProducts.append(dot)
        layerOutputs.append(myOut)
    return layerOutputs[-1]
def eval_networkpt2():
    w1 = -1+2*np.random.rand(2,2)
    w2 = -1 + 2 * np.random.rand(2,2)

    Weighs = [None,w1,w2]

    b1 = np.random.rand(1,2)
    # print(b1)
    # input()
    b2 = np.random.rand(1,2)
    biases = [None,b1,b2]

    inputLayer = np.array([[2,3]])
    train_set = {
        (0,0):(0,0),
        (0,1):(0,1),
        (1,0):(0,1),
        (1,1):(1,0)
    }
    learn_rate = 10
    for epoch in range(100):
        
        
        for inp in train_set:
            # out = train_set[inp]
            invector = np.array([inp])
            out = np.array([train_set[inp]])
            # print(invector)
            # print(out)
            # input()
            dotProducts = [None]
            layerOutputs = [invector]
            for i in range(1,len(Weighs)):
                dot = layerOutputs[-1]@Weighs[i] + biases[i]
                myOut = vectorized_sig(dot)
                dotProducts.append(dot)
                layerOutputs.append(myOut)
                # prevLayer = myOut
            calc_eror = error(out,layerOutputs[-1])

            # print("Epoch ",epoch,", error=",calc_eror)
            # print("out",layerOutputs)
            # evaluate the delta N
            deltaN = vectorized_diff(dotProducts[-1]) *(out-layerOutputs[-1])
            deltaLayers = [deltaN]
            # print("Dot products:",dotProducts)

            for layer in range(len(Weighs)-2,0,-1):
                deltaL = vectorized_diff(dotProducts[layer]) * (deltaLayers[-1]@Weighs[layer+1].transpose())
                deltaLayers.append(deltaL)
            deltaLayers.append(None)
            deltaLayers.reverse()
            # print(len(deltaLayers))
            # print(deltaLayers)
            for L in range(1,len(Weighs)):
                biases[L] = biases[L] + learn_rate * deltaLayers[L]
                Weighs[L] = Weighs[L] + learn_rate*(layerOutputs[L-1].transpose() @ deltaLayers[L])
            print("Epoch",epoch,", input: ",inp,"result: ",layerOutputs[-1])
        print()
    print("Training results")
    for t in train_set:
        t = np.array([t])
        result = evalInput(t,Weighs,biases)
        result[0][0] = round(result[0][0])
        result[0][1] = round(result[0][1])
        print("Input: ",t)
        print("Result: ",result)
        print()

def evalnetworkcircle():
    w1 = -1+2*np.random.rand(2,12)
    # print(w1.shape)
    # input()
    w2 = -1 +2* np.random.rand(12,4)
    # print(w2.shape)
    # input()
    w3=-1+2*np.random.rand(4,1)
    # print(w3.shape)
    # input()
    Weighs = [None,w1,w2,w3]

    b1 = -1+2*np.random.rand(1,12)
    # print(b1.shape)
    # input()
    b2 = -1+2*np.random.rand(1,4)
    # print (b2.shape)
    b3 = -1 + 2*np.random.rand(1,1)
    # print(b3.shape)
    # input()
    biases = [None,b1,b2,b3]
    train_set = list()
    with open("10000_pairs.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            coords = line.split()
            x = float(coords[0])
            y = float(coords[1])
            if math.sqrt(x**2 + y**2) < 1:
                result = 1 # inside the circle results in 1
            else:
                result = 0 # outside the circle results in 0
            train_set.append(((x,y),result))
    # print(train_set)
    learn_rate = 0.1
    # print(len(train_set))
    # input()
    for epoch in range(500):        
        # print(len(train_set))
        # input()
        for inp,value in train_set:
            # out = train_set[inp]
            invector = np.array([inp])
            out = np.array([[value]])
            # print("invector",invector)
            
            # print(invector)
            # print(out)
            # input()
            dotProducts = [None]
            layerOutputs = [invector]
            for i in range(1,len(Weighs)):
                dot = layerOutputs[-1]@Weighs[i] + biases[i]
                #print("Size of dot product: ",dot.shape)
                # input()
                myOut = vectorized_sig(dot)
                dotProducts.append(dot)
                layerOutputs.append(myOut)
                # prevLayer = myOut
            # for L in range(0,len(layerOutputs)):
                #print(layerOutputs[L].shape)
            # input()
            # print("out should have dimension of :",out.shape)
            calc_eror = error(out,layerOutputs[-1])
            # print("layerOutputs",layerOutputs)
            # input()

            # print("Epoch ",epoch,", error=",calc_eror)
            # print("out",layerOutputs)
            # evaluate the delta N
            deltaN = vectorized_diff(dotProducts[-1]) *(out-layerOutputs[-1])
            # print("size of delta N:", deltaN.shape)
            # input()
            deltaLayers = [deltaN]
            # print("Dot products:",dotProducts)

            for layer in range(len(Weighs)-2,0,-1):
                deltaL = vectorized_diff(dotProducts[layer]) * (deltaLayers[-1]@Weighs[layer+1].transpose())
                # print(vectorized_diff(dotProducts[layer]))
                deltaLayers.append(deltaL)
            deltaLayers.append(None)
            deltaLayers.reverse()
            # print(deltaLayers)
            # print(len(deltaLayers))
            # print(deltaLayers)
            # print("delta layers: ",deltaLayers)
            # input()
            # print("weights: ",Weighs)
            # print("biases: ",biases)
            # print("Check bias vector dimension shapes and weights: ")
            for L in range(1,len(Weighs)):
                biases[L] = biases[L] + learn_rate * deltaLayers[L]
                # print(biases[L].shape, deltaLayers[L].shape)
                
                # print(layerOutputs[-1].transpose())
                # input()
                Weighs[L] = Weighs[L] + learn_rate*(layerOutputs[L-1].transpose() @ deltaLayers[L])
                # print(Weighs[L].shape,(layerOutputs[L-1].transpose() @ deltaLayers[L]).shape)
                # input()
            # print("weights: ",Weighs)
            # print("biases: ",biases)
        
        # go through training set and classify again
        correct = 0
        
        # print("incorrectly classified points, epoch ",epoch,":")
        for point,loc in train_set:
            inputVector = np.array([point])
            result = evalInput(inputVector,Weighs,biases)
            result = round(result[0][0])
            if result == loc:
                correct += 1
            else:
                pass
                # print(point)
        learn_rate = learn_rate * 0.98
        print(epoch,": ",correct/len(train_set),len(train_set)-correct)
        # input()
# eval_networkpt2()
# evalnetworkcircle()
# def evaluate_circletake2(architechture):
#     train_set = list()
#     with open("10000_pairs.txt") as f:
#         lines = [line.strip() for line in f.readlines()]
#         for line in lines:
#             coords = line.split()
#             x = float(coords[0])
#             y = float(coords[1])
#             if math.sqrt(x**2 + y**2) < 1:
#                 result = 1 # inside the circle results in 1
#             else:
#                 result = 0 # outside the circle results in 0
#             train_set.append(((x,y),result))
#     # print(train_set)
#     # generate neural netw
#     weights = [None]
#     for i in range(len(architechture)-1):
#         weightsArray = -1+ 2*np.random.rand(architechture[i],architechture[i+1])
#     biases = [None]
#     for j in range(1,len(architechture)):
#         biases.append(-1+2*np.random.rand(1,architechture[j]))
#     EPOCHS = 100
#     for k in range(EPOCHS):
#         for inputpair,output in train_set:
#             # make inputpair and output into 2D arrays
#             invector = np.array([inputpair])
#             outvalue = np.array([[output]])
#             layerDotProducts = [None] # dot
#             layerOutputs = [invector] # "a"
#             for l1 in range(1,len(weights)):
#                 dot = (layerDotProducts[l1-1]@weights[l1]) + biases[l1]
#                 myOut = vectorized_diff(dot) # results for this layer
#                 layerOutputs.append(myOut)
#             # delta N is pairwise multiplication of last value and actual value - layer Out
#             deltaN = vectorized_diff(layerDotProducts[-1]) * (outvalue-layerOutputs[-1])
#             deltaout = 4
choice = sys.argv[1]
if choice == "S":
    eval_networkpt2()
else:
    evalnetworkcircle()