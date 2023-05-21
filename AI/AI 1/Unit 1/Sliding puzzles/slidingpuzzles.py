
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
    visited = set()

    fringe.append((state,0,""))
    visited.add((state,0,""))
    # v = state, pathlength, path taken
    while len(fringe) > 0:
        # v is a tuple with path in it
        v = fringe.popleft()
        if goal_test(v[0]):
            return v
        children = get_children(v[0],size,v[1],v[2])
        for c in children:
            if c not in visited:
                fringe.append(c)
                visited.add(c)

    return None
def get_children(state,size,path,dir):
    states = []
    spot = state.find(".")
    row = spot//size
    col = spot%size
    if row - 1 >=0: #top
        toRet = swap(state,(row-1)*size + col,spot)
        states.append((toRet,path+1))

    if row + 1 < size: #down
        states.append((swap(state,(row+1)*size+col,spot),path+1))
    if col + 1 < size:#left
        states.append((swap(state,row*size+col+1,spot),path+1))

    if col -1 >=0:#right
        states.append((swap(state,row*size+col-1,spot),path+1))
    return states

def swap(s,i,j):
    arr = list(s)
    temp= arr[i]
    arr[i] = arr[j]
    arr[j] = temp
    return "".join(arr)

def steps_taken(state,seq,size):
    path = []
    for s in seq:
        spot = state.find(".")
        row = spot//size
        col = spot%size
        if s=="t": #top
            path.append(swap(state,(row-1)*size + col,spot))
    
        if s=="t": #down
            path.append(swap(state,(row+1)*size+col,spot))
        if s=="l":#left
            path.append(swap(state,row*size+col+1,spot))

        if s=="r":#right
            path.append(swap(state,row*size + col-1,spot))

    return path
# with open("slide_puzzle_tests.txt") as f:
#     vals = []
#     for line in f:
#         line = line.split()
#         vals.append((int(line[0]),line[1].rstrip()))
vals = [(2,"A.CB")]
for i,val in enumerate(vals):
    
    print("Line ",i," start state: ")
    print_puzzle(val[1],val[0])
    print("Line ",i," goal state: ")
    print_puzzle(find_goal(val[1]),val[0])
    result = BFSearch(val[1],val[0])
    print("Length of path: ",result[1])
    print("Path taken: ")
    for s in steps_taken(val[1],result[2],val[0]):
        print_puzzle(s,val[0])









