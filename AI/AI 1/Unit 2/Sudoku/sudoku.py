import string
import sys
def row_constr(N):
    row_sets = []
    for i in range(N):
        rset = set()
        for j in range(N):
            rset.add(i*N+j)
        row_sets.append(rset)
    return row_sets

def col_constr(N):
    col_sets = []
    for i in range(N):
        c_set = set()
        for j in range(N):
            c_set.add(N*j+i)
        col_sets.append(c_set)
    return col_sets

# bl_h == block heihgt
# bl_w = block width
# to find block:
def block_constr(N,bl_h,bl_w):
    blocks = dict()
    for i in range(0,N,bl_h):
        for j in range(0,N,bl_w):
            bloc_vals = set()
            top = i*N + j
            for r in range(bl_h):
                for j in range(bl_w):
                    bloc_vals.add(top+r*N+j)
            blocks[top] = bloc_vals
    return blocks

def count_symbols(state,symbol_set):
    count_dict = dict()
    for el in state:
        if el not in count_dict.keys():
            count_dict[el] = 1
        else:
            count_dict[el] += 1
    print(count_dict)

# state(the puzzle) will be converted into an array to make manipulation easier
def backtrack(state,N,bl_h, bl_w,rn,cn,bn,sym_set):

    next_space = get_next(state)
    if next_space == -1:
        return state
    for val in sorted_values(next_space,state,N,rn,cn,bn,bl_h,bl_w,sym_set): # if val if empty and there still is a "." then call naturally terminates
        # assign val to space
        state[next_space] = val
        # call result
        result = backtrack(state,N,bl_h,bl_w,rn,cn,bn,sym_set) 
        # if result is not None:
        if result is not None:
            return result
        else:
            state[next_space] = "."
    return None

def get_next(state):
    for i in range(len(state)):
        if state[i] == ".":
            return i
    return -1

def sorted_values(pos,state,N,row_neighbors,col_neighbors,block_neigh,bl_h,bl_w,symbol_set):
    row = pos//N
    col = pos%N
    block = (row//bl_h)*N * bl_h + (col//bl_w) * bl_w
    taken = set()
    for i in row_neighbors[row]:
        taken.add(state[i])
    for j in col_neighbors[col]:
        taken.add(state[j])
    for k in block_neigh[block]:
        taken.add(state[k])
    avalible = list()
    for s in symbol_set:
        if s not in taken:
            avalible.append(s)
    return avalible


def check_symbols(puzzle):
    syms = dict()
    for ch in puzzle:
        if ch in syms.keys():
            syms[ch] += 1
        else:
            syms[ch] = 1
    return syms

with open(sys.argv[1]) as f:
    test_cases = f.readlines()

def is_prime(num):
    factors = []
    for i in range(1,int(num**0.5)+1):
        if num%i == 0:
            factors.append(i)
            if num//i!= i:
                factors.append(num//i)
    factors.sort()
    return len(factors) == 2, factors

def get_symbols(N):
    symbols = set(("123456789"+ string.ascii_uppercase)[0:N])
    return symbols
def print_puzzle(puzzle,N,bloc_height,block_width):
    for i in range(N):
        for j in range(N):
            print(puzzle[i*N+j],end="")
            if j%block_width == block_width-1:
                print("|",end="")
            else:
                print(" ",end="")
        print() 
        if i%bloc_height == bloc_height-1:
            print("- "*N)
    
for case in test_cases:
    case = list(case)
    N = int(len(case)**0.5)
    prime, factors = is_prime(N)
    # print(factors)
    if prime:
        print("Invalid test case, prime number")
    mid = (len(factors)-1)//2
    if abs(factors[mid] - N**0.5) < 0.0000000001:
        subblock_height = factors[mid]
        subblock_width = factors[mid]
    else:
        subblock_height = factors[mid]
        subblock_width = factors[mid+1]
    # row neighors, column neighbors, block neighbors
    # print_puzzle(case,N,subblock_height,subblock_width)
    rn,cn,bln = row_constr(N),col_constr(N),block_constr(N,subblock_height,subblock_width)
    symbol_set = get_symbols(N)
    result = backtrack(case,N,subblock_height,subblock_width,rn,cn,bln,symbol_set)
    # print_puzzle(case,N,subblock_height,subblock_width)
    print("".join(result))




  
