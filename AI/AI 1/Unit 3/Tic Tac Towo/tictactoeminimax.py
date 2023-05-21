import sys
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
the minimax algorithms assume that both players(max_step and min_step) will make the optimal decision, with the score quantifying the benefit of the descision. 
Depending on which player the computer is, the function will make the most beneficial descision for itself. 
X, which is max, always "wants" to get the higher score And thus chooses the highest scoring opportunity after min has played
O, or min, always wants the get the lower score and thus chooses the lowest scoring opportunity after max has played

the function that is called differs
    - def gameOver(board) -> 1 if X winds, 0 if draw, -1 if O wins,
    - def nextMoves(board,player) -> list of boards which represent next possible moves
"""

def gameOver(board):
    """
    Returns a tuple of (boolean,int)
    boolean -- indicates if the game is over
    int -- indicates the score of the game
    """
    # check diagonals, rows and columns. Returns a (bool,int) tuple. bool indicates if game is over, int describes score of board
    
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
    if board.find(".") == -1:
        return True,0
    # if no board is present, return false
    return False,69


def print_board(board):
    for i in range(3):
        row = "{0}\t\t\t\t{1}"

        chars0 = ""
        chars1 = ""
        for j in range(3):
            chars0+=board[i*3+j]
            chars1 += str(i*3+j)
        print(row.format(chars0,chars1))
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

    

def play_turn(board,player):
    """
    Returns the index of the space which the token representing the computer should play at.
    If the game is over, returns -1
    """
    isover,score = gameOver(board)
    if isover:
        return -1

    if player == "X":
        maxScore = -100
        move = -1
        boardlist = list(board)
        for i in range(len(board)):
            if board[i] == ".": # check if location is valid
                boardlist[i] = player # play there
                new_board = "".join(boardlist) # create the new string
                myScore = min_step(new_board) # call min_step
                # print("i:",i,"myscore=",myScore)
                if myScore > 0: # print the score
                    print("Going at ",i," results in a win")
                elif myScore < 0:
                    print("Going at ",i," results in a loss")
                else:
                    print("Going at ",i," results in a tie")
                if myScore > maxScore: # set maxscore and best move if good to update
                    move = i
                    maxScore = myScore
                boardlist[i] = "." # resets space for next move
        print("I choose ",move)
        return move
    else:

        minScore = 100
        move = -1
        boardlist = list(board)
        for i in range(len(board)):
            if board[i] == ".":
                boardlist[i] = player
                new_board = "".join(boardlist)
                myScore = max_step(new_board)
                if myScore < 0:
                    print("Going at ",i," results in a win")
                elif myScore > 0:
                    print("Going at ",i," results in a loss")
                else:
                    print("Going at ",i," results in a tie")
                if myScore < minScore:
                    move = i
                    minScore = myScore
                boardlist[i] = "."
        print("I choose ",move)
        return move

# max step represents X
def max_step(board):
    """
    max_step represents "X"
    """
    isover,score = gameOver(board)
    if isover:
        return score
    possMoves = nextMove(board,"X")
    results = []
    for next_move in possMoves:
        results.append(min_step(next_move))
    return max(results)

def min_step(board):
    """
    min_step() is "O", always trying to minimize score. Calls max_step
    """
    isover,score = gameOver(board)
    if isover:
        return score
    possMoves = nextMove(board,"O")
    results = []
    for move in possMoves:
        results.append(max_step(move))
    return min(results)


"""Acepts user input starting here"""
def check(board):
    end,score = gameOver("".join(board))
    if end:
        if score > 0:
            print("X wins")
        elif score < 0:
            print("O wins")
        else:
            print("Tie")
        return True
    return False
startboard = sys.argv[1]#"........." 
# startboard = "OXX.O.XOX"
# print(min_step(startboard))
# print(max_step(startboard))
# print(gameOver("OXXOOXXOX"))

if startboard == "".join(["." for i in range(9)]):
    player = input("Should I play X or O? ")
    other = "O"
    turn = 0
    # if turn is even, then computer is going. If turn is odd, then user is going
    if player == "O":
        other = "X"
        turn = 1
   
    
    while True:
        print_board(startboard)
        if turn%2 == 0:
            loc = play_turn(startboard,player)
            board = list(startboard)
            board[loc] = player
            startboard = "".join(board)

        else:
            user = int(input("Your choice? "))
            board = list(startboard)
            board[user] = other
            startboard = "".join(board)
        turn +=1
        if check(board):
            print_board(board)
            break

else:
    if check(list(startboard)):
        print("Board is complete")
        exit()
    countX = 0
    countO = 0
    for ch in startboard:
        if ch == "X":
            countX += 1
        elif ch == "O":
            countO += 1
    player = "O"
    user = "X"
    turn = 0
    if countX == countO:
        player = "X"
        user = "O"
    while True:
        print_board(startboard)
        if turn%2 == 0:
            loc = play_turn(startboard,player)
            board = list(startboard)
            board[loc] = player
            startboard = "".join(board)

        else:
            user_choice = int(input("Your choice? "))
            board[user_choice] = user
            startboard = "".join(board)
        turn +=1
        if check(board):
            print_board(board)
            break

        

        
