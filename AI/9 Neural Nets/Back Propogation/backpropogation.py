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
    learn_rate = 1
    for epoch in range(600):
        
        
        for inp,val in train_set:
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
        result = evalInput(t,Weighs,biases)
        result[0][0] = round(result[0][0])
        result[0][1] = round(result[0][1])
        print("Input: ",t)
        print("Result: ",result)
        print()

def evalnetworkcircle():
    w1 = -1+2*np.random.rand(2,12)
    w2 = -1 +2* np.random.rand(12,4)
    w3=-1+2*np.random.rand(4,1)

    Weighs = [None,w1,w2,w3]

    b1 = -1+2*np.random.rand(1,12)
    # print(b1)
    # input()
    b2 = -1+2*np.random.rand(1,4)
    b3 = -1 +2*np.random.rand(1,1)
    biases = [None,b1,b2,b3]
    train_set = []
    for k in range(10):
        x = -1+2*np.random.rand()
        y = -1 + 2 * np.random.rand()
        result = 0 if x*x + y*y >=1 else 1
        train_set.append(((x,y),result))
    learn_rate = 1
    for epoch in range(600):
        
        
        for inp in train_set:
            # out = train_set[inp]
            in1,out = inp
            invector = np.array(list(in1))
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


        # go through training set and classify again
        correct = 0
        # print(Weighs)
        # print(biases)
        print("incorrectly classified points, epoch ",epoch,":")
        for point,loc in train_set:
            result = evalInput(point,Weighs,biases)
            result = round(result[0][0])
            if output == loc:
                correct += 1
            else:
                print(point)
        print("percentarge: ",correct/len(train_set)*100)
        # input()
evalnetworkcircle()
            

            

