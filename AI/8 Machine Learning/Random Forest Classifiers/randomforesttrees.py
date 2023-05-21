import matplotlib.pyplot as plt
import random
import sys
import math
# sys.argv = ["junk","connect-four.csv","7000","5000","60000","5000"]
def plot_data(X_vals,Y_vals,Yrand2,xlabels,ylabels):
    # X_vals = [random.random()*100 for i in range(100)]
    # Y_vals = [random.random()*100 for i in range(100)]
    normal = plt.scatter(X_vals,Y_vals,label="Normal")
    randForest = plt.scatter(X_vals,Yrand2,label="Random Forest Classifier")
    # classes = ["Normal","Random Forest Classifiers"]
    plt.legend((normal,randForest),("Normal","Random Forest Classifiers"))
    plt.xlabel(xlabels)
    plt.ylabel(ylabels)
    plt.show()
def calculate_entropy(featureIndex,featureList):
    count = dict()

    # count the values present
    # print(featureList)
    for k in range(len(featureList)):
        if (feature_value:=featureList[k][featureIndex]) not in count:
            count[featureList[k][featureIndex]] = dict()
        if featureList[k][-1] not in count[feature_value]:
            count[feature_value][featureList[k][-1]] = 0
        count[feature_value][featureList[k][-1]] += 1
    # get the percentages

    expected_entrophy = 0
    for c in count:
        # calculate the probability of getting the feature, the entropy of the dataset associated with the feature itself, add -log * value to those
        sub_total = 0
        myEntrophy = 0
        # print(c)
        # print("\n",count[c])
        # input()
        for val in count[c]:
            sub_total += count[c][val]
        for val in count[c]:
            myEntrophy += (-math.log2(count[c][val]/sub_total)) * count[c][val]/sub_total
        # print("myEntrophy",myEntrophy)
        expected_entrophy += (sub_total/len(featureList) * myEntrophy)
    return expected_entrophy

def initEntrophy(valueList):
    count = dict()
    for v in valueList:
        # print(valueList)
        # input()
        if v[-1] not in count:
            count[v[-1]] = 0
        count[v[-1]] += 1
    entrophy = 0
    for k in count:
        entrophy += (-1*count[k]/len(valueList) * math.log2(count[k]/len(valueList)))
    return entrophy
# store the values in play_tennis as a list of values
# filename = sys.argv[1]
# with open(filename) as f:
#     lines = [line.strip() for line in f.readlines()]
#     # print("Features: ",lines[0])
#     featureNames = [varName + "?" for varName in lines[0].split(",")]
#     featureList = []
#     result_values = []
#     for line in lines[1:]:
#         line = line.split(",")
#         featureList.append(line)
#         result_values.append(line[-1])

# start_ent = initEntrophy(result_values)
# print(start_ent)
# for f in range(len(featureNames)-1):
#     print("feature: ",featureNames[f],end="\t")
#     feature_entrophy = calculate_entropy(f,featureList,result_values)
#     print("Entrophy change: ", (start_ent-feature_entrophy),end="\n")
tree = dict()
def build_trees(feature_list,tree,feature_names):
    """
    1.  Consider each feature in turn.  Find the information gain from differentiating based on that feature.
    - feature list is the feature values associated with a particular feature,
    -  featureNames is the name of the feature
    - otherwise, identification is done on index   
    2.  Choose the feature with the highest information gain. 
    3.  Split the dataset into smaller datasets based on the possible values of the chosen feature. 
    4.  If any of the resulting datasets has an entropy of 0, then it is a leaf. 
    5.  Otherwise, recur on any smaller dataset with an entropy > 0.
    returns the tree
    """
    # the item PASSED is the tree
    # start with the initial list of features and values
    # calculate the initial entrophy
    initialEntro = initEntrophy(feature_list)
    # print()
    # if the initial entrophy is 0, then to the tree dict, add the title of the last column and result
    if abs(initialEntro - 0) < 0.000000000001:
        # tree[feature_names[-1]]=feature_list[0][-1] # assign the last value
        return feature_list[0][-1]
    

    # calculate the entrophy gain for each given feature by index
    splitBy,bestGain = splitPointFeature(feature_list,initialEntro,feature_names)
    
    # if splitBy is None:
    #     # aka best entrophy gain is 0, randomly select an outcome
    #     item = random.choice(feature_list)[-1]
    #     return item



    subsets = split_data(feature_list,splitBy)
    # once decided the feature(index) which will give the largest information gain, 
        # add the name of the feature to TREE
        # create a dict with POSS_VALUE: new list of the subsets
            # for each sublist in the storage dict:
                # call build tree again, and set the value corresponding to the feature_outcome key to be a new dict
    tree[feature_names[splitBy]] = dict()
    for feature_outcome in subsets:
        newSubtree = dict()
        if abs(bestGain) < 0.000000001:
            tree[feature_names[splitBy]][feature_outcome] = random.choice(subsets[feature_outcome])[-1]
        else:
            tree[feature_names[splitBy]][feature_outcome] = build_trees(subsets[feature_outcome],newSubtree,feature_names)
    return tree

def split_data(feature_list,index):
    """
    Splits the data set according to the outcomes of a particular index
    returns dict[str:list(tuple)]
    """
    toRet = dict()
    for vector in feature_list:
        if vector[index] in toRet:
            toRet[vector[index]].append(vector)
        else:
            toRet[vector[index]] = [vector]
    return toRet 
