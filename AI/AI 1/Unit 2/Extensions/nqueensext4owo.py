"""
Uses method of storage for auxillary information about diagonals found here:
https://towardsdatascience.com/computing-number-of-conflicting-pairs-in-a-n-queen-board-in-linear-time-and-space-complexity-e9554c0e0645
"""
import random
from collections import Counter
import time
"""
Overtime for 112, 113, 118,127, 163, 165,166, 180
Strategy for solving Nqueens:
1. Replace get_next function with one that returns the row with minimum conflict and length greater than one
2. implement a forward looking function that eliminates options based on placement
3. try adding a constraint satisfaction function(Although this doesn't seem very useful)
4. Combine the used_col and taken col to be encoded in state
"""

def backtrack(state,N,solved,start):
    """
    The bactracking function executes forward looking on owowowowo
    """
    # var is the row
    if time.perf_counter()-start > 0.5:
        raise Exception("Overtime")
        return None
    var = get_next(state)
    if var == -1:
        return state
    for val in sorted_val(state,var):
        new_board = [state[i].copy() for i in range(N)]
        new_board[var] = {val}
        solved.append(var)
        new_board = eliminate_diag(solved,new_board,N)
        if new_board is not None:
        # print(taken_cols)
        # input()
            result = backtrack(new_board,N,solved.copy(),start)
            if result is not None:
                return result
    return None


# this function modifies the sets within a list containing the taken diagonal rows
def get_next(state):
    """
    Return the index of the row with minimum conflict conflict that is NOT 1 element.
    If the set associated with a row is empty, solution does not work. Return -1
    """
    minlen = 10000000
    index = -1
    for i in range(len(state)):
        if (l:=len(state[i])) > 1 and l < minlen:
            minlen = l
            index = i
    return index
    
def eliminate_diag(rows,state,N):
    """
    rows - a list of rows that have already been solved
    state [set,set,set,set,...]
    N - len(state) the size of the board
    Eleminates the diagonals associated with a particular row by getting rid of column values as a particular choice
    Calls forward looking on the rows given
    Returns none if a row ends up empty
    """
    while len(rows) > 0:
        row = rows.pop()
        for curr_val in state[row]:
            break
        # eliminates the row values
        for r1 in range(len(state)):
            if r1!=row:
                if curr_val in state[r1]:
                    state[r1].remove(curr_val)
                    if len(state[r1]) == 0:
                        return None
                    if len(state[r1]) == 1:
                        rows.append(r1)
        # eliminates elemnt from diagonals
        r = row+1
        col = curr_val+1
        # take right down diagonals
        while r < N and col < N:
            if col in state[r]:
                state[r].remove(col)
                if len(state[r]) == 0:
                    return None
                if len(state[r]) == 1:
                    rows.append(r)
            r += 1
            col += 1

        # take left up diagonals
        r = row - 1
        col = curr_val-1
        while r >= 0 and col >=0:
            if col in state[r]:
                state[r].remove(col)
                if len(state[r]) == 0:
                    return None
                if len(state[r]) == 1:
                    rows.append(r)
            r -= 1
            col -= 1

        # take right up diagonals
        r = row - 1
        col = curr_val+1
        while r >= 0 and col < N:
            if col in state[r]:
                state[r].remove(col)
                if len(state[r]) == 0:
                    return None
                if len(state[r]) == 1:
                    rows.append(r)
            r -= 1
            col += 1

        # take left down diagonals
        r = row + 1
        col = curr_val-1
        while r < N and col >= 0:
            if col in state[r]:
                state[r].remove(col)
                if len(state[r]) == 0:
                    return None
                if len(state[r]) == 1:
                    rows.append(r)
            r += 1
            col -= 1
    return state


def sorted_val(state,row):
    return state[row]


def goal_test(state, N):
    if len(state) > N:
        return False
    
    for r in range(len(state)):
        val = state[r]
        if val is None:
            return False
        left = val-1
        right = val + 1
        for i in range(r+1,len(state)):
            if val == state[i]:
                return False
            if left >=0 and state[i] == left:
                return False

            if right < N and state[i] == right:
                return False

            left -= 1
            right += 1

    return True



def call_backtrack(size):
    N = size 
    initial = [{j for j in range(N)} for i in range(N)]
    start = time.perf_counter()
    try:
        res = backtrack(initial,N,[],start)
    except Exception as e:
        # print(e)
        res = call_repair(N)
    return res

"""Functions necessary for incremental repari"""
def backtrackForInc(state,N,used_col:set,taken_cols,col_queens,posDiagQueens,negDiagQueens):
    """
    posDiagqueens: obtain diagonal by row + col
    negDiagQueens: obtain diagonal by N-1-row+col
    """
    if None not in state:
        return state
    # var is the row

    for row in range(N):
        vals = sorted_valForInc(state,N,used_col,taken_cols,row)
        if len(vals) > 0:
            state[row] = random.choice(vals)
        else:
            state[row] = random.randint(0,N-1)
        col_queens[state[row]] += 1
        posDiag = row + state[row]
        negDiag = N-1-row + state[row]
        posDiagQueens[posDiag] += 1
        negDiagQueens[negDiag] += 1
        used_col.add(state[row])
        eliminate_diag_backtrack(row,state[row],taken_cols,N)
    return state

# this function modifies the sets within a list containing the taken diagonal rows

