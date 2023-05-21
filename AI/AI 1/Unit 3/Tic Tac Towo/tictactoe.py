from collections import deque
"""
Tic tac toe
board is represented as string of nine characters.
X = X
O = O
. = empty space:
......... = empty grid

1. Model a 3x3 Tic-Tac-Toe board as a 9 character string where "." means empty and the players are "X" and "O".
Please use capital letters to match my grading script. By convention, we will say "X" always moves first. For any
board, determine if the game is over, and if so whether X wins, O wins, or there is a tie. (Note that the board
does not have to be full for the game to be over.) If the game is not over, determine the set of all possible
moves remaining
    - def gameOver(board) -> 1 if X winds, 0 if draw, -1 if O wins,
    - def nextMoves(board,player) -> list of boards which represent next possible moves
2.
X wins in some moves {5: 120, 7: 444}
Y wins in some moves {6: 148, 8: 168}
draw 78
Puzzles:  958
total games:  255168
"""

def gameOver(board):
    """
    Returns a tuple of (boolean,int)
        boolean -- indicates if the game is over
        int -- indicates the score of the game
    """
    # check diagonals, rows and columns. Returns a (bool,int) tuple. bool indicates if game is over, int describes score of board
    if board.find(".") == -1:
        return True,0
    for row in range(3):
        if (seq:=board[(row*3):(row+1)*3]) == "XXX":
            return True,1
        if seq == "OOO":
            return True,-1
    for col in range(3):
        seq = board[col:col+3*3:3]
        if seq == "XXX":
            return True,1
        if seq == "OOO":
            return True,-1
    # check diagonals
    posDiag = board[0]+board[4]+board[8]
    negDiag = board[2]+board[4]+board[6]

    if posDiag == "XXX":
        return True,1
    if posDiag == "OOO":
        return True,-1
    if negDiag == "XXX":
        return True,1
    if negDiag == "OOO":
        return True,-1
    # if no board is present, return false
    return False,69


def print_board(board):
    for i in range(3):
        for j in range(3):
            print(board[i*3+j],end=" ")
        print()
def nextMove(board,player):
    """
    board - the 9 character string representation of the board
    player - the character "X" or "O" that is going
    """
    possMoves = []
    spaces = list(board)
    for i in range(len(spaces)):
        if spaces[i] == ".":
            spaces[i] = player
            possMoves.append("".join(spaces))
            spaces[i] = "."
    return possMoves

def countMoves():
    """
    generate the final board states
    to find total number of games:
        sum of the # of X! * # of O! for each board
    """
    totalSequences = 0
    # perform a BFS search to find total number of final boards
    # start player can be determined on the basis of whether spaces remaining are odd or even:
        # empty = odd: X player
        # empty = even: Y plays
    start = "........."
    visited = dict()
    fringe = deque()
    endstates = set()

    movestowinX = dict()
    movestowinO = dict()
    numDraw = 0
    visited[start] = 1
    # information on fringe: the total number
    fringe.append(start)
    while len(fringe) > 0:
        board = fringe.popleft()
        # print("board=",board,"player =",player)
        endGame, score = gameOver(board)

        if endGame:
            endstates.add(board)
            moves = len(board) - board.count(".")
            if score > 0:
                if moves not in movestowinX:
                    movestowinX[moves] = 0
                movestowinX[moves] += 1
            elif score < 0:
                if moves not in movestowinO:
                    movestowinO[moves] = 0
                movestowinO[moves] += 1
            else:
                numDraw += 1
            continue
        spacesleft = board.count(".")
        if spacesleft%2 == 1:
            children = nextMove(board,"X")
        else:
            children = nextMove(board,"O")
        for child in children:
            if child not in visited:
                visited[child] = visited[board]
                fringe.append(child)
            else:
                visited[child] += visited[board]
    print("Total games: ",totalSequences)
    print("End states: ",len(endstates))
    print("X wins in some moves",movestowinX)
    print("Y wins in some moves",movestowinO)
    print("draw",numDraw)
    # print(endstates)

    for e in endstates:
        totalSequences += visited[e]
    print("Puzzles: ",len(endstates))
    print("total games: ",totalSequences)
    # print(endstates)
    return endstates

countMoves()
# def factorial(n):
#     prod = 1
#     for i in range(1,n+1):
#         prod *= i
#     return prod

# ends = countMoves()

# # determine the numbe of total games, and games which can be found where X wins in # moves
# totalGames = 0
# movesToWin = dict()
# for board in ends:
#     xcount = 0
#     Ocount = 0
#     emptycount = 0
#     for ch in board:
#         if ch == "O":
#             Ocount += 1
#         elif ch == "X":
#             xcount += 1
#         else:
#             emptycount += 1
#         totalGames += (factorial(xcount)*factorial(Ocount))
#     if xcount not in movesToWin:
#         movesToWin[xcount] = 1
#     else:
#         movesToWin[xcount]+= 1
# print("Total games",totalGames)
# print("Moves to win: ",movesToWin)


# lines for testing the validity of the function
# board = "XOXXOXOXO"
# print_board(board)
# print(gameOver(board))