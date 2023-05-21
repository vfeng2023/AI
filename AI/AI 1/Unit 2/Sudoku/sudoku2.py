import string
import sys
from collections import deque
import time
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

# given position, N, block height, block width, returns relevant neighbor information
def get_location(pos,N,bl_h,bl_w):
    row = pos//N
    col = pos%N
    block = (row//bl_h)*N * bl_h + (col//bl_w) * bl_w
    return row,col,block
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
# removes a value from a string

def remove(ch,string):
    chs = list(string)
    for i in range(len(chs)):
        if chs[i] == ch:
            chs[i] = ""
    return "".join(chs)


def count_symbols(state,symbol_set):
    count_dict = dict()
    for el in state:
        if el not in count_dict.keys():
            count_dict[el] = 1
        else:
            count_dict[el] += 1
    print(count_dict)


def forward(state,N,bl_h,bl_w,rn,cn,bn,solved_square):

    while len(solved_square) > 0:
        s = solved_square.pop()
        row,col,block = get_location(s,N,bl_h,bl_w)

        for neigh in rn[row],cn[col],bn[block]:
            for j in neigh:
                if j!=s:
                    old = len(state[j])
                    state[j] = remove(state[s],state[j])
                    if len(state[j]) == 0:
                        return None
                    if old > len(state[j]) and len(state[j]) == 1:
                        solved_square.append(j)
    return state
        

# state(the puzzle) will be converted into an array to make manipulation easier
def backtrack(state,N,bl_h, bl_w,rn,cn,bn,sym_set):

    next_space = get_next(state)
    if next_space == -1:
        return state
    for val in sorted_values(next_space,state,N,rn,cn,bn,bl_h,bl_w,sym_set): # if val if empty and there still is a "." then call naturally terminates
        # assign val to space
        new_board = state.copy()
        new_board[next_space] = val
        checked = forward(new_board,N,bl_h,bl_w,rn,cn,bn,[next_space])
        # call result
        if checked is not None:
            result = backtrack(new_board,N,bl_h,bl_w,rn,cn,bn,sym_set) 
            # if result is not None:
            if result is not None:
                return result
    return None

def get_next(state):
    # minIndex = 
    # for i in range(1,len(state)):
    #     if len(state[i]) > 1 and len(state[i])>len(state[minIndex]):
    #         minIndex = i
    # return minIndex
    minlen = 1000000
    index = -1
    for i in range(0,len(state)):
        if len(state[i]) > 1 and len(state[i]) < minlen:
            minlen = len(state[i])
            index = i
    return index

def goal_test(s):
    for ch in s:
        if len(ch)!=1:
            return False
    return True

def sorted_values(pos,state,N,row_neighbors,col_neighbors,block_neigh,bl_h,bl_w,symbol_set):
    row = pos//N
    col = pos%N
    block = (row//bl_h)*N * bl_h + (col//bl_w) * bl_w
    taken = set()
    for i in row_neighbors[row]:
        if len(state[i]) == 1:
            taken.add(state[i])
    for j in col_neighbors[col]:
        if len(state[j]) == 1:
            taken.add(state[j])
    for k in block_neigh[block]:
        if len(state[j]) == 1:
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
    test_cases = [line.strip() for line in f.readlines()]
# test_cases = [".912..5....54........3.89.4.3....1.515.....292.9....3.9.86.7........46....2..149."]
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
    symbols = ("123456789"+ string.ascii_uppercase)[0:N]
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

start = time.perf_counter()
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

    symbols = get_symbols(N)
    for i in range(len(case)):
        if case[i] == ".":
            case[i] = symbols

    # row neighors, column neighbors, block neighbors
    # print_puzzle(case,N,subblock_height,subblock_width)
    rn,cn,bln = row_constr(N),col_constr(N),block_constr(N,subblock_height,subblock_width)
    symbol_set = set(symbols)
    solved_square = []
    for i in range(len(case)):
        if len(case[i]) == 1:
            solved_square.append(i)
    # print(case)
    forward(case,N,subblock_height,subblock_width,rn,cn,bln,solved_square)
    # print(case)
    result = backtrack(case,N,subblock_height,subblock_width,rn,cn,bln,symbol_set)
    # print_puzzle(case,N,subblock_height,subblock_width)
    print("".join(result))

end = time.perf_counter()
print("solve in ",(end-start),"seconds")
  
