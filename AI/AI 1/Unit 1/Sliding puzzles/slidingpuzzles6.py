
from collections import deque
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
            return visited[v][0],visited
        children = get_children(v,size)
        for c in children:
            if c not in visited.keys():
                fringe.append(c)
                visited[c]=[visited[v][0]+1,v]

    return None,visited

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


#hardest puzzle
length,paths = BFSearchHardest("12345678.",3)

print("Length: ",length)

print("Puzzles: ")
for p in paths.keys():
    if paths[p] == 31:
        print_puzzle(p,3)
        print()












