"""
RANDOM - picks a random valid move
AGRESSIVE - for ultimate tic tac toe, always picks the move which wins on the local board.
Board - a list of 9 XOOXXXOOO strings representing the smaller boards(numbers)
Next_move(board,last_played) -- returns a list of possible next moves
score_board(board,player) -- returns the score of a board. Heurestic
def min_step, max_step: Depth limited to value, should implement alpha beta pruning
printBoard() - prints everything nicely
- https://stackoverflow.com/questions/25027122/break-the-function-after-certain-time
"""
import random
def gameOver(board,player):
    """
    Returns 1,0,-1 or None
    1 - I win
    0 - Draw
    -1 - Other wins
    None = incomplete board
    """
    # check diagonals, rows and columns. Returns a (bool,int) tuple. bool indicates if game is over, int describes score of board
    other = "O"
    if player == "O":
        other = "X"
    win = player*3
    loss = other*3
    
    
    for row in range(3):
        if (seq:=board[(row*3):(row+1)*3]) == win:
            return 1
        if seq == loss:
            return -1
    for col in range(3):
        seq = board[col:col+3*3:3]
        if seq == win:
            return 1
        if seq == loss:
            return -1
    # check diagonals
    posDiag = board[0]+board[4]+board[8]
    negDiag = board[2]+board[4]+board[6]

    if posDiag == win:
        return 1
    if posDiag == loss:
        return -1
    if negDiag == win:
        return 1
    if negDiag == loss:
        return -1
    if board.find(".") == -1:
        return 0
    # if no board is present, return false
    return None

def next_move(board,player,last_played):
    if last_played == -1: # if board is starting
        return list(range(81))
    # from last_played, determine the location on the subboard
    next_loc = last_played%9
    # get game corresponding to lastplayed location
    status = gameOver(board[next_loc],player)
    if status is None:
        poss_moves = []
        for i in range(9):
            if board[next_loc][i] == ".":
                poss_moves.append(next_loc*9+i)
        return poss_moves
    # if the game at that location is complete, return all unplayed indices on the board
    else:
        poss_moves = []
        for sub in range(len(board)):
            for i in range(len(board[sub])):
                if board[sub][i] == ".":
                    poss_moves.append(9*sub+i)
        return poss_moves

def printBoard(board):
    toRet = ""
    for row in range(3):
        index1 = ""
        for col in range(0,3):
            for i in range(0,3):
                toRet += board[row*3+col][i]
                index1 += str(9*(row*3+col)+i) + " "
            if col < 2:
               toRet += "|"
               index1 += "|"
        toRet+= "\t\t\t"+index1 + '\n'
        index2 = ""
        for col in range(0,3):
            for i in range(3,6):
                toRet += board[row*3+col][i]
                index2 += str(9*(row*3+col)+i) + " "
            if col < 2:
                toRet += "|"
                index2 += "|"
        toRet+="\t\t\t"+index2+'\n'
        index3 = ""
        for col in range(0,3):
            for i in range(6,9):
                toRet += board[row*3+col][i]
                index3 += str(9*(row*3+col)+i)+ " "
            if col < 2:
                toRet += "|"
                index3 += "|"
            
        toRet+="\t\t\t"+index3+'\n'
        toRet += "---+---+---\t\t\t----------------------------\n"

    print(toRet)
        
        
def make_move(board,location,token):
    subboard = location//9
    subindex = location%9
    old = board[subboard]
    new = old[:subindex]+token + old[subindex+1:]
    board[subboard] = new
    return board
test_board = ["........." for i in range(9)]

def getbigBoard(board,player):
    other = "O"
    if player == "O":
        other = "X"
    big_board = "" # <-- status of the large board . = incomplete, ? = draw, X = X won, O = O won
    for b in board:
        status = gameOver(b,player)
        if status is None:
            big_board += "."
        else:
            if status == 1:
                big_board += player
            elif status == 0:
                big_board += "?"
            else:
                big_board += other
    return big_board

def scoreBoard(board,player):
    """
    1 - player win
    0 - Draw
    -1 - player lost
    # higher score indicates better outcome for passed player
    """
    other = "O"
    if player == "O":
        other = "X"
    big_board = getbigBoard(board,player)
    endGame = gameOver(big_board,player)
    if endGame is not None:
        if endGame > 0:
            return 100000
        elif endGame == 0:
            return 100*(big_board.count(player)-big_board.count(other))
        else:
            return -100000
    else:
        # advantage for: having a two in a row on a big board, getting the center, getting corner squares
        
        # small board weighting: the completeness of the board(number open/9 * score of small board)

        # total score: large board score+score of each small board
        big_Score = score_subboard(big_board,player)*10
        smallScore = 0
        weights = [10,1,10,
                    1,20,1,
                    10,1,10] # corners have weight of 10, points, center is 20, edges are 1
        for b in range(len(board)):
            smallScore += score_subboard(board[b],player) * weights[b]
        return big_Score + (smallScore)*0.2
        
