import random
from collections import Counter
import time
# state is an array populated with N -1
# nested list set structure containing the conflicting diagonals(need to reset if does not work out)
#taken cols -- diagonals for each row that cannot be used
# used_col -- vertical columns which cannot be used


def backtrack(state,N,curr,used_col:set,taken_cols):
    if None not in state:
        return state
    # var is the row

    for row in range(N):
        vals = sorted_val(state,N,used_col,taken_cols,row)
        if len(vals) > 0:
            state[row] = random.choice(vals)
        else:
            state[row] = random.randint(0,N-1)
            
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

def sorted_val(state,N,nums,taken,row):
    avalible = []
    for i in range(N):
        if i not in nums and (taken[row][i] <= 0):
            avalible.append(i)
    return avalible

def count_conflict(state,N,row):
    col = state[row]
    count = 0
    # conflict if column is same or row2 - row1 == col2 - col1 <-- indicates diagonal
    for compare in range(len(state)):
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
        print("Board ",state, " conflict ", total:=total_conflict(state,N))
        conflict = total
    return state

def call_repair(N):   
    initial = [None for i in range(N)]
    taken = [Counter() for _ in range(N)]

    res=backtrack(initial,N,0,set(),taken)
    total = total_conflict(res,N)
    print("Initial state: ",res,"Conflict ",total)
    inc_repair(res,N,total)
    
    print("Verification: ",test_solution(res))
start = time.perf_counter()
# call_repair(200)
call_repair(36)
end = time.perf_counter()

print("total time: ",(end-start)," seconds")