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

# used for forward looking
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

def constr_loop(state,cleared_squares,constr_set,symbol_set):
    row_symbols = dict()
    for ind in constr_set:
        for s in state[ind]:
            if s in row_symbols:
                row_symbols[s].append(ind)
            else:
                row_symbols[s] = [ind]
    for syms in symbol_set:
        if syms not in row_symbols:
            return None
        else:
            if len(row_symbols[syms]) == 1:
                index = row_symbols[syms][0]
                if len(state[index]) > 1:
                    state[index] = syms
                    cleared_squares.append(index)
    return cleared_squares
# constraint propagation : returns a list of cleared indices. if failure, returns None
def constr(state,N,rn,cn,bn,symbol_set,bl_h,bl_w): # rn and cn: [set] bn - dict(int:set())
    cleared_squares = []
    for constr_set in (rn,cn):
        for i in range(len(constr_set)):
            if constr_loop(state,cleared_squares,constr_set[i],symbol_set) is None:
                return None

    for k in bn.keys():
        if constr_loop(state,cleared_squares,bn[k],symbol_set) is None:
            return None
    return forward(state,N,bl_h,bl_w,rn,cn,bn,cleared_squares)

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
        # constr_cleared = constr(new_board,N,bl_h,bl_w,rn,cn,bn,sym_set)
        # while constr_cleared is not None:
        #     checked = forward(new_board,N,bl_h,bl_w,rn,cn,bn,constr_cleared)
        #     constr_cleared = constr(new_board,N,bl_h,bl_w,rn,cn,bn,sym_set)
        # call result
        if checked is not None:
            constraint_board = constr(checked,N,rn,cn,bn,sym_set,bl_h,bl_w)
            if constraint_board is not None:
                result = backtrack(constraint_board,N,bl_h,bl_w,rn,cn,bn,sym_set) 
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
        if len(state[i]) == 0:
            return -1
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
    return list(state[pos])


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
# test_cases = ["................"]

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
    print(case)
    forward(case,N,subblock_height,subblock_width,rn,cn,bln,solved_square)
    print(case)
    result = backtrack(case,N,subblock_height,subblock_width,rn,cn,bln,symbol_set)
    # print_puzzle(case,N,subblock_height,subblock_width)
    print("".join(result))

end = time.perf_counter()
  