def score_subboard(board,player):
    VICTORY = 500
    CORNER = 25
    CENTER = 30
    TWO = 20
    other = "O"
    if player == "O":
        other = "X"
    end = gameOver(board,player)
    if end is not None:
        return end * VICTORY
    else:
        score = 0
        myTwo = 0
        otherTwo = 0
        for i in range(3):
            if (seq:=board[i:i+3]) == player+player+"." or seq == "."+player+player:
                myTwo += 1
            if seq == other+other+"." or seq == "."+other+other:
                otherTwo += 1
        # columns
        for col in range(3):
            seq = board[col:col+3*3:3]
            if seq == player+player+"." or seq == "."+player+player:
                myTwo += 1
            if seq == other+other+"." or seq == "."+other+other:
                otherTwo += 1
        # diagonals
        posDiag = board[0]+board[4]+board[8]
        negDiag = board[2]+board[4]+board[6]
        if posDiag == player+player + "." or posDiag == "."+player+player:
            myTwo += 1
        if posDiag == other+other+"." or posDiag == "."+other+other:
                otherTwo += 1

        if negDiag == player+player + "." or negDiag == "."+player+player:
            myTwo += 1
        if negDiag == other+other+"." or negDiag == "."+other+other:
                otherTwo += 1
        score += TWO*(myTwo-otherTwo)
        # look for corners
        myCorners = 0
        otherCorners = 0
        for c in [0,2,6,8]:
            if board[c] == player:
                myCorners += 1
            elif board[c] == other:
                otherCorners+= 1
        if myCorners == 3:
            myCorners *= 2
        if otherCorners == 3:
            otherCorners *= 2
        score += CORNER*(myCorners - otherCorners)
        # add weighting for centers
        if board[len(board)//2] == player:
            score += CENTER
        elif board[len(board)//2] == other:
            score -= CENTER
        return score

# test_board = ["XOX.......","OOOOOOOOO","OOOOOOOOO",".........",".........",".........",".........",".........","........."]            
# printBoard(test_board)     
# print(scoreBoard(test_board,"O")) 

def max_step(board,player,depth,alpha,beta,max_depth,last_played):

    """
    
    """
    other = "X"
    if player == "X":
        other = "O"
    if alpha >= beta:
        return scoreBoard(board,player)
    if depth > max_depth:
        return scoreBoard(board,player)
    result = []
    nextPossMoves = next_move(board,player,last_played)
    for move in nextPossMoves:
        nb = board.copy()
        make_move(nb,move,player)
        # printBoard(nb)
        next_poss = min_step(nb,other,depth+1,alpha,beta,max_depth,move)
        if next_poss > alpha:
            alpha = next_poss
        result.append(next_poss)
    return max(result)

def min_step(board,other,depth,alpha,beta,max_depth,last_played):
    """
    Attempts to minimize score. No shift in perspective
    """
    player = "X"
    if  other == "X":
        player = "O"
    if alpha >= beta:
        return scoreBoard(board,player)
    if depth > max_depth:
        return scoreBoard(board,player)
    result = []
    nextPossMoves = next_move(board,other,last_played)
    for move in nextPossMoves:
        nb = board.copy()
        make_move(nb,move,other)
        # printBoard(nb)
        next_poss = max_step(nb,player,depth+1,alpha,beta,max_depth,move)
        if next_poss < beta:
            beta = next_poss
        result.append(next_poss)
    # print(result)
    return min(result)
    
def bestPlayer(board,last_played,player,max_depth):
    other = "O"
    if player == "O":
        other = "X"
    alpha = -float("inf")
    beta = float("inf")
    nextPossMoves = next_move(board,player,last_played)
    bestPos = nextPossMoves[0]
    max_score = -float('inf')
    # scores = []
    for move in nextPossMoves:
        nb = board.copy()
        make_move(nb,move,player)
        result = min_step(nb,other,1,alpha,beta,max_depth,move)
        # scores.append(result)
        if result > alpha:
            alpha = result
        if result > max_score:
            max_score = result
            bestPos = move
    # print("BEst",scores)
    return bestPos

def rand(board,nextPossPositions):
    return random.choice(nextPossPositions)

def aggressive(board,nextPossPositions,player):
    # evaluates all the next possible positions and returns the one with the higher score
    best = nextPossPositions[0]
    maxScore = 0
    # scores = []
    for move in nextPossPositions:
        nb = board.copy()
        nb = make_move(nb,move,player)
        score = scoreBoard(board,player)
        # scores.append(score)
        if maxScore < score:
            maxScore = score
            best = move
    # print("AGRESSIVE",scores)
    return best
def displayOverall(board,player):
    big = getbigBoard(board,player)
    toRet = ""
    for i in range(3):
        for j in range(3):
            toRet += big[i*3+j]
            toRet += "|"
        toRet += "\n"
        toRet += "-+-+-\n"
    print(toRet)
# board = [".X......." for i in range(9)]
# next = next_move(board,0,-1)
# print(next)
# print(aggressive(board,next,"X"))
# board = ['XX.OOO...', 'OOX..OO.O', 'XXOO....O', 'XX.......', 'XX......O', 'XX.......', 'X........', '..O......', 'XXX.O....']
# printBoard(board)
# displayOverall(board,"O")
# print(scoreBoard(board,"X"))
# print(next_move(board,"X",4))
# best = bestPlayer(board,4,"X",2)
# test the minimax algorithm implementation again user

# test_board = ['XOOOOOOXX', 'XXOOOXOOX', 'XXOXOXXXX', 'XXOXOXO..', 'XXX.O....', 'XXO..O..O', 'XXO.O.O..', 'XX..O..OO', 'XXO.O.O..']
# next = [32, 33, 34, 35, 39, 41, 42, 43, 44, 48, 49, 51, 52, 57, 59, 61, 62, 65, 66, 68, 69, 75, 77, 79, 80]

# aggressive(test_board,next,"X")
# bestPlayer(test_board,0,"O",1)