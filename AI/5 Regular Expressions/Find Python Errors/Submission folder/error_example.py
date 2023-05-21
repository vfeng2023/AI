# find max and min of an array
String name = "Bob 3" # incorrect variable assignment with type declaration
teacher = "4Smith" 
int period = 7 # incorrect variable assignment with type declaration
date == "February" # variable assignment using == instead of =
isSmith = teacher == "4Smith" 
def printStudent(name,teacher,period) # missing colon
    print("Name",name)
    print("Teacher :",teacher)
    print("Period :",period)
def findMax(arr):
    1maxval = arr[0] # variable starting with digit
    for i in range(len(arr)):
        if arr[i] > maxval or arr[i] == maxval # missing colon
            maxval == arr[i] # variable assignment using == instead of =
    return maxval

def findMin(arr):
    3minval = arr[0] # variable name staring with digit
    for i in range(len(arr)):
        if arr[i] < minval:
            minval = arr[i]
    return minval


array = [4,5,6,1,2,4]
maximum = findmax(array) # undefined function name
minimum = findmin(array) # undefined function name
print("Array: ",array)
print("Minimum: ",minimum)
print("Maximum value", maximum)

