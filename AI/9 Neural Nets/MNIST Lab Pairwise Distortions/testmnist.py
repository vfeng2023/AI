import pickle
import math
import numpy as np
with open("testset.pkl","rb") as f:
    testing_set = pickle.load(f)

with open("savedcoeff.pkl","rb") as f1:
    weights,biases = pickle.load(f1)

def evalInput(inputvector,Weighs,biases):
    invector = inputvector
    # print(invector)
    # print(out)
    # input()
    dotProducts = [None]
    layerOutputs = [invector]
    for i in range(1,len(Weighs)):
        dot = layerOutputs[-1]@Weighs[i] + biases[i]
        myOut = vectorized_sigmoid(dot)
        dotProducts.append(dot)
        layerOutputs.append(myOut)
    return layerOutputs[-1]
def sigmoid(x):
    return 1/(1+math.exp(-x))
def get_Value(array):
    maxVal = 0
    for i in range(len(array[0])):
        if array[0][i] > array[0][maxVal]:
            maxVal = i
    return maxVal
vectorized_sigmoid = np.vectorize(sigmoid)
correct = 0
total = 0

with open('prwisewieghts.pkl',"rb") as f:
    networks = pickle.load(f)
    f.close()
def maxIndex(array):
    maxIndex = 0
    for i in range(len(array)):
        if array[i] > array[maxIndex]:
            maxIndex = i
    return maxIndex
correct = 0
for pixelMatrix,number in testing_set:
    numPredictions = [0 for i in range(10)]
    for pr in networks:
        cat0,cat1 = pr
        weights,biases = networks[pr]
        result = evalInput(pixelMatrix,weights,biases)
        integerresult = int(result[0][0]+0.5)
        numPredictions[pr[integerresult]] += 1
    pred = maxIndex(numPredictions)
    if number == pred:
        correct += 1

        


print("Testing results on ", len(testing_set) ," accuracy of ", correct/len(testing_set))




