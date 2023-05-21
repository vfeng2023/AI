import random
from collections import Counter
import time
# state is an array populated with N -1
# nested list Counter structure containing the conflicting diagonals(need to reset if does not work out)
#taken cols -- diagonals for each row that cannot be used
# used_col -- vertical columns which cannot be used
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
        print("N=",N," overtime")
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
    Return the index of the row with least choices that is NOT 1 element.
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


def call_backtrack(size):
    N = size 
    initial = [{j for j in range(N)} for i in range(N)]
    start = time.perf_counter()
    try:
        res = backtrack(initial,N,[],start)
    except Exception as e:
        res = call_repair(N)
    
    end = time.perf_counter()
    print("Size =",N, "solution ",res," found in ",(end-start), " seconds.")
    resfinal = []
    for r in res:
        if type(r) == set:
            for first in r:
                break
        else:
            first = r
        resfinal.append(first)
    print("Verification: ", test_solution(resfinal))
    print()

"""
Functions necessary for incremental repair
"""
def backtrack_gen(state,N,col_conflicts,diag_conf):
    # var is the row

    for row in range(N):
        val = chooseNext(state,N,row,col_conflicts,diag_conf)
        state[row] = val
        add_diag(row,val,diag_conf,N)
        col_conflicts[val] += 1


    return state

def chooseNext(state,N,row,col_conf,diag_conf):
    """
    Precondition: row is None
    Iterates through each row. determines the column with minconflict
    """
    minconf = N+100
    mincol = 0
    for col in range(N):
        if count_conflict(state,N,row,col,col_conf,diag_conf,False) < minconf:
            mincol = col
    return 0

def add_diag(row,col,diag_conf,N):
    diff = min(row,col)
    diag = (row-diff,col-diff)
    diag_conf[diag] += 1
    # add one to diagonals running against 
    diff2 = N-1-col
    new_row = row- diff2
    if new_row >=0:
        diag_conf[(new_row,N-1)] += 1
def remove_diag(row,col,diag_conf,N):
    diff = min(row,col)
    diag = (row-diff,col-diff)
    diag_conf[diag] -= 1
    # add one to diagonals running against 
    diff2 = N-1-col
    new_row = row- diff2
    if new_row >=0:
        diag_conf[(new_row,N-1)] -= 1
def get_diag(row,col,diag_conf,N):
    diff = min(row,col)
    diag = (row-diff,col-diff)
    # add one to diagonals running against 
    diff2 = N-1-col
    new_row = row- diff2
    if new_row >=0:
        (diag,(new_row,diff2))

    return (diag,None)
def count_conflict(state,N,row,col,col_conf,diag_conf,isPlaced):
    """
    returns the number of conflict in a particular row and column.
    Mantains backing [set,set,set,...] that is bidirectional for conflict/
    Count conflict would merely return the length of a particular list
    When queen is placed in a column, counter of the column increases by 1
    Number of diagonals = 2n-1
    diagonals determined by coordinates (r,c) of uppermost row and leftmost column
    the diagonal of a particular square is found by:
        diff = min(r,c)
        diag = (r-diff, c-diff)
    finding the conflict resulting from placing a queen in a particular square is the sum of the diagonal and vertical conflicts
    finding the conflict in a row is the sum of all of the conflicts of the columns in that row.
    diagonal and vertical conflicts are the number of queens in a square
    111
    101
    111
    diagonals defined as running from the edges downward. The ones on the right border likewise run downward 
    """
    val = get_diag(row,col,diag_conf,N)
    print(val)
    diag1,diag2 = val
    conf = col_conf[col] + diag_conf[diag1]
    if diag2 is not None:
        conf+= diag_conf[diag2]
    if isPlaced: # to exclude the piece itself if one is placed is (r,c)
        conf -= 2

    return conf

def row_conflict(state,row,N,col_conf,diag_conf):
    total = 0
    for col in range(N):
        total += count_conflict(state,N,row,col,col_conf,diag_conf,col == state[row])
    return total
def total_conflict(state,N,col_conf,diag_conf):
    total = 0
    for r in range(len(state)):
        total += row_conflict(state,r,N,col_conf,diag_conf)
def inc_repair(state,N,conflict,col_conf,diag_conf):
    """
    # determine the row with the most total conflict
    # find the the column in that row with the least conflict
    # swap the values
    # repeat until there are no more conflicting values
    """
    # find row with most conflicts
    while conflict > 0:
        max_rows = []
        biggest = 0
        for i in range(N):
            count = row_conflict(state,i,N,col_conf,diag_conf)
            if count == biggest:
                max_rows.append(i)
            elif count > biggest:
                biggest = count
                max_rows= [i]
        fix = random.choice(max_rows)

        # determine col in that row with the least
        minconf = N + 100
        min_col = []
        for col in range(N):
            conf = count_conflict(state,N,fix,col,col_conf,diag_conf,state[fix] == col)
            if conf == minconf:
                min_col.append(col)
            else:
                minconf = conf
                min_col = [col]

        # remove the queen from records of diag_conf and col_conf
        remove_diag(fix,state[fix],diag_conf,N)
        col_conf[state[fix]] -=1
        # replace that row with that
        state[fix] = random.choice(min_col)
        add_diag(fix,state[fix],diag_conf,N)
        col_conf[state[fix]] -= 1
        # call in repair again until conflict reaches 0
        total=total_conflict(state,N)
        conflict = total
    return state

def call_repair(N):   
    initial = [None for i in range(N)]
    col_conflicts = [0 for _ in range(N)]
    diag_conf = dict()
    #necessary horizontal and vertical adjustments for diag_conf
    for i in range(N):
        diag_conf[(0,i)] = 0
        diag_conf[(i,0)] = 0
        diag_conf[(i,N-1)] = 0
    res = backtrack_gen(initial,N,col_conflicts,diag_conf)
    total = total_conflict(res,N)
    inc_repair(res,N,total)
    return res

print(call_repair(4))
# start = time.perf_counter()
# for i in range(8,201):
#     call_backtrack(i)
# # call_backtrack(112)
# # stops being fast at 111 going forward
# # for i in range(200,8,-1):
# #     call_backtrack(i)
# end = time.perf_counter()
# # stops at 181 going in reverse
# print("Total time= ",(end-start), " seconds")