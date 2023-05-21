import random
# state is an array populated with N -1
def backtrack(state,N,used_vals:set,used_spaces) -> list:
    if goal_test(state,N):
        return state
    var = next_space(state,used_spaces,N)
    used_spaces.add(var)
    for val in sorted_val(state,N,used_vals):
        state[var] = val
        used_vals.add(val)
        result = backtrack(state,N,used_vals,used_spaces.copy())
        if result is not None:
            return result
        else:
            state[var] = None
            used_vals.remove(val)


#generate next value using random
def next_space(state,used,N):
    r = random.randint(0,N-1)
    while r in used:
        r = random.randint(0,N-1)
    return r

def sorted_val(state,N,nums):
    avalible = []
    for i in range(N):
        if i not in nums:
            avalible.append(i)
    return avalible


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
print(backtrack(initial,N,set(),set()))