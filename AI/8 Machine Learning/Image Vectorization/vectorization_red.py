from PIL import Image
import random
import sys
# img = Image.open('puppy.jpg')

def naive8Color(filename):
    """
    Produces the naive 8 color quantization
    """
    img = Image.open(filename)
    width,height = img.size
    pix = img.load()
    for x in range(width):
        for y in range(height):
            color = pix[x,y]
            newColor = [0,0,0]
            for i in range(len(color)):
                if color[i] < 128:
                    newColor[i] = 0
                else:
                    newColor[i] = 255
            pix[x,y] = tuple(newColor)
    colors = [(i,j,k) for i in (0,255) for j in (0,255) for k in (0,255)]
    combined = addMenu(img,colors)
    combined.save(filename+'.naive8color.png')



def naive27Color(filename):
    """
    Produces the naive 27 color quantization
    """
    img = Image.open(filename)
    width,height = img.size
    pix = img.load()
    for x in range(width):
        for y in range(height):
            color = pix[x,y]
            newColor = [0,0,0]
            for i in range(len(color)):
                if color[i] < 255//3:
                    newColor[i] = 0
                elif color[i] < 255//3*2:
                    newColor[i] = 127
                else:
                    newColor[i] = 255
            pix[x,y] = tuple(newColor)
    colorowos = []
    pizchoice = [0,127,255]
    for i in pizchoice:
        for j in pizchoice:
            for k in pizchoice:
                colorowos.append((i,j,k))
    combined = addMenu(img,colorowos)
    combined.save(filename+'.naive27color.png')
# filename = 'puppy.jpg'
# naive8Color(filename)
# naive27Color(filename)


K = 2
# run the k means algorithm
def kmeans(filename):
    """
    1) Specify a value of K.
    2) Choose K distinct random elements of the set. (In our case, the specific vectors representing K random
    elements from the data set, ensuring that all K of the selections represent different specific stars.) Call these the
    means, though we haven’t averaged anything yet.
    3) Associate each mean with a list of stars. Loop over every single star and assign it to the list belonging to the
    mean that is closest to that star’s data. We’ll do this by finding the squared error between the star and each
    mean and assigning it to the mean that results in the smallest squared error. (More on this below.)
    4) Take each list of stars generated in step 3 separately. Find the actual mean of these stars. That is, form a new
    vector with the average value of each star’s surface temperature in this group, then the average of luminosity,
    etc. Intuitively, you can see that – at least at first – these values will be quite different from our initial “means”
    that we randomly guessed in step 2.
    5) Repeat steps 3 and 4 over and over. Since the values of the means have changed, stars that used to belong to
    one mean’s group will now shift to a different one. Therefore, as step 4 repeats, the means will change again…
    and the points will move again… etc. Keep repeating until this becomes stable; that is, until no star changes
    group / no mean changes value. (This means you’ll need to keep track of the groups and how many stars move
    in or out during each round.)
    6) When the process resolves, you’ve found the K specific means that minimize the squared error! (Well, pretty
    close; the algorithm isn’t mathematically guaranteed to converge to optimality. In practice it is quite robust, but
    may produce a variety of near-optimal answers.) Each mean is paired with a group of data points; these are the
    natural groups that the algorithm has found. 

    """
    img = Image.open(filename)
    pixelsCount = dict() # pizle color and location
    imgPix = img.load()
    width,height = img.size
    for x in range(width):
        for y in range(height):
            if imgPix[x,y] in pixelsCount:
                pixelsCount[imgPix[x,y]].append((x,y))
            else:
                pixelsCount[imgPix[x,y]] = [(x,y)]
    allPixels = list(pixelsCount.keys()) # the types of pixels
    # print("All pixels",len(allPixels))

    means = random.sample(allPixels,k=K)
    # do initial classification
    meanGroups = {color:[] for color in means}
    for c in allPixels:
        minMean = None
        minDist = float('inf')
        # find the maximum groups
        for mean in meanGroups:
            if (v:=squaredError(mean,c)) < minDist:
                minDist = v
                minMean = mean
        meanGroups[minMean].append(c)
    transfer = True
    generation = 1
    while transfer: # while there are changes to the groups
        # calculate the new means
        # print(meanGroups)
        newGroup = dict()
        for group in meanGroups:
            avg = calc_avg(pixelsCount, meanGroups[group])
            newGroup[avg] = meanGroups[group]
        # move the pixels around
        # print(newGroup.keys())
        # input()
        # print(newGroup)
        # print("newGroup: ",newGroup.keys())
        # input()
        moved = {k:[] for k in newGroup.keys()}
        kepted = {k:[] for k in newGroup.keys()}
        added = {k:[] for k in newGroup.keys()}
        for newMean in newGroup:
            # calculate the closest mean
            for c in newGroup[newMean]:
                minMean = None
                minDist = float('inf')
                # find the maximum groups
                for submean in newGroup:
                    if (v:=squaredError(submean,c)) < minDist:
                        minDist = v
                        minMean = submean
                if minMean is newMean:
                    kepted[minMean].append(c)
                else:
                    moved[newMean].append(c)
                    added[minMean].append(c)
        # print("Kept", kepted)
        # print("Moved",moved)
        # print("Added",added)
        # input()
        # stats and transfer
        transfer=False
        netChanges = []
        for m in newGroup:
            net = len(added[m]) - len(moved[m]) # added - moved
            netChanges.append(net)
            if net!=0:
                transfer = True
            kepted[m].extend(added[m])
        print("Generation {0}: {1}".format(generation,netChanges))
        generation += 1
        meanGroups = kepted
        # print(kepted)

    # alter image
    colors = []
    for m in meanGroups:
        pizm = tuple(round(c) for c in m)
        colors.append(pizm)
        for pix in meanGroups[m]:
            for x,y in pixelsCount[pix]:
               imgPix[x,y] = pizm
    img.show()
    combined = addMenu(img,colors)
    combined.save(filename+'.kmeansout{0}.png'.format(K))

