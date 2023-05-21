from collections import deque
import time
import sys
def gen_children(word_list):
    patterns = dict()
    for i in range(len(word_list)-1):
        word1 = word_list[i]
        word2 = word_list[i+1]
        key = match(word1,word2)

        if key in patterns:
            patterns[key].append(word1)

        else:
            patterns[key] = [word1]

    return patterns

def get_childs(word,pattern_dict):
    children = set()
    for i in range(len(word)-1,-1,-1):
        if (key:=word[:i]) in pattern_dict:
            for w in pattern_dict[key]:
                if isChild(word,w):
                    children.add(w)

    return children

def match(word1,word2):
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            return word1[:i]

def isChild(parent,child):
    diff = 0
    for ch in range(len(parent)):
        if parent[ch] != child[ch]:
            diff += 1
    return diff == 1
def BFSearch(start,end,table):
    fringe = deque()
    visited = dict()

    fringe.append(start)
    visited[start] = None

    while len(fringe) > 0:
        v = fringe.popleft()
        if v == end:
            return visited

        children = get_childs(v,table)
        for c in children: # where table contains the children of v
            if c not in visited:
                visited[c] = v
                fringe.append(c)

    return None

def trace_path(end, poss_paths):
    path = ""
    length = 0
    p = end
    while p is not None:
        path = p + "\n" + path
        p = poss_paths[p]
        length += 1

    return length,path        

with open("words_06_letters.txt") as f:
    words = [line.strip().lower() for line in f]
    

with open("puzzles_normal.txt") as f2:
    puzzles = [line.strip().lower().split() for line in f2]

start = time.perf_counter()
word_table = gen_children(words) 
end = time.perf_counter()

print(word_table)
print("Data structure storing children built in %s seconds" %(end-start))
print("There are %s words in this dictionary."% len(word_table))

print(get_childs("zeroes",word_table))
# run_results = []
# start2 = time.perf_counter()
# for line,case in enumerate(puzzles):
#     tree = BFSearch(case[0],case[1],word_table)
#     if tree is not None:
#         res = trace_path(case[1],tree)
#         run_results.append(res)
#     else:
#         run_results.append((0,"No Solution"))
# end2 = time.perf_counter()

# print("Time to solve puzzles: ", (end2-start2), " second")

# print("Total run time: ", (end2-start))

# for index,case in enumerate(run_results):
#     print("Length: ",case[0])
#     print("Path: \n",case[1])
