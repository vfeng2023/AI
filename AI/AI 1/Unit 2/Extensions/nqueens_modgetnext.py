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
    return res

"""
Functions necessary for incremental repair
"""
def backtrack_gen(state,N,curr,used_col:set,taken_cols):
    if None not in state:
        return state
    # var is the row

    for row in range(N):
        vals = sorted_val_gen(state,N,used_col,taken_cols,row)
        if len(vals) > 0:
            state[row] = random.choice(vals)
        else:
            state[row] = random.randint(0,N-1)
            
        used_col.add(state[row])
        eliminate_diag_gen(row,state[row],taken_cols,N)
    return state

# this function modifies the sets within a list containing the taken diagonal rows
def eliminate_diag_gen(row,curr_val,taken,N):
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

def reset_diag_gen(row,curr_val,taken,N):
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

def sorted_val_gen(state,N,nums,taken,row):
    avalible = []
    for i in range(N):
        if i not in nums and (taken[row][i] <= 0):
            avalible.append(i)
    return avalible


def count_conflict(state,N,row,col=state[row]):
    count = 0
    # conflict if column is same or row2 - row1 == col2 - col1 <-- indicates diagonal
    for compare in range(len(state)):
        if state[compare]!=None:
            if compare!=row:
                if state[compare] == col or abs(compare-row) == abs(state[compare]-col):
                    count += 1

    return count

def total_conflict(state,N):
    count = 0
    for i in range(N):
        count += count_conflict(state,N,i)
    return count//2
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


def inc_repair(state,N,conflict):
    if conflict == 0:
        return state
    # find row with most conflicts
    while conflict > 0:
        max_rows = []
        biggest = 0
        for i in range(N):
            count = count_conflict(state,N,i)
            if count == biggest:
                max_rows.append(i)
            elif count > biggest:
                biggest = count
                max_rows= [i]
        fix = random.choice(max_rows)

        # determine col in that row with the least
        original = state[fix]
        least = N+100
        min_cols = []
        for i in range(N):
            state[fix] = i
            conf = count_conflict(state,N,fix)
            if conf < least:
                least = conf
                min_cols = [i]
            elif conf == least:
                min_cols.append(i)

        
        # replace that row with that
        state[fix] = random.choice(min_cols)
        # call in repair again until conflict reaches 0
        total=total_conflict(state,N)
        conflict = total
    return state

def call_repair(N):   
    initial = [None for i in range(N)]
    taken = [Counter() for _ in range(N)]
    res=backtrack_gen(initial,N,0,set(),taken)
    total = total_conflict(res,N)
    inc_repair(res,N,total)
    return res


start = time.perf_counter()
solved = []
N = 8
while time.perf_counter()-start < 30:
    solved.append(call_backtrack(N))
    N += 1
# call_backtrack(112)
# stops being fast at 111 going forward
# for i in range(200,8,-1):
#     call_backtrack(i)
# end = time.perf_counter()
# # stops at 181 going in reverse
# print("Total time= ",(end-start), " seconds")

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