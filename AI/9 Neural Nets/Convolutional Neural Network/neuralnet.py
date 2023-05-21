from itertools import pairwise
import numpy as np

def relu(val):
    return max(0,val)

vectorized_relu = np.vectorize(relu)
def applyFilter(image, filter,bias,stride=1):
    """
    What function is supposed to do:
    Using NumPy, we can program the convolution operation quite easily. 
    The convolution function makes use of a for-loop to convolve all the filters over the image. 
    Within each iteration of the for-loop, two while-loops are used to pass the filter over the image. 
    At each step, the filter is multipled element-wise(*) with a section of the input image. 
    The result of this element-wise multiplication is then summed to obtain a single value using NumPy’s sum method, 
    and then added with a bias term.
    """
    # applies and returns result from application of a singular filter
    imw,imh = image.shape
    filw,filh = filter.shape
    outputWidth = int(np.floor((imw-filw)/stride)+1)
    outputHeight = int(np.floor((imh-filh)/stride)+1)
    convFeatures = np.zeros((outputWidth,outputHeight))

    for row in range(0,imw-filw+1,stride):
        for col in range(0,imh-filh+1,stride):
            slice = image[row:row+filw,col:col+filh]
            pairwiseprod = slice * filter
            convOpResult = np.sum(pairwiseprod)
            convFeatures[row][col] = convOpResult
    convFeatures = convFeatures + bias
    # print(convFeatures)
    convFeatures = vectorized_relu(convFeatures)

    return convFeatures

testimg = np.array([[1,1,1,0,0],[0,1,1,1,0],[0,0,1,1,1],
[0,0,1,1,0],[0,1,1,0,0]])
filter = np.array([[-1,0,-1],[0,-1,0],[-1,0,-1]])
biases = np.zeros((1,1))

print(applyFilter(testimg,filter,biases))