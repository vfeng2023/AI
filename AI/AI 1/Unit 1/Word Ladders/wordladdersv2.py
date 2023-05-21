from collections import deque
import time
import sys
def gen_children(word,valid):
    word = word.lower()
    alpha = list("abcdefghijklmnopqrstuvwxyz")
    chars = list(word)
    for i in range(len(chars)):
        original = chars[i]
        for ch in alpha:
            chars[i] = ch
            if (s:="".join(chars)) in valid.keys() and s!=word:
                valid[word].append(s)

        chars[i] = original



def BFSearch(start,end,table):
    fringe = deque()
    visited = dict()

    fringe.append(start)
    visited[start] = None

    while len(fringe) > 0:
        v = fringe.popleft()
        if v == end:
            return visited
        for c in table[v]: # where table contains the children of v
            if c not in visited:
                visited[c] = v
                fringe.append(c)

    return None

def BFSearch2(start,table):
    fringe = deque()
    visited = dict()

    fringe.append(start)
    visited[start] = None

    while len(fringe) > 0:
        v = fringe.popleft()
        for c in table[v]: # where table contains the children of v
            if c not in visited:
                visited[c] = v
                fringe.append(c)

    return len(visited)

def BFSearch3(start,table):
    fringe = deque()
    visited = set()

    fringe.append(start)
    visited.add(start)

    while len(fringe) > 0:
        v = fringe.popleft()
        for c in table[v]: # where table contains the children of v
            if c not in visited:
                visited.add(c)
                fringe.append(c)

    return visited

def BFSearch4(start,table):
    fringe = deque()
    visited = dict()

    fringe.append(start)
    visited[start] = 0

    longest = 0
    child = start
    while len(fringe) > 0:
        v = fringe.popleft()
        for c in table[v]: # where table contains the children of v
            if c not in visited:
                visited[c] = visited[v]+1
                fringe.append(c)
                if visited[c] > longest:
                    longest = visited[c]
                    child = c


    return longest,child

def trace_path(end, poss_paths):
    path = []
    length = 0
    p = end
    while p is not None:
        path.append(p)
        p = poss_paths[p]
        length += 1

    return length,path

def trace_path4(end,poss_paths):
    path = []
    length = 0
    p = end
    while p !=0:
        path.append(p)
        p = poss_paths[p]
        length += 1

    return length,path        

with open(sys.argv[1]) as f:
    word_table = {line.strip().lower():[] for line in f}

# with open("puzzles_normal.txt") as f2:
#     puzzles = [line.strip().lower().split() for line in f2]

start = time.perf_counter()
for w in word_table.keys():
    gen_children(w,word_table)
end = time.perf_counter()

print("Data structure storing children built in %s seconds" %(end-start))
print("There are %s words in this dictionary."% len(word_table))

singletons = 0
for w in word_table.keys():
    if len(word_table[w]) == 0:
        singletons += 1

print("#1: ",singletons," have no solution")


largest = 1
largest_word = ""
for w in word_table.keys():
    size = BFSearch2(w,word_table)
    if size > largest:
        largest = size
        largest_word = w

print("#2: ",largest," ",largest_word)


total = 0
searched = set()
for w in word_table.keys():
    if w not in searched:
        clump = BFSearch3(w,word_table)
        searched = searched.union(clump)

        if len(clump) > 1:
            total += 1
print("#3:",total)

# result is the set of all of the words in the clump
result = BFSearch3(largest_word,word_table)

# print(result)
# print(len(result))

length4 = 0
root = largest_word
stop = ""
for j in result:
    lengthp, end = BFSearch4(j,word_table)
    if  lengthp> length4:
        length4 = lengthp
        root = j
        stop = end

path = BFSearch(root,stop,word_table)
length4,trail = trace_path(stop,path)
print("#4: ")
print("Length = ",length4)

print("Path: ")

for i in range(len(trail)-1,-1,-1):
    print(trail[i])









