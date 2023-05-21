from othello_imports import possible_moves, make_move
import time
import sys
import math
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
        return;
    player = "x"
    if other == "x":
        player = "o"
    if depth > maxdepth: # terminates call and returns score if depth is reached
        return scoreGame(board,player)
    nextMoves = possible_moves(board,other)
    if len(nextMoves) == 0:
        return scoreGame(board,other) # multiply by negative 1 since the scores called with min_step are opposite those called by max_step
    scores = []
    for move in nextMoves:
        new_board = make_move(board,other,move)
        otherturn = max_step(new_board,player,depth+1,maxdepth,alpha,beta)
        if otherturn is not None:
            if otherturn < beta:
                beta = otherturn
            scores.append(otherturn)
    return min(scores)

# """Scoring function here"""
# def scoreGame(board,player):
#     """
#     scoring strategy needs to:
#         - account for mobility early game
#         - account for pieces taken
#         - give captured corners more weight
#         - give corner adjacent less weight
#         score = (my avalible spaces - other avalible spaces) * 
#         (1-occupied spaces/size of board(64)) * 4 + 
#         count x - count o + 
#         (mycorners-other corners)*4+1*(- my_corner_adjacent + other_corner_adjacent) 
#         defined in so higher score is intended to mean higher probability of winning for given player
#     """
#     other = "o"
#     if player == "o":
#         other = "x"
#     ptokens = possible_moves(board,player) # spaces player can move to
#     otokens = possible_moves(board,other) # spaces opponent can move to
#     pcount = board.count(player) # number of tokens on the board
#     ocount = board.count(other)
#     if len(ptokens) == 0 and len(otokens)==0: # if the game is over
#         return 1000000+(pcount-ocount)
#     else:
#         return pcount-ocount
#     # difference in the avalible moves
#     # score = (len(ptokens) - len(otokens))*4*(1-(pcount+ocount)/64) # newly captured pieces
#     # corners_dict = {
#     # 0: {1, 8, 9},
#     # 7: {6, 14, 15},
#     # 56: {57, 48, 49},
#     # 63: {62, 54, 55}
#     # }
#     # # adds additional points if corners are occupied, deducts points if occupied
#     # for c in corners_dict:
#     #     if board[c] == player:
#     #         score += 4
#     #     elif board[c] == other:
#     #         score -= 4
#     #     for sq in corners_dict[c]:
#     #         if board[sq] == player and board[c]==other:
#     #             score -= 2
#     #         elif board[c] == other and board[c]==player:
#     #             score += 2
#     # return score

def scoreGame(board,player):
    other = "o"
    if player == "o":
        other = "x"
    ptokens = possible_moves(board,player)
    otokens = possible_moves(board,other)
    if len(ptokens) == 0 and len(otokens)==0: # if the game is over
        pcount = board.count(player)
        ocount = board.count(other)
        return 1000000+(pcount-ocount)
    # difference in the avalible moves
    score = (len(ptokens) - len(otokens))*4 # newly captured pieces
    corners_dict = {
    0: {1, 8, 9},
    7: {6, 14, 15},
    56: {57, 48, 49},
    63: {62, 54, 55}
    }
    # adds additional points if corners are occupied, deducts points if 
    for c in corners_dict:
        if board[c] == player:
            score += 4
        elif board[c] == other:
            score -= 4
        for sq in corners_dict[c]:
            if board[sq] == player:
                score -= 2
            elif board[c] == other:
                score += 2
    return score




# All your other functions



class Strategy():

    logging = True  # Optional

    def best_strategy(self, board, player, best_move, still_running):

        depth = 1

        for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all

            best_move.value = find_next_move(board, player, depth)

            depth += 1
# print(scoreGame("oxxxxx.xoooooxx.xooo.xoo.xooxoox.oxxooxx.xoxxoxxxxxxxxooo.oxxooo","o"))
# print(find_next_move("...........................ox......xo...........................","x",3))
# board = sys.argv[1]
# player = sys.argv[2]
# # # # board = "...........................ox......xo..........................."
# # # # player = "o"
# depth = 1

# for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
# start = time.perf_counter()
# while time.perf_counter() - start < 1.5:
    # print(find_next_move(board, player, depth))
    # depth += 1
# while True:
   # print(19)
# print(19)
# print(scoreGame())
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