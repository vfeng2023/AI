import sys
from collections import deque
import time
from heapq import heappush,heappop,heapify

# returns true if puzzle solvable
def parity_check(puzzle,size):
    stop = puzzle.find(".")
    row = stop//size
    puzzle = puzzle[:stop] + puzzle[stop+1:]

    # determine out of order pairs
    count = 0
    for i in range(len(puzzle)):
        for j in range(i+1,len(puzzle)):

            if puzzle[i] > puzzle[j]:
                count += 1

    if size%2 == 1:
        return count%2 == 0

    else:
        return (row%2 == 0 and count%2 == 1) or (row%2 == 1 and count%2==0)

def find_goal(state):
    toRet = sorted(state)
    toRet = toRet[1:]
    toRet.append(".")
    return "".join([str(ch) for ch in toRet])

def goal_test(state):
    return state == find_goal(state)

def get_children(state,size):
    states = []
    spot = state.find(".")
    row = spot//size
    col = spot%size
    if row - 1 >=0:
        toRet = swap(state,(row-1)*size + col,spot)
        states.append(toRet)

    if row + 1 < size:
        states.append(swap(state,(row+1)*size+col,spot))
    if col + 1 < size:
        states.append(swap(state,row*size+col+1,spot))

    if col -1 >=0:
        states.append(swap(state,row*size+col-1,spot))
    return states

def swap(s,i,j):
    arr = list(s)
    temp= arr[i]
    arr[i] = arr[j]
    arr[j] = temp
    return "".join(arr)

def kDFSearch(start,k,size):
    fringe = list()
    start_state = start
    start_depth = 0
    start_ancestors = set()
    start_ancestors.add(start)
    fringe.append((start_state,start_depth,start_ancestors))

    while len(fringe) > 0:
        state,depth,ancestors = fringe.pop()
        if goal_test(state):
            return depth

        if depth < k:
            children = get_children(state,size)
            for c in children:
                if c not in ancestors:
                    new_ancestors = ancestors.copy()
                    new_ancestors.add(c)
                    fringe.append((c,depth+1,new_ancestors))
    return None

def iterDFSearch(start,size):
    max_depth = 0
    result = None
    while result is None:
        result = kDFSearch(start,max_depth,size)
        max_depth += 1

    return result

def BFSearch(state,size):
    fringe = deque()
    visited = dict()
    fringe.append(state)
    visited[state] = [0,None]
    # other information can be added using the corresponding array

    while len(fringe) > 0:
        v = fringe.popleft()
        if goal_test(v):
            return visited[v][0]
        children = get_children(v,size)
        for c in children:
            if c not in visited.keys():
                fringe.append(c)
                visited[c]=[visited[v][0]+1,v]

    return None

def a_star(start,size):
    mappings = letter_to_index()
    closed = set()
    start_depth = 0
    f = taxicab(start,size,mappings)
    fringe = list()
    heapify(fringe)
    heappush(fringe,(f,start,start_depth))
    while(len(fringe) > 0):
        f,state,depth = heappop(fringe)
        if goal_test(state):
            return depth
        if state not in closed:
            closed.add(state)
            children = get_children(state,size)
            for child in children:
                if child not in closed:
                    heappush(fringe,(depth + taxicab(child,size,mappings),child,depth+1))
    return None
        
def letter_to_index():
    alpha_to_index = dict()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for index,letter in enumerate(alpha):
        alpha_to_index[letter] = index
    return alpha_to_index
def taxicab(puzzle,size,indices):
    """
    To improve this heurestic:
    - take parent state, and move required to get to current state from parent state
    - determine if the change moves the moved tile closer or further from the goal state
    """
    if puzzle[0].isdigit() or puzzle[1].isdigit():
        indices = {ch:int(ch) for ch in puzzle if ch!="."}

    distance = 0
    for i in range(len(puzzle)):
        if puzzle[i]!=".":
            index = indices[puzzle[i]]
            cor_r = index//size
            cor_c = index%size

            curr_r = i//size
            curr_c = i%size

            distance += (abs(curr_r-cor_r)+abs(curr_c-cor_c))
    return distance


with open(sys.argv[1]) as f:
    tests = f.readlines()

    tests = [line.strip().split() for line in tests]
    for t in range(len(tests)):
        tests[t][0] = int(tests[t][0])


def call_BFS(puzzle,size,line):
        start = time.perf_counter()
        length = BFSearch(puzzle,size)
        end = time.perf_counter()

        print("Line ",line,": ", case,", ",length," moves found in ",(end-start),"seconds")

def call_iterDFS(case,size,line):
    start2 = time.perf_counter()
    length2 = iterDFSearch(case,size)
    end2 = time.perf_counter()

    print("Line ",line,": ", case,", ",length2," moves found in ",(end2-start2),"seconds")

def call_astar(case,size,line):
    start3 = time.perf_counter()
    length3 = a_star(case,size)
    end3 = time.perf_counter()
    print("Line ",line, ": ", case,", ",length3,"moves found in ",(end3-start3)," seconds")


for line,case in enumerate(tests):

    #testing puzzles in 15 for BFS and DFS
    size,puzzle,calls = case
    start = time.perf_counter()
    isSolvable = parity_check(puzzle,size)
    end = time.perf_counter()
    if isSolvable:

        if calls == "B":
            call_BFS(puzzle,size,line)

        elif calls == "I":
            call_iterDFS(puzzle,size,line)

        elif calls == "A":
            call_astar(puzzle,size,line)

        else:
            call_BFS(puzzle,size,line)
            call_iterDFS(puzzle,size,line)
            call_astar(puzzle,size,line)

    else:
        print("Line ",line,": ",puzzle," has no solution found in",(end-start)," seconds")

    print()

