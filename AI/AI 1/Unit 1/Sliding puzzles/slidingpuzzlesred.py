
from collections import deque
import sys
import time
def print_puzzle(state,size):
    for k in range(size):
        for j in range(size):
            print(state[k*size+j],end=" ")
        print()

def find_goal(state):
    toRet = sorted(state)
    toRet = toRet[1:]
    toRet.append(".")
    return "".join([str(ch) for ch in toRet])

def goal_test(state):
    return state == find_goal(state)

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

def BFSearchHardest(state,size):
    fringe = deque()
    visited = dict()
    fringe.append(state)
    visited[state] = 0
    maxlen = 0
    # other information can be added using the corresponding array

    while len(fringe) > 0:
        v = fringe.popleft()
        if visited[v] > maxlen:
            maxlen = visited[v]
        children = get_children(v,size)
        for c in children:
            if c not in visited.keys():
                fringe.append(c)
                visited[c]=visited[v]+1

    return maxlen,visited

def biBFSearch(state,goal,size):
    #initiate relevant structures for each direction
    fringeStart = deque()
    visitedStart = dict()

    fringegoal = deque()
    visitedgoal = dict()

    #add relevant information to each array
    fringeStart.append(state)
    visitedStart[state] = [0,None]

    fringegoal.append(goal)
    visitedgoal[goal] = [0,None]
    # other information can be added using the corresponding array
    while len(fringeStart) > 0 and len(fringegoal) > 0:
        #pop left
        vs = fringeStart.popleft()
        vg = fringegoal.popleft()
        
        # get children
        childs = get_children(vs,size)
        childg = get_children(vg,size)

        # add to visited and fring if not processed. Also end search if child is in both
        for cs in childs:
            if (cs in visitedStart) and (cs in visitedgoal):
                return cs,visitedStart,visitedgoal

            if cs not in visitedStart:
                fringeStart.append(cs)
                visitedStart[cs] = [visitedStart[vs][0]+1,vs]

        for cg in childg:
            if (cg in visitedStart) and (cg in visitedgoal):
                return cg,visitedStart,visitedgoal
            
            if cg not in visitedgoal:
                fringegoal.append(cg)
                visitedgoal[cg] = [visitedgoal[vg][0]+1,vg]
    
    return None
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

def trace_path(end, path_taken):
    path = []
    step = end
    while step is not None:
        path.append(step)
        step = path_taken[step][1]

    return path



with open(sys.argv[1]) as f:
    tests = f.readlines()

    tests = [line.split() for line in tests]

    for t in range(len(tests)):
        tests[t][0] = int(tests[t][0])


for line,case in enumerate(tests):
    # run for bFS
    start = time.perf_counter()
    length = BFSearch(case[1],case[0])
    end = time.perf_counter()

    print("Line ",line,": ", case[1],", ",length," moves found in ",(end-start),"seconds for BFS")

    #run for biBFS
    start = time.perf_counter()
    midpoint,startdict,goaldict = biBFSearch(case[1],goal:=find_goal(case[1]),case[0])
    length = startdict[midpoint][0] + goaldict[midpoint][0]
    end = time.perf_counter()
    
    print("Line %s: %s, %s moves found in %s second for biBFS"%(line,case[1],length,(end-start)))

    print()











