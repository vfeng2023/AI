import time
import sys
"""
You have a square grid; each square may contain a digit from 1 to the size of the grid. The grid is divided into blocks of varying shape and size, with arithmetic clues written in them. 
Your aim is to fully populate the grid with digits such that:

Each row contains only one occurrence of each digit
Each column contains only one occurrence of each digit
The digits in each block can be combined to form the number stated in the clue, using the arithmetic operation given in the clue. That is:
An addition clue means that the sum of the digits in the block must be the given number. For example, ‘15+’ means the contents of the block adds up to fifteen.
A multiplication clue (e.g. ‘60×’), similarly, means that the product of the digits in the block must be the given number.
A subtraction clue will always be written in a block of size two, and it means that one of the digits in the block is greater than the other by the given amount. 
For example, ‘2−’ means that one of the digits in the block is 2 more than the other, or equivalently that one digit minus the other one is 2. The two digits could be either way round, though.
A division clue (e.g. ‘3÷’), similarly, is always in a block of size two and means that one digit divided by the other is equal to the given amount.
Note that a block may contain the same digit more than once (provided the identical ones are not in the same row and column). 
This rule is precisely the opposite of the rule in Solo's ‘Killer’ mode (see chapter 11).

- Build constraint sets (block, row, column)
- For block constraints:
    - associate each index with a letter
    - each letter associates with an operation and a sum
        - applyOp(), 
        - 3 data records:
            - index to letter
            - letter to result
            - letter to operation
            - index to letter for blocks which are division or subtraction
        
    - for forward looking
        - cleared_squares = [...]
        while len(cleared_squares) > 0:
            square = cleared_square.pop()
            for row square is in:
                remove square as an option
                if len(board[removed_index]) == 0:
                    return None
            for column square is in:
                remove value at square as option:
                if len(board[removed_index]) == 0:
                    return None
            for block square is in:
                decrease constraint value by doing inverse of block operation on a copy of the constraint_set state tracker
                    --> * is /, - is +, + is -
                    if result is less than the identity value for respective operation or results in fraction answer:
                        ex: 6 + 6-7 = -1 < 0: return None
                            abs(6//7 - 6/7) > 0.0000001 return None # check i fraction
                            subtraction: neither a-result nor a+result result in a valid value
                            division:
                            neither val/result or val * result result in a valid answer
                            addition:
                            result - val results in a negative number
                            multiplication:
                            result /val results in a fraction
                    division and subtraction can determine the value in the square if valid
    - for constraint satisfaction:(probably not neccesary)
        - cleared squares = []
        - for each column 
            build frequency table of symbols occuring in indices
            if table[symbol] == 1 index:
                assign to square
                add to cleared squares
        - repeat for row
        - call forward looking on the cleared_squares
                
- get_next:
    - if board is not populated:
        - return a square from the division or subtraction square
    else:
        - return square with least choices(just do this)
- backtracking:
    if filled return state
    next_space = return index with fewest choices
    for v in possible_values:
        nb = board.copy()
        nb[next_space] = v
        checked =forward_looking(nb)
        if checked is not None:
            constr = contraint_satisfaction(checked)
            result = backtrack(checked)
            if result is not None:
                return result
    return None

"""

def build_row(N):
    """
    builds the row constrainst sets
    """
    rows = {r:set() for r in range(N)}
    for i in range(N*N):
        r = i//N
        rows[r].add(i)
    return rows
def build_col(N):
    """
    builds the column constraint sets
    """
    column_dict = {c:set() for c in range(N)}
    for i in range(N*N):
        c = i%N
        column_dict[c].add(i)
    return column_dict

def build_block(initState,block_ops):
    """
    block ops should be in form of [("A",res,op)]
    builds the index to block mappings and the block to result and operation mappings("A":[op,result,[indices if op is / or -]])
    """

    blockToRes = dict()
    blockToOp = dict()
    # build from block_ops
    for b,res,op in block_ops:
        blockToRes[b] = res
        blockToOp[b] = [op]
        if op == "/" or op == "-":
            blockToOp[b].append([])
    
    # indexToBlock

    indToBlock = dict()
    for i in range(len(initState)):
        indToBlock[i] = initState[i]
        if blockToOp[initState[i]][0] == "/" or blockToOp[initState[i]][0] == "-":
            blockToOp[initState[i]][1].append(i)
    return blockToRes,blockToOp,indToBlock

def backtrack(state,N,blockToRes,blockToOp,indToBlock,rowConstr,colConstr):
    """
    state -- array with strings as choices for the values to be used
    """
    next = get_next(state,N)
    if next == -1:
        return state
    for v in state[next]:
        new_state = state.copy()
        new_state[next] = v
        new_res = blockToRes.copy()
        checked = forward(new_state,N,[next],new_res,blockToOp,indToBlock,rowConstr,colConstr)
        if checked is not None:
            result = backtrack(checked,N,new_res,blockToOp,indToBlock,rowConstr,colConstr)
            if result is not None:
                return result

def get_next(state,N):
    minchoice = N + 100
    index = -1
    for i in range(len(state)):
        if (l:=len(state[i])) > 1 and l < minchoice:
            minchoice = l
            index = i
    return index
