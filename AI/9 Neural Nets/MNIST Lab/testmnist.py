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
for pixelMatrix,numberMatrix in testing_set:
    result = evalInput(pixelMatrix,weights,biases)
    prediction = get_Value(result)
    actual = get_Value(numberMatrix)
    if prediction == actual:
        correct += 1
    else: 
        print("Predicted: ",prediction, "actual ",actual)
    total += 1
        


print("Testing results on ", len(testing_set) ," accuracy of ", correct/len(testing_set))




