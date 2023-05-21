from math import log
import random
K = 7
# run the k means algorithm on star_data.csv
with open('star_data.csv') as f:
    lines = [line.strip() for line in f.readlines()[1:]]
    # print(lines)
    all_vectors = []
    for line in lines:
        temp,lum,radius,magn,star_type,_,_ = line.split(",")
        temp = log(float(temp),10)
        lum = log(float(lum),10)
        radius = log(float(radius),10)
        magn = float(magn)
        star_type = int(star_type)
        # sequence:<log(Temperature), log(Luminosity), log(Radius), Absolute Visual Magnitude, star Type>  
        all_vectors.append((temp,lum,radius,magn,star_type))


def initializeKmeans():
    start_means = random.sample(all_vectors,k=K)
    start_dict = {mean:[] for mean in start_means}
    return start_dict

def classify(groups):
    # initial classification of the groups
    
    for star in all_vectors:
        # calculate the smallest difference
        minDiff = float('inf')
        minMean = None
        for mean in groups:
            diff = squaredError(mean,star)
            if diff < minDiff:
                minDiff = diff
                minMean = mean
        # adds it to associated list
        groups[minMean].append(star)
    # print(all_vectors)
    return groups
    

def squaredError(mean,star):
    diff = 0
    for k in range(4):
        diff += (mean[k]-star[k]) * (mean[k]-star[k])
    return diff

def kmeans():
    # store the values in a set
    myDict = initializeKmeans()
    # loop through existing starts and classify them
    myDict = classify(myDict)
    # while not stablized:
    change = True
    while change:
        newGroups = dict()
        for key in myDict:
            newkey = find_means(myDict[key])
            newGroups[newkey] = myDict[key]
        
        # figure out the starts that need to be moved/kept
        movedStars = {key:[] for key in newGroups}
        keptStars = {key:[] for key in newGroups}

        # for each new mean:
            # for star in each group:
                # see if it is moved
                # if moved to another group: 
                    # change
        for mean in newGroups:
            for star1 in newGroups[mean]:
                minDiff = float('inf')
                minMean = None
                for submean in newGroups.keys():
                    diff = squaredError(submean,star1)
                    if diff < minDiff:
                        minDiff = diff
                        minMean = submean
                if minMean is mean:
                    keptStars[minMean].append(star1)
                else:
                    movedStars[minMean].append(star1)
        # change the location if necessary by adding to keptStarts
        change = False
        for moveMean in movedStars:
            if len(movedStars[moveMean]) > 0:
                change = True
                keptStars[moveMean].extend(movedStars[moveMean])
        myDict = keptStars
    # loop through each list of stars and see if they change location
    # structure for storing groups:
        # dictionary of tuples to list of tuples
        # calulate means to make the new groups
        # if current means the same as previous means -- break
    return keptStars
def find_means(star_list):
    values = [0,0,0,0]
    for s in star_list:
        for i in range(4):
            values[i] += s[i]
    for j in range(4):
        values[j]/=len(star_list)
    return tuple(values)
    
resultClass = kmeans()
print(resultClass)
filename = input("Save stats to file: ")
with open(filename,"w") as f:
    for res in resultClass:
        starType = [0,0,0,0,0,0]
        # get the percentage of stars of each type
        for star in resultClass[res]:
            starType[star[4]] += 1
        totalStars = sum(starType)
        print("Mean: ",res)
        f.write("Mean :"+str(res)+"\n")
        f.write("Size of group: "+str(len(resultClass[res]))+"\n")
        print("Percent of each type in group")
        for k in range(len(starType)):
            percent = starType[k]/totalStars * 100
            percent = round(percent,ndigits=3)
            f.write(s:="{0} : {1}%\n".format(k,percent))
            print(s)
        print("Stars: ")
        for member in resultClass[res]:
            print(member)
f.close()

        