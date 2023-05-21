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
    other = "o"
    if player == "o":
        other = "x"
    maxScore = -1*float('inf')
    nextMoves = possible_moves(board,player)
    if len(nextMoves) == 0:
        return None
    bestMove = nextMoves[0]
    alpha = -math.inf
    beta = math.inf
    for move in nextMoves:
        new_board = make_move(board,player,move)
        score = min_step(new_board,other,0,depth,alpha,beta)
        if score is not None and score > alpha:
            alpha = score
        if score is not None and score > maxScore:
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
        return
    other = "o"
    if player == "o":
        other = "x"
    if depth > maxdepth: # terminates call and returns score if depth is reached
        return scoreGame(board,player)
    nextMoves = possible_moves(board,player)
    if len(nextMoves) == 0:
        return scoreGame(board,player)
    scores = []
    for move in nextMoves:
        new_board = make_move(board,player,move)
        otherturn = min_step(new_board,other,depth+1,maxdepth,alpha,beta)
        if otherturn is not None:
            if otherturn > alpha:
                alpha = otherturn
            scores.append(otherturn)
    return max(scores)


# trying to minimize scpre
def min_step(board,other,depth,maxdepth,alpha,beta):
    if alpha >= beta:
        return
    player = "x"
    if other == "x":
        player = "o"
    if depth > maxdepth: # terminates call and returns score if depth is reached
        return scoreGame(board,player)
    nextMoves = possible_moves(board,other)
    if len(nextMoves) == 0:
        return scoreGame(board,other)
    scores = []
    for move in nextMoves:
        new_board = make_move(board,other,move)
        otherturn = max_step(new_board,player,depth+1,maxdepth,alpha,beta)
        if otherturn is not None:
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
    score = 0
    pcount = board.count(player)
    ocount = board.count(other)
    if len(ptokens) == 0 and len(otokens)==0: # if the game is over

        return 10000*(pcount-ocount) # ensures victory is large number
    # difference in the avalible moves
    score += (len(ptokens) - len(otokens))/(len(ptokens)+len(otokens))*100 # mobility
    score += (pcount-ocount)/(pcount + ocount) * 100
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
            elif board[c] == other:
                ocorneradj += 1
    if pcorners + ocorners!=0:
        score += 100*(pcorners-ocorners)/(pcorners + ocorners)
    if pcorneradj + ocorneradj !=0:
        score -= 50*(pcorneradj-ocorneradj)/(pcorneradj+ocorneradj)
    return score

class Strategy():

    logging = True  # Optional

    def best_strategy(self, board, player, best_move, still_running):

        depth = 1

        for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all

            best_move.value = find_next_move(board, player, depth)

            depth += 1