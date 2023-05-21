import random
# state is an array populated with N -1
def backtrack(state,N,curr,used_rows:set) -> list:
    if goal_test(state,N):
        return state
    var = curr+1
    for val in sorted_val(state,N,used_rows):
        state[var] = val
        used_rows.add(val)
        result = backtrack(state,N,var,used_rows)
        if result is not None:
            return result
        else:
            state[var] = None
            used_rows.remove(val)


def sorted_val(state,N,nums):
    print(type(nums))
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

for N in range(8,30):
    initial = [None for i in range(N)]

    print(res:=backtrack(initial,N,-1,set()))
# print(test_solution(res))
