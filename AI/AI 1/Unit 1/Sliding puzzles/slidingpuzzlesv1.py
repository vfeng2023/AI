
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

    start_node = (state,0,None)
    fringe.append(start_node)
    visited.add(start_node)

    while len(fringe) > 0:
        # v is a tuple with path in it
        v = fringe.popleft()
        if goal_test(v[0]):
            return v
        children = get_children(v[0],size,v[1],v)
        for c in children:
            if c not in visited:
                fringe.append(c)
                visited.add(c)

    return None
def get_children(state,size,path,parent):
    states = []
    spot = state.find(".")
    row = spot//size
    col = spot%size
    if row - 1 >=0:
        toRet = swap(state,(row-1)*size + col,spot)
        states.append((toRet,path+1,parent))

    if row + 1 < size:
        states.append((swap(state,(row+1)*size+col,spot),path+1,parent))
    if col + 1 < size:
        states.append((swap(state,row*size+col+1,spot),path+1,parent))

    if col -1 >=0:
        states.append((swap(state,row*size+col-1,spot),path+1,parent))
    return states

def find_children(v):
    path = []
    while v[2] is not None:
        path.append(v[0])
        v = v[2]

    path.reverse()
    return path
        

def swap(s,i,j):
    arr = list(s)
    temp= arr[i]
    arr[i] = arr[j]
    arr[j] = temp
    return "".join(arr)

# with open("slide_puzzle_tests.txt") as f:
#     vals = []
#     for line in f:
#         line = line.split()
#         vals.append((int(line[0]),line[1].rstrip()))

vals = [(2,"3.12")]
for i,val in enumerate(vals):
    
    print("Line ",i," start state: ")
    print_puzzle(val[1],val[0])
    print("Line ",i," goal state: ")
    print_puzzle(find_goal(val[1]),val[0])
    result = BFSearch(val[1],val[0])
    print("length of path: ",result[1])
    # print("Path taken: ",find_children(result))