def splitPointFeature(feature_list,initEntrophy,feature_names):
    """
    Retuns the feature to split on based on feature index
    """
    bestFeature = 0
    bestGain = -math.inf
    for k in range(len(feature_names)-1):
        myEntrophy = calculate_entropy(k,feature_list)
        infoGain = initEntrophy - myEntrophy
        if infoGain > bestGain:
            bestFeature = k
            bestGain = infoGain
    # if abs(bestGain-0) < 0.000000001:
    #     return None
    return bestFeature,bestGain
# def printNicely(tree,depth):
#     for val in sorted(tree.keys()):
#         print("\n"+"\t"*depth+"*{0}:".format(val),end="")
def classify(dataPt, tree):
    """
    Classifies a data point based on the given tree
    """
    return classify_helper(dataPt,tree)
def classify_helper(dataPt,tree):
    if isinstance(tree,str):
        return tree
    for k in tree:
        # get the value corresponding to the variable k
        # check the dictionary for the value
        # if the value is not in the dictionary, choose a random value from the keys to go down
        # else:
            # check the value for the keys
            # if the key is a string, return true
            # otherwise, call classify_helper to continue searching
       #  print(k)
        myVal = dataPt[k]
        if myVal not in tree[k]:
            next_item = random.choice(list(tree[k].keys()))
            return classify_helper(dataPt,tree[k][next_item])
        else:
            if isinstance(tree[k][myVal],str):
                return tree[k][myVal]
            else:
                return classify_helper(dataPt,tree[k][myVal])


def printNicely(tree,depth,location=sys.stdout):
    for value in sorted(tree.keys()):
        if isinstance(tree[value],str):
            print("  "*depth+"*{0}-->{1}".format(value,tree[value]),file=location)
        else:
            print("  "*depth+"*{0}".format(value),file=location)
            printNicely(tree[value],depth+1,location=location)
# data = [["y","y","republican"],["y","y","democrat"]]
# featurenames = list(range(len(data[0])))
# tree = dict()
# tree = build_trees(data,tree,featurenames)
# printNicely(tree,0)
filename = sys.argv[1]
test_set_size = int(sys.argv[2])
with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
    data_set = []
    missing_vals = []
    feature_names = lines[0].split(",")
    for line in lines[1:]:
        dataPt = line.split(",")
        data_set.append(dataPt)
    random.shuffle(data_set)
    # input()
    train_pool = data_set[0:len(data_set)-test_set_size]
    # print(train_pool)
    testing_set = data_set[len(data_set)-test_set_size:len(data_set)]
    # print(testing_set)


# for random forest classifiers:


# go through each of the forest trees and classify based on mode for the data points in the testing set

def find_mode(classifications):
    el = None
    for key in classifications:
        if el is None:
            el = key
        if classifications[key] > classifications[el]:
            el = key
    return el
# create 10 trees each with a sample 1/10 the size of the training pool data
def random_forest(curr_train_pool,feature_names,totalSize,testSet):
    forest = list()
    # print("Given size: ",totalSize)
    train_set_size = totalSize//10
    if train_set_size == 0:
        train_set_size = 2
    # print("Resulting train set size: ",train_set_size)
    for k in range(10):
        tree = dict()
        myTrainSet = random.sample(curr_train_pool,train_set_size)
        tree = build_trees(myTrainSet,tree,list(range(len(feature_names))))
        forest.append(tree)
    # print("Number of trees used: ",len(forest))
    correct = 0
    total = 0
    for test in testing_set:
        poss_class = dict()
        for pine in forest:
            result = classify(test,pine)
            if result in poss_class:
                poss_class[result] += 1
            else:
                poss_class[result] = 1
        mode = find_mode(poss_class)
        # print("possible classifications:",poss_class)
        if mode == test[-1]:
            correct += 1
        total += 1
    return correct/total
    


Xsize = []
YAcc = []
Yrandforest = []
MIN = int(sys.argv[3])
MAX = int(sys.argv[4])
STEP = int(sys.argv[5])
for size in range(MIN,MAX,STEP):
    print(size)
    theSame = True
    train_set = random.sample(train_pool,k=size)
    while theSame:
        theSame = False
        count = dict()
        for t in train_set:
            if t[-1] in count:
                count[t[-1]] += 1
            else:
                count[t[-1]] = 1
        for c in count:
            if count[c] == 0:
                theSame = True
                break
        train_set = random.sample(train_pool,k=size)
    tree = dict()
    # print(len(train_set))
    tree = build_trees(train_set,tree,list(range(len(train_set[0]))))
    # print(tree)
    # printNicely(tree,0)
    # input()
    correct = 0
    total = 0
    # print(len(testing_set))
    # input()
    for data in testing_set:
        result = classify(data,tree)
        if result == data[-1]:
            correct += 1
            # print(result,data[-1])
        total += 1

    # results with random forest
    randforestacc = random_forest(train_pool,feature_names,size,testing_set)
    Xsize.append(size)
    YAcc.append(correct/total)
    Yrandforest.append(randforestacc)
    print("Normal accuracy: ",correct/total)
    print("Random forest accuracy: ",randforestacc)
# print(Xsize)
# print(YAcc)
plot_data(Xsize,YAcc,Yrandforest,"Training Set Size","Accuracy")