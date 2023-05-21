import time
import sys
import math
"""
Functions used to run othello
"""

def possible_moves(board, token):
    """
     Returns a list of all possible squares that can be played into by token
    """
    other = "x"
    if token == "x":
        other = "o"
    mod_board = add_border(board,8)
    # print_board(mod_board,10)
    valid_squares = []
    for square in range(len(mod_board)):
        if mod_board[square] == ".":
            directions = [-11,-10,-9,-1,1,9,10,11]
            
            for d in directions:
                space = square + d
                while 0 <= space < len(mod_board):
                    if mod_board[space] == other:
                        space += d
                    else:
                        break
                if mod_board[space] == token and space!=square+d:
                    row = square//10
                    col = square%10

                    board_row = (row-1)
                    board_col = col - 1
                    board_space = board_row*8+board_col
                    valid_squares.append(board_space)
                    break
    return valid_squares
                

def make_move(board,token,index):
    other = "x"
    if token == "x":
        other = "o"
    bordered = list(add_border(board,8))
    bordered_index = (index//8+1)*10 + (index%8+1)
    bordered[bordered_index] = token
    direction = [-11,-10,-9,-1,1,9,10,11]
    for d in direction:
        space = bordered_index + d
        changed = 0
        while 0 <=space < len(bordered):
            if bordered[space] == other:
                bordered[space] = token
                changed += 1
                space += d
            else:
                break
        if bordered[space] != token:
            for i in range(changed):
                space -= d
                bordered[space] = other
    stripped = strip_border("".join(bordered))
    return stripped

def add_border(board,size):
    """
    adds question mark border
    size is the size of the board
    """
    final = "??????????"
    for i in range(0,size):
        final += ("?"+board[i*size:(i+1)*size]+"?")
    final += "??????????"

    return final
def strip_border(board):
    toRet = ""
    for ch in board:
        if ch!="?":
            toRet += ch
    return toRet

def print_board(board,size):
    for i in range(size):
        for j in range(size):
            print(board[i*size+j],end= "")
        print()
#print(possible_moves("xxoo.xox.....oox......oxo..ooxooo..oox.ox.xxx..oxoox...o.....xox","x"))
# print(s:=add_border("...........................ox......xo...........................",8))
# print(len(s))
"""
def negamax(board,player,depth,maxdepth):
    if depth > maxdepth or both None:
        return score of game
    nextMoves = possible_moves(board,token)
    
    scores = []
    for move in next moves:
        scores.append(-1*negamax(move,other,player,depth+1,maxdepth))
    # if nextMoves = []:
    #     return None
    return max(scores)

def score(board,player,depth,maxdepth,myMoves,otherMoves):
     x = board.count("x")
     o = board.count("o")
     if len(myMoves) > 0 and len(otherMoves) > 0:
         count corners taken by black, corners taken by white
         count corner adjacent squares(subtract from score)
         x + o + 4* (black-white corners) - 4 * (corners taken by other) - 2* count taken by me

       
"""

def find_next_move(board, player, depth): # whatever player passed is max_step, that is, trying to to maximize score of this player

    # Based on whether player is x or o, start an appropriate version of minimax
    # that is depth-limited to "depth".  Return the best available move.
    # sets the values of player and other
    other = "o"
    if player == "o":
        other = "x"
    # sets the maxScore
    maxScore = -1*float('inf')
    # finds the next moves for the given player
    nextMoves = possible_moves(board,player)
    # doesn't output anything if moves == None
    if len(nextMoves) == 0:
        return None
    # sets an initial value for bestmove
    bestMove = nextMoves[0]
    # sets alpha and beta to negative and positive infinity, respectively
    alpha = -math.inf
    beta = math.inf
    # for each move
    for move in nextMoves:
        # get new board
        new_board = make_move(board,player,move)
        # calls minstep with alpha and beta
        score = min_step(new_board,other,0,depth,alpha,beta)
        # if score is larger than alpha(the minimum node the maximizer node can return)
        if score > alpha:
            alpha = score
        # update maxscore if applicable
        if score > maxScore:
            maxScore = score
            bestMove = move
    return bestMove


# define max step an minstep in generalized terms to avoid redundant code
# All your other functions
def max_step(board,player,depth,maxdepth,alpha,beta): 
    """Alpha and beta implement A/B pruning
        - alpha: the minimum value that max_step can return
        - beta: maximum value min_step can return
        - if alpha >= beta, then no point in looioking into future anymore
    """
    if alpha >= beta:
        return scoreGame(board,player)
    other = "o"
    if player == "o":
        other = "x"
    if depth > maxdepth: # terminates call and returns score if depth is reached
        return scoreGame(board,player)
    # gets the next moves
    nextMoves = possible_moves(board,player)
    if len(nextMoves) == 0:
        return scoreGame(board,player)
    scores = []
    # appends calls fro minsteps, updates alpha and beta accordingly
    for move in nextMoves:
        new_board = make_move(board,player,move)
        otherturn = min_step(new_board,other,depth+1,maxdepth,alpha,beta)
        if otherturn > alpha:
            alpha = otherturn
        scores.append(otherturn)
    return max(scores)


# trying to minimize scpre, which is returned from the perspective of player
def min_step(board,other,depth,maxdepth,alpha,beta):
    """
    Implements alpha beta pruning on line 190
    """
    player = "x"
    if other == "x":
        player = "o"
    if alpha >= beta: #Alpha beta pruning here
        return scoreGame(board,player)
    if depth > maxdepth: # terminates call and returns score if depth is reached
        return scoreGame(board,player)
    nextMoves = possible_moves(board,other)
    if len(nextMoves) == 0:
        return scoreGame(board,player)
    scores = []
    # returns the minimum scores
    for move in nextMoves:
        new_board = make_move(board,other,move)
        otherturn = max_step(new_board,player,depth+1,maxdepth,alpha,beta)
        # updates beta, the largest value minimum score minimizer node will return
        if otherturn < beta:
            beta = otherturn
        scores.append(otherturn)
    return min(scores)


"""Scoring function here"""
def scoreGame(board,player):
    """
    uses everything as a fraction of 100, 0 is a draw game
    """
    other = "o"
    if player == "o":
        other = "x"
    ptokens = possible_moves(board,player)
    otokens = possible_moves(board,other)
    # print("player has these spaces ",len(ptokens)," opponent has",len(otokens))
    score = 0
    pcount = board.count(player)
    ocount = board.count(other)
    # print("player token count", pcount)
    # print("other count",ocount)
    if len(ptokens) == 0 and len(otokens)==0: # if the game is over

        return 10000*(pcount-ocount) # ensures victory is large number
    # difference in the avalible moves
    mobility = (len(ptokens) - len(otokens))/(len(ptokens)+len(otokens))*100*(1-(pcount+ocount)/64) # mobility
    score += mobility
    # print("mobility",mobility)
    tokensscore = (pcount-ocount)/(pcount+ocount)*200*(pcount+ocount)/64
    score += tokensscore
    corners_dict = {
    0: {1, 8, 9},
    7: {6, 14, 15},
    56: {57, 48, 49},
    63: {62, 54, 55}
    }
    # adds additional points if corners are occupied, deducts points if surrounding corners are occupied
    pcorners = 0
    ocorners = 0
    pcorneradj = 0
    ocorneradj = 0
    
    for c in corners_dict:
        if board[c] == player:
            pcorners += 1
        elif board[c] == other:
            ocorners += 1
        for sq in corners_dict[c]:
            if board[sq] == player:
                pcorneradj += 1
            elif board[sq] == other:
                ocorneradj += 1
    # print("pcorners,ocorners,pcorneradj,ocorneradj",pcorners,ocorners,pcorneradj,ocorneradj)
    if pcorners + ocorners!=0:
        conrerscore = 50*(pcorners-ocorners)/(pcorners+ocorners)
        # print("Coners",conrerscore)
        score += conrerscore
    if pcorneradj + ocorneradj !=0:
        corneradjscore = 50*(pcorneradj-ocorneradj)/(pcorneradj+ocorneradj)
        # print("coner adjacent",corneradjscore)
        score -= corneradjscore
    return score


# print(scoreGame("oxxxxx.xoooooxx.xooo.xoo.xooxoox.oxxooxx.xoxxoxxxxxxxxooo.oxxooo","o"))
# # print(find_next_move("...........................ox......xo...........................","x",3))
board = sys.argv[1]
player = sys.argv[2]
# # # # # board = "...........................ox......xo..........................."
# # # # # player = "o"
depth = 1

for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
# # # start = time.perf_counter()
# # # while time.perf_counter() - start < 1.5:
    print(find_next_move(board, player, depth))
    depth += 1
# print(find_next_move("...........................ox......xxx..........................","o",4))

# results = []
# with open("boards_timing.txt") as f:
#     for line in f:
#         board, token = line.strip().split()
#         temp_list = [board, token]
#         print(temp_list)
#         for count in range(1, 7):
#             print("depth", count)
#             start = time.perf_counter()
#             find_next_move(board, token, count)
#             end = time.perf_counter()
#             temp_list.append(str(end -start))
#         print(temp_list)
#         print()
#         results.append(temp_list)
#         with open("boards_timing_my_results.csv", "w") as g:
#             for l in results:
#                 g.write(", ".join(l) + "\n")


# test_board = "...xx......xxoo...xo.x....xooox...xoooox.xxoxooxxxxoooooo.o....."
# test_board = test_board.replace("x","i")
# test_board = test_board.replace("o","x")
# test_board = test_board.replace("i","o")


# print_board(test_board,8)
# print(possible_moves(test_board,"x"))
# print(possible_moves(test_board,"o"))
# print(scoreGame(test_board,"x"))