def forward(state,N,cleared_squares,blockToRes,blockToOp,indToBlock,rowConstr,colConstr):
    """
    Calls forward looking on a square
    N is the size of one size of the square
    """
#  - cleared_squares = [...]
#         while len(cleared_squares) > 0:
#             square = cleared_square.pop()
#             for row square is in:
#                 remove square as an option
#                 if len(board[removed_index]) == 0:
#                     return None
#             for column square is in:
#                 remove value at square as option:
#                 if len(board[removed_index]) == 0:
#                     return None
#             for block square is in:
#                 decrease constraint value by doing inverse of block operation on a copy of the constraint_set state tracker
#                     --> * is /, - is +, + is -
#                     if result is less than the identity value for respective operation or results in fraction answer:
#                         ex: 6 + 6-7 = -1 < 0: return None
#                             abs(6//7 - 6/7) > 0.0000001 return None # check i fraction
#                             subtraction: neither a-result nor a+result result in a valid value
#                             division:
#                             neither val/result or val * result result in a valid answer
#                             addition:
#                             result - val results in a negative number
#                             multiplication:
#                             result /val results in a fraction
#                     division and subtraction can determine the value in the square if valid
    while len(cleared_squares) > 0:
        # print_puzzle(state,N)
        # print(blockToRes)
        square = cleared_squares.pop()
        row = square//N
        col = square%N
        for constrSet in rowConstr[row],colConstr[col]:
            for neighbor in constrSet:
                if neighbor!=square:
                    oldlen = len(state[neighbor])
                    state[neighbor] = state[neighbor].replace(state[square],"")
                    if len(state[neighbor]) == 0:
                        return None
                    if oldlen > 1 and len(state[neighbor]) == 1:
                        cleared_squares.append(neighbor)
        block = indToBlock[square]
        op = blockToOp[block][0]
        val = int(state[square])

        # elimination based on operation
        if op == "+":
            blockToRes[block] -= val
            if blockToRes[block] < 0:
                return None
        elif op == "x":
            res = blockToRes[block]
            if res//val < 1 or abs(res//val - res/val) > 0.000000001:
                return None
            else:
                blockToRes[block]=blockToRes[block]//val
        elif op == "-":
            poss1 = val + blockToRes[block]
            poss2 = val - blockToRes[block]
            for neigh in blockToOp[block][1]:
                if neigh != square:
                    break
            oldlen = len(state[neigh])
            neighVal = int(state[neigh])
            if len(state[neigh]) == 1 and neighVal-val != blockToRes[block] and val-neighVal !=blockToRes[block]:
                return None
            if poss1 > N and poss2 < 0:
                return None
            else:
                if oldlen > 1:
                    state[neigh] = ""
                    if poss1 <= N:
                        state[neigh] += str(poss1)
                    if poss2 > 0:
                        if poss2!=poss1:
                            state[neigh] += str(poss2)

            if oldlen > 1 and len(state[neigh]) == 1:
                cleared_squares.append(neigh)
        else:
            poss1 = val * blockToRes[block]
            poss2 = val // blockToRes[block]
            for neigh in blockToOp[block][1]:
                if neigh != square:
                    break
            neighVal = int(state[neigh])
            if len(state[neigh]) == 1 and neighVal/val != blockToRes[block] and val//neighVal !=blockToRes[block]:
                return None
            oldlen = len(state[neigh])
            if poss1 > N and (poss2 <= 0 or abs(poss2-val/blockToRes[block]) > 0.000000001):
                return None
            else:
                if oldlen > 1:
                    state[neigh] = ""
                    if poss1 <= N:
                        state[neigh] += str(poss1)

                    if poss2 > 0 and abs(poss2-val/blockToRes[block]) < 0.000000001:
                        if poss2!=poss1:
                            state[neigh] += str(poss2)
                    if oldlen > 1 and len(state[neigh]) == 1:
                        cleared_squares.append(neigh)
    return state
def print_puzzle(state,N):
    for i in range(N):
        for j in range(N):
            print(state[i*N+j],end=" ")
        print()
with open(sys.argv[1]) as f:
    puzzle = [line.strip() for line in f.readlines()]
    # print(puzzle)
    initstate = puzzle[0]
    N = int(len(initstate)**0.5)
    rules = []
    for i in range(1,len(puzzle)):
        stuff = puzzle[i]
        block,res,op = stuff.split()
        res = int(res)
        rules.append((block,res,op))

rowConstr = build_row(N)
colConstr = build_col(N)
blockToRes,blockToOp,indToBlock = build_block(initstate,rules)
# print(rowConstr)
# print(colConstr)
# print(blockToRes)
# print(blockToOp)
# print(indToBlock)
symbols = "123456789"[:N]
board = [symbols for i in range(len(initstate))]
# print(board)
# print_puzzle(board,N)
result = backtrack(board,N,blockToRes,blockToOp,indToBlock,rowConstr,colConstr)
# result = forward(board,N,[0],blockToRes,blockToOp,indToBlock,rowConstr,colConstr)
# print_puzzle(initstate,N)
# print(blockToOp)
# print(blockToRes)
# print_puzzle(result,N)
print("".join(result))


