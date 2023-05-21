import sys

arg = sys.argv[1]

def fib(n):
    fibSeries = []
    curr = 1
    next = 1
    for i in range(1,n):
        fibSeries.append(curr)
        temp = next
        next = next + curr
        curr = temp
    return fibSeries

if arg == "A" or arg == "B":
    total = 0
    for i in range(2,len(sys.argv)):
        total += int(sys.argv[i])
    print(total)

elif arg == "C":
    for i in range(2,len(sys.argv)):
        val = int(sys.argv[i])
        if val%3 == 0:
            print(val, end=" ")
    print("\n")

elif arg == "D":
    arr = fib(int(sys.argv[2]))
    arr = [str(i) for i in arr]
    print(" ".join(arr))

elif arg == "E":
    start = int(sys.argv[2])
    end = int(sys.argv[3])

    for k in range(start, end + 1):
        print(k*k - 3 * k + 2, end = " ")

elif arg == "F":
    a = float(sys.argv[2])
    b = float(sys.argv[3])
    c = float(sys.argv[4])

    if a + b < c or b + c < a or a + c < b:
        raise Exception("Invalid side length")

    else:
        s = 0.5 * (a+b+c)
        area = (s * (s-a) * (s-b) *(s-c))**0.5
        print(area)


elif arg == "G":
    vowels = {"a":0,"e":0,"i":0,"o":0,"u":0}
    string = sys.argv[2].lower()

    for ch in string:
        if ch in vowels:
            vowels[ch] += 1
    
    for key in vowels:
        print(key,":",vowels[key])