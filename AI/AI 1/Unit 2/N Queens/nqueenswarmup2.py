# state is an array populated with N -1
def backtrack(state,N):
    if goal_test(state,N) and (None not in state):
        return state
    var = get_next(state,N)
    print(var)
    for val in sorted_val(state,N):
        new_state = state.copy()
        new_state[var] = val
        result = backtrack(new_state,N)
        if result is not None:
            return result

    


def get_next(state,N):
    # if len(state) < N:
    #     return len(state)
    # return None
    try:
        return state.index(None)
    except ValueError:
        return -1
def sorted_val(state,N):
    avalible = []
    for i in range(N):
        if i not in state:
            avalible.append(i)

    return avalible


def goal_test(state, N):
    if len(state) > N:
        return False
    
    for r in range(len(state)):
        val = state[r]
        if val is None:
            continue
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

N = 9
initial = [None for i in range(N)]

print(res:=backtrack(initial,N))
# print(test_solution(res))
