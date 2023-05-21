import random
from collections import Counter
import time
# state is an array populated with N -1
# nested list Counter structure containing the conflicting diagonals(need to reset if does not work out)
#taken cols -- diagonals for each row that cannot be used
# used_col -- vertical columns which cannot be used
"""
Strategy for solving Nqueens:
1. Replace get_next function with one that returns the row with minimum conflict and length greater than one
2. implement a forward looking function that eliminates options based on placement
3. try adding a constraint satisfaction function(Although this doesn't seem very useful)
4. Combine the used_col and taken col to be encoded in state
"""

def backtrack(state,N,solved):
    """
    The bactracking function executes forward looking on owowowowo
    """
    # var is the row
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
            result = backtrack(new_board,N,solved.copy())
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

def reset_diag(row,curr_val,taken,N):
    """
    No longer needed since making copies of new board states
    """
    r = row+1
    col = curr_val+1
    # take right down diagonals
    while r < N and col < N:
        taken[r][col] -= 1
        r += 1
        col += 1

    # take left up diagonals
    r = row - 1
    col = curr_val-1
    while r >= 0 and col >=0:
        taken[r][col] -=1
        r -= 1
        col -= 1

    # take right up diagonals
    r = row - 1
    col = curr_val+1
    while r >= 0 and col < N:
        taken[r][col]-=1
        r -= 1
        col += 1

    # take left down diagonals
    r = row + 1
    col = curr_val-1
    while r < N and col >= 0:
        taken[r][col]-=1
        r += 1
        col -= 1

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
    res = backtrack(initial,N,[])
    end = time.perf_counter()
    print("Size =",N, "solution ",res," found in ",(end-start), " seconds.")
    resfinal = []
    for r in res:
        for first in r:
            break
        resfinal.append(first)
    print("Verification: ", test_solution(resfinal))
    print()

start = time.perf_counter()
# for i in range(8,201):
#     call_backtrack(i)
# call_backtrack(35)
call_backtrack(116)

end = time.perf_counter()

print("Total time= ",(end-start), " seconds")