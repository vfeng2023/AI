import pickle
import numpy as np
import math
def initializeWeights(networkstruct):
    weights = [None]
    for k in range(len(networkstruct)-1):
        newWeight =-1+2*np.random.rand(networkstruct[k],networkstruct[k+1])
        weights.append(newWeight)
    biases = [None]
    for k in range(1,len(networkstruct)):
        newBias = -1 * 2 * np.random.rand(1,networkstruct[k])
        biases.append(newBias)

    return weights,biases

# weights,biases = initializeWeights([2,4,1])
def saveweights(weights,biases):
    filename = "weights_biases.pkl"# input("Save weights and biases to: ")
    with open(filename,"wb") as f:
        pickle.dump((weights,biases),f)
        f.close()
def get_weights(filename):
    """returns weights, biases in that order"""
    with open(filename,"rb") as f:
        w,b = pickle.load(f)
    return w,b
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
"""Old code """
# def sigmoid(x):
#     return 1/(1+math.exp(-x))
# def derivsigmoid(x):
#     val = sigmoid(x)
#     return val * (1-val)
# vectorized_sigmoid = np.vectorize(sigmoid)
# vectorized_deriv = np.vectorize(derivsigmoid)
# def backpropogate(train_set):
#     EPOCHS = 100

#     weights,biases = initializeWeights([784,300,100,10])
#     learning_rate = 0.1
#     for epoch in range(EPOCHS):
#         for pixelMatrix,output in train_set:
#             invector = pixelMatrix
#             dotProducts = [None]
#             layerOutputs = [invector]
#             for L in range(1,len(weights)):
#                 dot = layerOutputs(L-1) @ weights[L] + biases[L]
#                 dotProducts.append(dot)
#                 layerOut = vectorized_sigmoid(dot)
#                 layerOutputs.append(layerOut)
#             difference = layerOut[-1] - output
#             deltaN = vectorized_deriv(dotProducts[-1]) * difference
#             deltaLayers = [deltaN]
#             for layer in range(len(weights)-2,0,-1):
#                 deltaL = vectorized_deriv(dotProducts[layer])*(deltaLayers[-1] * weights[layer+1].transpose())
#                 deltaLayers.append(deltaL)
#             for coefflayer in range(1, len(weights)):
#                 biases[coefflayer] = biases[coefflayer] + learning_rate* deltaLayers[coefflayer]
#                 weights[coefflayer] = weights[coefflayer] + learning_rate *(layerOut[layer-1].transpose()@deltaLayers[coefflayer])
#         learning_rate = learning_rate * 0.998
#         saveweights()
"""Algorithm testing"""
def sigmoid(x):
    return 1/(1+math.exp(-x))
def derivsigmoid(x):
    val = sigmoid(x)
    return val * (1-val)
vectorized_sigmoid = np.vectorize(sigmoid)
vectorized_deriv = np.vectorize(derivsigmoid)
def initializeWeights(networkstruct):
    weights = [None]
    for k in range(0,len(networkstruct)-1):
        newWeight =-1+2*np.random.rand(networkstruct[k],networkstruct[k+1])
        weights.append(newWeight)
    biases = [None]
    for k in range(1,len(networkstruct)):
        newBias = -1 * 2 * np.random.rand(1,networkstruct[k])
        biases.append(newBias)

    return weights,biases
def backpropogate(train_set,weights,biases):
    EPOCHS = 100

    
    weight_sizes = [w.shape if w is not None else (0,0) for w in weights]
    bias_shapes = [bias.shape if bias is not None else (0,0) for bias in biases]
    print(weight_sizes,bias_shapes)
    learning_rate = 0.1
    print("Starting")
    
    for epoch in range(EPOCHS):
        count = 0
        for pixelMatrix,output in train_set:
            invector = pixelMatrix
            dotProducts = [None]
            layerOutputs = [invector]
            for L in range(1,len(weights)):
                dot = layerOutputs[L-1] @ weights[L] + biases[L]
                dotProducts.append(dot)
                layerOut = vectorized_sigmoid(dot)
                layerOutputs.append(layerOut)
            difference = output-layerOutputs[-1]
            deltaN = vectorized_deriv(dotProducts[-1]) * difference
            deltaLayers = [deltaN]
            for layer in range(len(weights)-2,0,-1):
                deltaL = vectorized_deriv(dotProducts[layer])*(deltaLayers[-1] @ weights[layer+1].transpose())
                deltaLayers.append(deltaL)
            deltaLayerssizes= [w.shape if w is not None else None for w in deltaLayers]
            
            deltaLayers.append(None)
            deltaLayers.reverse()
            deltaLayerssizes= [w.shape if w is not None else None for w in deltaLayers]
            # print("Delta layer sizes: ",deltaLayerssizes)
            # coefflayerzies = [w.shape if w is not None else None for w in layerOutputs]
            for coefflayer in range(1, len(weights)):
                biases[coefflayer] = biases[coefflayer] + learning_rate* deltaLayers[coefflayer]

                weights[coefflayer] = weights[coefflayer] + learning_rate *(layerOutputs[coefflayer-1].transpose()@deltaLayers[coefflayer])
            count += 1
            if count%10000 == 0:
                print("Trained ",count)
        learning_rate = learning_rate * 0.998
        wb = (weights,biases)
        with open("savedcoeff.pkl","wb") as f:
            pickle.dump(wb,f)
        print("Finished training epoch", epoch," trained on ",len(train_set))

        # correct = 0
        # for t,out in train_set:
        #     res = evalInput(t,weights,biases)
        #     # print(res)
        #     # input()
        #     res[0][0] = round(res[0][0])
        #     if res[0][0] == out[0][0]:

        #         correct += 1
        # total = len(train_set)
        # print(epoch,": ",correct/total,total-correct)
            


# with open("10000_pairs.txt") as f:
#         train_set = []
#         lines = [line.strip() for line in f.readlines()]
#         for line in lines:
#             coords = line.split()
#             x = float(coords[0])
#             y = float(coords[1])
#             if math.sqrt(x**2 + y**2) < 1:
#                 result = 1 # inside the circle results in 1
#             else:
#                 result = 0 # outside the circle results in 0
#             v1 = np.array([[x,y]])
#             v2 = np.array([[result]])
#             train_set.append((v1,v2))
with open("trainset.pkl","rb") as f:
    train_set = pickle.load(f)
initweights,initbiases = initializeWeights([784,300,100,10])
backpropogate(train_set,initweights,initbiases)

