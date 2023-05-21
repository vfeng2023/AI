# state is an array populated with N -1
def backtrack(state,N):
    if test_solution(state):
        return state
    var = get_next(state,N)
    for val in sorted_val(state,N):
        state[var] = val
        result = backtrack(state,N)
        if result is not None:
            return result
        else:
            state[var] = -1


def get_next(state,N):
    # if len(state) < N:
    #     return len(state)
    # return None
    i = 0
    while i < N and state[i] != -1:
        i+= 1
    return i
def sorted_val(state,N):
    avalible = []
    for i in range(N):
        if i not in state:
            avalible.append(i)

    return avalible


# def goal_test(state, N):
#     if len(state) > N:
#         return False
    
#     for r in range(len(state)):
#         val = state[r]
#         left = val-1
#         right = val + 1
#         for i in range(r+1,len(state)):
#             if val == state[i]:
#                 return False
#             if left >=0 and state[i] == left:
#                 return False

#             if right < N and state[i] == right:
#                 return False

#             left -= 1
#             right += 1

#     return True

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            if compare == -1:
                return False
            left -= 1
            right += 1
            if state[compare] == middle:
                return False
            if left >= 0 and state[compare] == left:
                return False
            if right < len(state) and state[compare] == right:
                return False
    return True

N = 5
initial = [-1 for i in range(N)]

print(backtrack(initial,N))
