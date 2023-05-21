from collections import deque
import time
import sys
def gen_children(word_list):
    patterns = dict()
    child_patterns = dict()
    for i in range(len(word_list)):
        child_patterns[word_list[i]] = []
        for j in range(len(word_list[i])):
            pat = word_list[i][:j]+"*"+word_list[i][j+1:]
            child_patterns[word_list[i]].append(pat)
            if pat in patterns:
                patterns[pat].append(word_list[i])

            else:
                patterns[pat] = [word_list[i]]


    return patterns,child_patterns

def get_childs(word,pattern_dict,child_patt):
    children = list()
    patt = child_patt[word]
    for p in patt:
        children.append(pattern_dict[p])
    return children

def BFSearch(start,end,table,child_patt):
    fringe = deque()
    visited = dict()

    fringe.append(start)
    visited[start] = None

    while len(fringe) > 0:
        v = fringe.popleft()
        if v == end:
            return visited

        children = get_childs(v,table,child_patt)
        for clump in children: # where table contains the children of v
            for c in clump:
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

with open(sys.argv[1]) as f:
    words = [line.strip().lower() for line in f]
    

with open(sys.argv[2]) as f2:
    puzzles = [line.strip().lower().split() for line in f2]

start = time.perf_counter()
word_table,child_pat = gen_children(words) 
end = time.perf_counter()

print("Data structure storing children built in %s seconds" %(end-start))
print("There are %s words in this dictionary."% len(word_table))

run_results = []
start2 = time.perf_counter()
for line,case in enumerate(puzzles):
    tree = BFSearch(case[0],case[1],word_table,child_pat)
    if tree is not None:
        res = trace_path(case[1],tree)
        run_results.append(res)
    else:
        run_results.append((0,"No Solution"))
end2 = time.perf_counter()

print("Time to solve puzzles: ", (end2-start2), " second")

print("Total run time: ", (end2-start))

for index,case in enumerate(run_results):
    print("Length: ",case[0])
    print("Path: \n",case[1])