def eliminate_diag_backtrack(row,curr_val,taken,N):
    r = row+1
    col = curr_val+1
    # take right down diagonals
    while r < N and col < N:
        taken[r][col] += 1
        r += 1
        col += 1

    # take left up diagonals
    r = row - 1
    col = curr_val-1
    while r >= 0 and col >=0:
        taken[r][col] += 1
        r -= 1
        col -= 1

    # take right up diagonals
    r = row - 1
    col = curr_val+1
    while r >= 0 and col < N:
        taken[r][col] += 1
        r -= 1
        col += 1

    # take left down diagonals
    r = row + 1
    col = curr_val-1
    while r < N and col >= 0:
        taken[r][col] += 1
        r += 1
        col -= 1


def sorted_valForInc(state,N,nums,taken,row):
    avalible = []
    for i in range(N):
        if i not in nums and (taken[row][i] <= 0):
            avalible.append(i)
    return avalible


def nextToRepair(state,N,colQueens,posDiagQueens,negDiagQueens):
    # 
    maxconf = 0
    index = []
    for r in range(N):
        conf = count_conflict(N,r,state[r],colQueens,posDiagQueens,negDiagQueens)
        if conf > maxconf:
            maxconf = conf
            index = [r]
        elif conf == maxconf:
            index.append(r)
    if maxconf <= 0:
        return None
    else:
        return index
def count_conflict(N,row,column,colQueens,posDiagQueens,negDiagQueens):
    """
    0 <=row < N, 0<=col< N
    
    """
    posDiag = row + column
    negDiag = N-1-row + column
    # queens * (queens-1) / 2 for a particular row, column, diagonal
    total = colQueens[column]*(colQueens[column]-1)//2
    total += (posDiagQueens[posDiag]*(posDiagQueens[posDiag]-1)//2)
    total += (negDiagQueens[negDiag] * (negDiagQueens[negDiag]-1)//2)
    return total

def total_conflict(state,N,colQueens,posDiagQueens,negDiagQueens):
    count = 0
    # for r in range(N):
    #     count += count_conflict(N,r,state[r],colQueens,posDiagQueens,negDiagQueens)
    # return count
    # total conflict finds the total pairs of conflicting queens
    for i in range(len(colQueens)):
        count += ((colQueens[i])*(colQueens[i]-1)//2)
    for j in range(len(posDiagQueens)):
        count += ((posDiagQueens[j])*(posDiagQueens[j]-1)//2)
        count += ((negDiagQueens[j]) * (negDiagQueens[j]-1)//2)
    return count

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True

def remove_queen(state,row,N,colQueens,posDiagQueens,negDiagQueens):
    posDiag = row + state[row]
    negDiag = N-1-row + state[row]
    colQueens[state[row]] -= 1
    posDiagQueens[posDiag] -= 1
    negDiagQueens[negDiag] -=1
    state[row] = None

def add_queen(state,N,row,col,colQueens,posDiagQueens,negDiagQueens):
    state[row] = col
    posDiag = row + col
    negDiag = N-1-row + col
    colQueens[state[row]] += 1
    posDiagQueens[posDiag] += 1
    negDiagQueens[negDiag] +=1


def inc_repair(state,N,colQueens,posDiagQueens,negDiagQueens,totalConf):
    while totalConf > 0:
        maxconf = 0
        maxrow = []
        # find the row with most conflict
        for r in range(N):
            conf = count_conflict(N,r,state[r],colQueens,posDiagQueens,negDiagQueens)
            if conf == maxconf:
                maxrow.append(r)
            elif conf > maxconf:
                maxconf = conf
                maxrow = [r]
                
        nextspace = random.choice(maxrow)

        # find index in row with least conflict
        minconf = N+100
        index = []
        original = state[nextspace]

        for col in range(N):
            remove_queen(state,nextspace,N,colQueens,posDiagQueens,negDiagQueens)
            add_queen(state,N,nextspace,col,colQueens,posDiagQueens,negDiagQueens)
            conf = count_conflict(N,nextspace,state[nextspace],colQueens,posDiagQueens,negDiagQueens)
            if conf < minconf:
                minconf = conf
                index = [col]
                
            elif conf == minconf:
                index.append(col)


        
        mincol = random.choice(index)
            # print(state)
            # totalConf = total_conflict(state,N,colQueens,posDiagQueens,negDiagQueens)
        remove_queen(state,nextspace,N,colQueens,posDiagQueens,negDiagQueens)
        add_queen(state,N,nextspace,mincol,colQueens,posDiagQueens,negDiagQueens)
        totalConf = total_conflict(state,N,colQueens,posDiagQueens,negDiagQueens)
        # print(state," total confilct", totalConf)
    return state

def call_repair(N):   
    initial = [None for i in range(N)]
    taken = [Counter() for _ in range(N)]
    colQueens = [0 for i in range(N)]
    posDiagQueens = [0 for i in range(2*N-1)]
    negDiagQueens = [0 for i in range(2*N-1)]
    res=backtrackForInc(initial,N,set(),taken,colQueens,posDiagQueens,negDiagQueens)
    # bactrack has no issue ad
    conf = total_conflict(res,N,colQueens,posDiagQueens,negDiagQueens)
    inc_repair(res,N,colQueens,posDiagQueens,negDiagQueens,conf)
    # print("Verification for N=",N,":",test_solution(res))
    return res


start = time.perf_counter()
solved = []
N = 8
while time.perf_counter() - start < 30:
    sol = call_backtrack(N)
    # print("N=",N,", solution: ",sol)
    solved.append(sol)
    N += 1

for i in range(len(solved)):
    size = len(solved[i])
    new_puzzle = []
    if type(solved[i][0]) is set:
        for s in solved[i]:
            for first in s:
                break
            new_puzzle.append(first)
    else:
        new_puzzle = solved[i]
    print("Test solution for N=",size,": ",test_solution(new_puzzle))

# print(call_backtrack(180))