def calc_avg(pixelsCount, pixelsList):
    red = 0
    green = 0
    blue = 0
    total = 0
    for pixel in pixelsList:
                # print(pixel)
                # input()
        count = len(pixelsCount[pixel])
        red += (pixel[0] * count)
        green+= (pixel[1] * count)
        blue += (pixel[2] * count)
        total += count
            #print(total)
            # print(total)
    if total == 0:
        total += 1
    avg = (red/total,green/total,blue/total)
    return avg


    # classify the number and type of each pixel in the form:
        # (r,g,b), instances is accessed via pixels
    # from this group, randomly select K to be the initial means:
    # while net change != 0:
        # for each one: 
            # 3 lists - staying, moving, incoming for the means

            # reclassify and recalulate means

            # 
def squaredError(mean,star):
    diff = 0
    for k in range(3):
        diff += (mean[k]-star[k]) * (mean[k]-star[k])
    return diff

def addMenu(img, colors):
    """
    Adds band of colors used at the foot of the image
    """
    width = img.size[0]
    bandheight = width//len(colors)+1
    colors.sort()
    colorBand = Image.new("RGB",(width,bandheight),0)
    pix = colorBand.load()
    boxsize = bandheight
    for y in range(bandheight):
        colorIndex = 0
        for x in range(width):
            if colorIndex < len(colors):
                pix[x,y] = colors[colorIndex]
            else:
                pix[x,y] = colors[len(colors) -1]
            # print(colorIndex)
            if x//boxsize > colorIndex:
                if colorIndex-1 < len(colors):
                    colorIndex += 1

    w = img.size[0]
    h = img.size[1] + colorBand.size[1]
    combined = Image.new("RGB",(w,h))
    combined.paste(img)
    combined.paste(colorBand,(0,img.size[1]))
    return combined
    

# newImage = Image.new('rbg','2')
filename = "drJ.jpeg"# sys.argv[0]
# naive8Color(filename)
# naive27Color(filename)
# kmeans(filename)
process = input("(N)aive or (K) means? ")
if process == "N":
    naive8Color(filename)
    naive27Color(filename)
else:
    kmeans(filename)

