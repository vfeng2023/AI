
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

    fringe.append(state)
    visited.add(state)
    while len(fringe) > 0:
        v = fringe.popleft()
        children = get_children(v,size)
        for c in children:
            if c not in visited:
                fringe.append(c)
                visited.add(c)

    print(len(visited))
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
    return tuple(states)

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
    
    # print("Line ",i," start state: ")
    # print_puzzle(val[1],val[0])
    # print("Line ",i," goal state: ")
    # print_puzzle(find_goal(val[1]),val[0])
    # print()

    # print("Line ",i," children: ")
    # for child in get_children(val[1],val[0]):
    #     print_puzzle(child,val[0])
    #     print()
    BFSearch(val[1],val[0])








