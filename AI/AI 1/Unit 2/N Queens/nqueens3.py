import random
from collections import Counter
# state is an array populated with N -1
# nested list set structure containing the conflicting diagonals(need to reset if does not work out)
#taken cols -- diagonals for each row that cannot be used
# used_col -- vertical columns which cannot be used


def backtrack(state,N,curr,used_col:set,taken_cols,unfilled):
    # print(state)
    # print(taken)
    # print()
    if goal_test(state,N) and len(unfilled) == 0:
        return state
    # var is the row
    var = get_next(state,N,unfilled)
    for val in sorted_val(state,N,used_col,taken_cols,var):
        state[var] = val
        used_col.add(val)
        eliminate_diag(var,val,taken_cols,N)
        # print(taken_cols)
        # input()
        result = backtrack(state,N,var,used_col,taken_cols,unfilled)
        if result is not None:
            return result
        else:
            state[var] = None
            used_col.remove(val)
            reset_diag(var,val,taken_cols,N)
            unfilled.add(var)
    return None


# this function modifies the sets within a list containing the taken diagonal rows
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

def reset_diag(row,curr_val,taken,N):
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
        taken[r][col] -= 1
        r -= 1
        col -= 1

    # take right up diagonals
    r = row - 1
    col = curr_val+1
    while r >= 0 and col < N:
        taken[r][col] -= 1
        r -= 1
        col += 1

    # take left down diagonals
    r = row + 1
    col = curr_val-1
    while r < N and col >= 0:
        taken[r][col]-=1
        r += 1
        col -= 1

def sorted_val(state,N,nums,taken,row):
    avalible = []
    for i in range(N):
        if i not in nums and (taken[row][i] <= 0):
            avalible.append(i)
    return avalible

def get_next(state, N,unfilled):
    return unfilled.pop()
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
                return False
            if left >= 0 and state[compare] == left:
                return False
            if right < len(state) and state[compare] == right:
                return False
    return True


N = 4
initial = [None for i in range(N)]


taken = [Counter() for _ in range(N)]
unfilled = {i for i in range(N)}
# print(taken)
print(N, res:=backtrack(initial,N,-1,set(),taken,unfilled))

# eliminate_diag(0,0,taken,N)
# reset_diag(0,0,taken,N)

# print(taken)
# print(test_solution(res))
