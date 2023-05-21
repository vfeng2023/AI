
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
    """
    Removed epoch count and validation, only runs one epoch on given weights and biases
    """
    
    # weight_sizes = [w.shape if w is not None else (0,0) for w in weights]
    # bias_shapes = [bias.shape if bias is not None else (0,0) for bias in biases]
    # print(weight_sizes,bias_shapes)
    learning_rate = 0.1
    print("Starting")
    
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
    return wb
        # with open("savedcoeff.pkl","wb") as f:
        #     pickle.dump(wb,f)
        # print("Finished training epoch", epoch," trained on ",len(train_set))

# for pairwise comparisons
# step 1 generate all possible pairs
poss_pairs = []
for i in range(10):
    for j in range(i+1,10):
        poss_pairs.append((i,j))

with open ("pairwisetrainset.pkl","rb") as f:
    training_dict = pickle.load(f)
# step 2: get the training subsets (items in test set broken down by pair) 
pair_sets = dict()
for pair in poss_pairs:
    cat0, cat1 = pair
    myTrainSet = []  # [(image, label)]
    for imgzero in training_dict[cat0]:
        result = np.array([[0]])
        myTrainSet.append((imgzero,result))
    for imgone in training_dict[cat1]:
        result = np.array([[1]])
        myTrainSet.append((imgone,result))
    pair_sets[pair] = myTrainSet
    print(myTrainSet)
    input()
# pair_sets correspond to the different pairwise comparison groupings. The order is VERY important. 0 = first num, 1 is second number

    
    
    
    
# step 3: iterate through all the training subsets to train the pairwise comparison neural nets
    # architechture - [784, 1] for each pairwise comparison with sigmoidal activation function
    # to keep labels simple, outputs are between 0 and 1 - each pair is arbitarily assigned a number
prwiseWeights = dict() # dictionary corresponding to weights and biases
for epoch in range(10): # start with 10 epochs
    for pr in pair_sets:
        if pr not in prwiseWeights:
            weights,biases = initializeWeights([784,1])
            weights,biases = backpropogate(pair_sets[pr],weights,biases)
            prwiseWeights[pr] = (weights,biases)
        else:
            weights,biases = prwiseWeights[pr]
            weights,biases = backpropogate(pair_sets[pr],weights,biases)
            prwiseWeights[pr] = (weights,biases)
        print("Finished training pair" ,pr)
    print("END OF EPOCH ",epoch)
    with open('prwisewieghts.pkl','wb') as f:
        pickle.dump(prwiseWeights,f)
        # stored as a dictionary of pair tuple: wb tuple
        f.close()

# TODO:
    # alter the way data is stored by grouping together all data images with a common label together
    # main storage structures - dictionary of labels to images, dictionary of pairs to weights and biases
# with open ('mnist_train.csv','r') as f:
#     training_dict = {} # [number:list of instances in training set]
#     lines = [line for line in f.readlines()]
#     for dataline in lines:
#         vals = dataline.split(",")
#         number = int(vals[0])
#         pixels = vals[1:]
#         for index,pixVal in enumerate(pixels):
#             pixels[index] = int(pixVal)/255
#         pixMatrix = np.array([pixels])
#         if number in training_dict:
#             training_dict[number].append(pixMatrix)
#         else:
#             training_dict[number] = [pixMatrix]

# with open("pairwisetrainset.pkl","wb") as f1:
#     pickle.dump(training_dict,f1)
#     f1.close()

        
