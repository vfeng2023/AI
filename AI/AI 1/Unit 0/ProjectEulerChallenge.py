from datetime import datetime # to tell how fast each solution is
def problem12():
    has500 = False
    n = 1
    while has500 == False:
        tri = int(n * (n + 1) / 2)
        count = 0
        for i in range(1, int(tri**0.5)):
            if tri % i == 0:
                count += 1
        count *=2
        if abs(tri**0.5-int(tri**0.5)) < 0.000000001:
            count += 1
        if count >= 500:
            has500 = True
            return tri
        n += 1

def sequence14(n):
    count = 0
    while n>1:
        if n%2 == 0:
            n=n/2
        else:
            n = 3*n+1
        count += 1
    return count+1
def problem14():

    most = sequence14(1)
    upper = 10**6
    n = 1
    for i in range(2,upper+1):
        val = sequence14(i)
        if(val > most):
            most = val
            n = i
    return n

def problem17():
    units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
             "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    count = 0
    for i in range(1,1000):
        num = ""
        if i%100 < 20 and i%100 > 0:
            num = units[i%100] + num
        elif i%100 >= 20:
            rem = i%100
            if rem%10!=0:
                num = units[rem%10]+num
            num = tens[rem//10-2]+num
        if i%100!=0 and i/100 > 0:
            num = "and"+num
        if i/100 > 0:
            num = units[i//100]+"hundred"+num
        count += len(num)
    count += len("one")+len("thousand")
    return count

def maxSum(triangle,i,j):
    if i < len(triangle) and j < len(triangle[i]):
        return max(triangle[i][j] + maxSum(triangle,i+1,j),triangle[i][j]+maxSum(triangle,i+1,j+1))
    return 0
def problem18():
    tri = [[75],
            [95,64],
            [17,47,82],
            [18,35,87,10],
            [20,4,82,47,65],
            [19,1,23,75,3,34],
            [88,2,77,73,7,63,67],
            [99,65,4,28,6,16,70,92],
            [41,41,26,56,83,40,80,70,33],
            [41,48,72,33,47,32,37,16,94,29],
            [53,71,44,65,25,43,91,52,97,51,14],
            [70,11,33,28,77,73,17,78,39,68,17,57],
            [91,71,52,38,17,14,91,43,58,50,27,29,48],
            [63,66,4,68,89,53,67,30,73,16,69,87,40,31],
            [4,62,98,27,23,9,70,98,73,93,38,53,60,4,23]]
    return maxSum(tri,0,0)

def problem21():
    divSums = []

    for n in range(10001):
        total = 0
        for i in range(1,int(n**0.5)+1):
            if n%i == 0:
                total += i + n//i
        total -= n
        if abs(n**0.5 - int(n**0.5)) < 0.000000001:
            total -= int(n**0.5)

        divSums.append(total)
    numSum = 0
    for num in range(10000):
        if divSums[num] < 10000 and divSums[divSums[num]] == num and divSums[num]!=num:
            numSum += num

    return numSum


def fifthSum(n):
    digits = list(map(int,list(str(n))))
    return sum([d**5 for d in digits])


def problem24():
    """
        next lexographic permutation from wikipedia:
        Find the largest index k such that a[k] < a[k + 1]. If no such index exists, the permutation is the last permutation.
        Find the largest index l greater than k such that a[k] < a[l].
        Swap the value of a[k] with that of a[l].
        Reverse the sequence from a[k + 1] up to and including the final element a[n].
        call this 1000000 times starting with 0123456789

    """
    ls = [0,1,2,3,4,5,6,7,8,9]
    for i in range(1000000-1):
        k = len(ls) -2
        while k+1 > 0 and ls[k] > ls[k+1]:
            k-=1
        l = 0
        for i in range(k,len(ls)):
            if ls[i] > ls[k]:
                l = i

        ls[l],ls[k] = ls[k],ls[l]
        start = k+1
        end = len(ls) -1 
        while start < end:
            ls[start],ls[end] = ls[end],ls[start]
            start += 1
            end -=1

    return "".join(list(map(str,ls)))        
        
def problem28():
    #each arm of the spiral follows a quadratic pattern.
    # 1,3,13; 1,9,25; 1,5,17, 1,7,21;
    # number of terms in each diagonal including one is n//2 + 1
    # 1,3,13 -- 4n^2 - 10n + 7
    # 1,9,25 --4n^2 - 4n + 1
    # 1,5,17 -- 4n^2 -8n + 5
    # 1,7,21 --4n^2 - 6n + 3

    total = 0
    for n in range(1,1001//2+2):
        total += 4*n*n - 10*n + 7
        total += 4*n*n - 4*n + 1
        total += 4*n*n - 8*n + 5
        total += 4*n*n - 6*n + 3
    
    total -=3
    return total

def problem30():
    upper = 9*9**5 #upper limit is 9*9^5, which is the edge case( really big number where fifth power sum is likely always larger than number)
    total = 0
    for n in range(2,upper+1):
        if fifthSum(n) == n:
            total += n
    return total


# print(datetime.now())
# print("#12: ",problem12()) #approximately 6 seconds
# print(datetime.now())
# print("#14: ",problem14()) #approximately 48 seconds
# print(datetime.now())
# print("#17: ",problem17()) # pretty fast
# print("#18: ",problem18()) # also pretty fast
# print("#21: ",problem21())

# print("#24: ",problem24())
print("#28: ", problem28())
# print("#30: ",problem30())