import math
def calculate_entropy(featureIndex,featureList,values):
    count = dict()

    # count the values present
    for k in range(len(featureList)):
        if (feature_value:=featureList[k][featureIndex]) not in count:
            count[featureList[k][featureIndex]] = dict()
        if values[k] not in count[feature_value]:
            count[feature_value][values[k]] = 0
        count[feature_value][values[k]] += 1
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
        expected_entrophy += (sub_total/len(values) * myEntrophy)
    return expected_entrophy

def initEntrophy(valueList):
    count = dict()
    for v in valueList:
        # print(valueList)
        # input()
        if v not in count:
            count[v] = 0
        count[v] += 1
    entrophy = 0
    for k in count:
        entrophy += (-1*count[k]/len(valueList) * math.log2(count[k]/len(valueList)))
    return entrophy
# store the values in play_tennis as a list of values
with open('play_tennis.csv') as f:
    lines = [line.strip() for line in f.readlines()]
    print("Features: ",lines[0])
    featureNames = lines[0].split(",")
    featureList = []
    values = []
    for line in lines[1:]:
        line = line.split(",")
        featureList.append(line[:-1])
        values.append(line[-1])

start_ent = initEntrophy(values)
print(start_ent)
for f in range(len(featureNames)-1):
    print("feature: ",featureNames[f],end="\t")
    feature_entrophy = calculate_entropy(f,featureList,values)
    print("Entrophy change: ", (start_ent-feature_entrophy),end="\n")
tree = dict()
def build_trees(feature_list,values):
    """
    1.  Consider each feature in turn.  Find the information gain from differentiating based on that feature.
    # feature list is the feature values associated with a particular feature,
    # featureNames is the name of the feature
    # otherwise, identification is done on index   
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
    # if the initial entrophy is 0, then to the tree dict, add the title of the last column and result
    # calculate the entrophy gain for each given feature by index
    # once decided the feature(index) which will give the largest information gain, 
        # add the name of the feature to TREE
        # create a dict with POSS_VALUE: new list of the subsets
            # for each sublist in the storage dict:
                # call build tree again, and set the value corresponding to the feature_outcome key to be a new dict
                

def split_data(feature_list,index):
    """
    Splits the data set according to the outcomes of a particular index
    returns dict[str:tuple]
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
    for k in range(len(feature_names)):
        myEntrophy = calculate_entropy(feature_names,feature_list,)