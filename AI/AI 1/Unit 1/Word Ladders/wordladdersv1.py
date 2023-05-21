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

def trace_path(end, poss_paths):
    path = []
    length = 0
    p = end
    while p is not None:
        path.append(p)
        p = poss_paths[p]
        length += 1

    return length,path        

with open(sys.argv[1]) as f:
    word_table = {line.strip().lower():[] for line in f}

with open(sys.argv[2]) as f2:
    puzzles = [line.strip().lower().split() for line in f2]

start = time.perf_counter()
for w in word_table.keys():
    gen_children(w,word_table)
end = time.perf_counter()

print("Data structure storing children built in %s seconds" %(end-start))
print("There are %s words in this dictionary."% len(word_table))

start2 = time.perf_counter()
for line,case in enumerate(puzzles):
    print("Line : %s" % line)
    tree = BFSearch(case[0],case[1],word_table)
    if tree is not None:
        length,path = trace_path(case[1],tree)
        print("Length: ",length)
        print("Path taken: ")
        for i in range(len(path)-1,-1,-1):
            print(path[i])

    else:
        print("No solution for given word")
    print()

end2 = time.perf_counter()

print("Time to solve puzzles: ", (end2-start2), " second")

print("Total run time: ", (end2-start))
