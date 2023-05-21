import math
import sys
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
filename = sys.argv[1]
with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
    # print("Features: ",lines[0])
    featureNames = [varName + "?" for varName in lines[0].split(",")]
    featureList = []
    result_values = []
    for line in lines[1:]:
        line = line.split(",")
        featureList.append(line)
        result_values.append(line[-1])

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
    print(initialEntro)
    # print()
    # if the initial entrophy is 0, then to the tree dict, add the title of the last column and result
    if abs(initialEntro - 0) < 0.000000000001:
        # tree[feature_names[-1]]=feature_list[0][-1] # assign the last value
        return feature_list[0][-1]
    # calculate the entrophy gain for each given feature by index
    splitBy = splitPointFeature(feature_list,initialEntro,feature_names)
    subsets = split_data(feature_list,splitBy)
    # once decided the feature(index) which will give the largest information gain, 
        # add the name of the feature to TREE
        # create a dict with POSS_VALUE: new list of the subsets
            # for each sublist in the storage dict:
                # call build tree again, and set the value corresponding to the feature_outcome key to be a new dict
    tree[feature_names[splitBy]] = dict()
    for feature_outcome in subsets:
        newSubtree = dict()
        print(feature_outcome,end=" ")
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
    print(feature_names[bestFeature],bestGain)
    return bestFeature
# def printNicely(tree,depth):
#     for val in sorted(tree.keys()):
#         print("\n"+"\t"*depth+"*{0}:".format(val),end="")
def printNicely(tree,depth,location=sys.stdout):
    for value in sorted(tree.keys()):
        if isinstance(tree[value],str):
            print("  "*depth+"*{0}-->{1}".format(value,tree[value]),file=location)
        else:
            print("  "*depth+"*{0}".format(value),file=location)
            printNicely(tree[value],depth+1,location=location)

print("Initial Entropy: ",end=" ")
tree = build_trees(featureList,tree,featureNames)
printNicely(tree,0)
# with open("treeout.txt","w") as f:
#     printNicely(tree,0,f)
# pprint.pprint(tree)