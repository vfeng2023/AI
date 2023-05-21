
import numpy as np
import pickle
with open("mnist_test.csv") as f:
    # generates a nested list of tuple with the normalized pixels and reference to the  and reference to correct number
    training_set = [] # [(list reference, correct number)]
    lines = [line for line in f.readlines()]
    for dataline in lines:
        vals = dataline.split(",")
        number = int(vals[0])
        pixels = vals[1:]
        for index,pixVal in enumerate(pixels):
            pixels[index] = int(pixVal)/255
        pixMatrix = np.array([pixels])
        
        numberMatrix = np.zeros((1,10))
        numberMatrix[0][number] = 1
        training_set.append((pixMatrix,numberMatrix))

# save training set:
with open("testset.pkl","wb") as f:
    pickle.dump(training_set,f)
    f.close()
for k in range(3):
    print(training_set[k][0].shape,training_set[k][1].shape)
        
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

weights,biases = initializeWeights([784,300,100,10])
# for w in weights:
#     if w is not None:
#         print(w.shape)
#     else:
#         print(None)
# for b in biases:
#     if b is not None:
#         print(b.shape)
# with open ("trainset.pkl","rb") as f:
#     vals = pickle.load(f)
#     for k in range(10):
#        v1 = vals[k][0]
#        v2 = vals[k][1]
#        print(v1.shape,v2.shape)
#        print(v1,v2)
#        print()