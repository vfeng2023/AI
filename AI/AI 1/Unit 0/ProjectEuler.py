import math
def problem1():
    return sum([i for i in range(1,1000) if i%3==0 or i%5 == 0])

def problem2():
    curr = 1
    next = 1
    total = 0
    while curr < 4000000:
        if curr%2 == 0:
            total += curr
        temp = next
        next = next + curr
        curr = temp

    return total

def isPrime(num):
    if num == 1:
        return False
    if num == 2:
        return True
    for i in range(2, int(math.sqrt(num))+1):
        if num%i==0:
            return False
    return True

def problem3(upper):
    largest = 1
    for k in range(1, int(math.sqrt(upper))+1):
        if upper %k == 0:
            if isPrime(k):
                largest = max(largest,k)
            if isPrime(upper/k):
                largest = max(largest,upper/k)
    return largest

def isPalindrome(num):
    digits = str(num)
    return digits == digits[::-1]

    return True
def problem4():
    largest = 91*99
    for i in range(1000,99,-1):
        for j in range(i,99,-1):
            if isPalindrome(i*j):
                largest = max(largest,i*j)
    return largest

def gcd(a,b):
    while b != 0:
        t = b
        b = a%b
        a = t
    return a

def problem5(n):
    prod = 1
    for i in range(1,n+1):
        if prod%i!=0:
            prod = prod//gcd(prod,i) * i
    return prod

def problem6(n):
    return (n*(n+1)//2)**2 - n*(n+1)*(2*n+1)//6

def problem7():
    pCount = 0
    p = 1
    while pCount < 10001:
        if isPrime(p):
            pCount += 1
        p += 1
    return p - 1

def problem8():
    string = """
    73167176531330624919225119674426574742355349194934
96983520312774506326239578318016984801869478851843
85861560789112949495459501737958331952853208805511
12540698747158523863050715693290963295227443043557
66896648950445244523161731856403098711121722383113
62229893423380308135336276614282806444486645238749
30358907296290491560440772390713810515859307960866
70172427121883998797908792274921901699720888093776
65727333001053367881220235421809751254540594752243
52584907711670556013604839586446706324415722155397
53697817977846174064955149290862569321978468622482
83972241375657056057490261407972968652414535100474
82166370484403199890008895243450658541227588666881
16427171479924442928230863465674813919123162824586
17866458359124566529476545682848912883142607690042
24219022671055626321111109370544217506941658960408
07198403850962455444362981230987879927244284909188
84580156166097919133875499200524063689912560717606
05886116467109405077541002256983155200055935729725
71636269561882670428252483600823257530420752963450"""
    num = "".join(string.split())
    digits = list(map(int,num))
    big = 1
    for i in range(len(digits)-12):
        prod = 1
        for j in range(13):
            prod *= digits[i+j]
        big = max(big, prod)

    return big
def isValid(a,b,c):
    if a + b <= c or a + c < b or b + c < a:
        return False
    return a+b+c == 1000 and a*a + b*b == c*c

def problem9():
    for a in range(1,500):
        for b in range(1, 500):
            c2 = a*a + b*b
            if abs(int(c2**0.5)-c2**0.5) < 0.000000001 and a + b + int(c2**0.5) == 1000:
                return a*b*int(c2 ** 0.5)

    return 0

def problem29():
    nums = set()
    for i in range(2,101):
        for j in range(2,101):
            nums.add(i**j)

    return len(nums)
print("#1:",problem1())
print("#2: ",problem2())
print("#3: ",problem3(600851475143))
print("#4: ",problem4())
print("#5: ",problem5(20))
print("#6: ",problem6(100))
print("#7: ",problem7())
print("#8: ",problem8())
print("#9: ",problem9())
print("#29: ",problem29())
    
