"""
Uses method found here: https://towardsdatascience.com/computing-number-of-conflicting-pairs-in-a-n-queen-board-in-linear-time-and-space-complexity-e9554c0e0645
"""
import random
from collections import Counter
import time
# state is an array populated with N -1
# nested list set structure containing the conflicting diagonals(need to reset if does not work out)
#taken cols -- diagonals for each row that cannot be used
# used_col -- vertical columns which cannot be used


def backtrack(state,N,used_col:set,taken_cols,col_queens,posDiagQueens,negDiagQueens):
    """
    posDiagqueens: obtain diagonal by row + col
    negDiagQueens: obtain diagonal by N-1-row+col
    """
    if None not in state:
        return state
    # var is the row

    for row in range(N):
        vals = sorted_val(state,N,used_col,taken_cols,row)
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
        eliminate_diag(row,state[row],taken_cols,N)
    return state

# this function modifies the sets within a list containing the taken diagonal rows

def get_next(state):
    choices = []
    for i in range(len(state)):
        if state[i] is None:
            choices.append(i)
    return random.choice(choices)
def eliminate_diag(row,curr_val,taken,N):
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


def sorted_val(state,N,nums,taken,row):
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
    res=backtrack(initial,N,set(),taken,colQueens,posDiagQueens,negDiagQueens)
    # bactrack has no issue ad
    # colQueens= [1, 1, 1, 2, 1, 0, 1, 1]
    # posDiagQueens= [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 2, 1, 0, 0, 0]
    # negDiagQueens=  [0, 0, 0, 1, 1, 2, 0, 1, 1, 0, 1, 0, 1, 0, 0]
    # res = [1, 6, 2, 0, 7, 3, 4, 3]
    # res = [0,0,0,0]
    # colQueens = [4,0,0,0]
    # posDiagQueens = [1,1,1,1,0,0,0]
    # negDiagQueens = [1,1,1,1,0,0,0]
    # test with a nonconflictnig board
    # res = [2,0,3,1]
    # colQueens = [1,1,1,1]
    # posDiagQueens = [0,1,1,0,1,1,0]
    # # negDiagQueens = [0,1,1,0,1,1,0]
    # print("Conflict: ",total_conflict(res,N,colQueens,posDiagQueens,negDiagQueens))
    # print("colQueens: ",colQueens)
    # print("posDiagDiagQueens:",posDiagQueens)
    # print("negDiagQueens: ",negDiagQueens)
    # print("Initial",res)
    # print("count conflict for row 0",count_conflict(N,3,res[3],colQueens,posDiagQueens,negDiagQueens))
    conf = total_conflict(res,N,colQueens,posDiagQueens,negDiagQueens)
    inc_repair(res,N,colQueens,posDiagQueens,negDiagQueens,conf)
    print("Verification for N=",N,":",test_solution(res))
    # print(res)
    # remove_queen(res,0,N,colQueens,posDiagQueens,negDiagQueens)
    # print("Queens removed",res)
    # print("colQueens: ",colQueens)
    # print("posDiagDiagQueens:",posDiagQueens)
    # print("negDiagQueens: ",negDiagQueens)
    # print("res",res)


    # print("adding queen")
    # add_queen(res,N,0,0,colQueens,posDiagQueens,negDiagQueens)
    # print("adding queen",res)
    # print("colQueens: ",colQueens)
    # print("posDiagDiagQueens:",posDiagQueens)
    # print("negDiagQueens: ",negDiagQueens)
    
    # print("res",res)
    # print(count_conflict(N,0,0,colQueens,posDiagQueens,negDiagQueens))
    # print("Verification: ",test_solution(res))
    return res


start = time.perf_counter()
call_repair(200)
# call_repair(94)
# end = time.perf_counter()
start = time.perf_counter()
for N in range(8,201):
    call_repair(N)
end = time.perf_counter()
print("Seconds taken: ",(end-start))
# solutions = []
# while time.perf_counter()-start < 30:
#     solutions.append(call_repair(N))
#     N += 1

# for i in range(len(solutions)):
#     print("Verification for N=",(i+8),": ",test_solution(solutions[i]))

