"""
Piece orientations:
See tetris_orientations.py
"""
import sys
import random
import time
import pickle
POPULATION_SIZE = 30
TOURNAMENT_SIZE = 10
NUM_CLONES = 1
NUM_TRIALS = 5
MUTATION_RATE = 0.2
# the board is modeled by a list of 20 strings, each one 10 long. A string is a row, an entry in the array in the column
# zero is the bottommost piece
TETRIS_PIECES = {
    "I":{
        0:["####"],
        1:["#","#","#","#"]
    },
    "O":{
        0:["##","##"]
    },
    "T":{
        0:["###"," # "],
        1:["# ","##","# "],
        2:[" # ","###"],
        3:[" #","##"," #"],

    },
    "S":{
        0:["## "," ##"],
        1:[" #","##","# "]
    },
    "Z":{
        0:[" ##","## "],
        1:["# ","##"," #"],
    },
    "J":{
        0:["###","#  "],
        1:["# ","# ","##"],
        2:["  #","###"],
        3:["##"," #"," #"],
    },
    "L":{
        0:["###","  #"],
        1:["##","# ","# "],
        2:["#  ","###"],
        3:[" #"," #","##"]
    }
}
PIECE_CHOICES = list(TETRIS_PIECES.keys())
# convert the piece + orientation into a character
# go through the reversed string and try placement in chucks of 10
# if can successfully place:
# return board with that configuration
# else:
    # return None
def place_piece(board,piece,orientation,location):
    """
    board is in REVERSE order
    """
    curr_piece = TETRIS_PIECES[piece][orientation]
    # location is 0 indexed
    piece_mask = ""
    size = len(curr_piece[0])
    for row in curr_piece:
        piece_mask += (" "*(location)) + row + (" "* (10-size-(location)))
    if len(piece_mask) > len(curr_piece) * 10:
        return None,None
    # attempt placement, top bottom, stoping at the last valid position
    last_valid_move,lastCleared = "GAME OVER", 0
    for i in range(len(board),0,-10): # go through each row 
        if i - len(piece_mask) >= 0:
            board_seg = board[i-len(piece_mask):i]
            result = mask(piece_mask,board_seg)
            if result is not None:
                newboard = board[:i-len(result)] + result + board[i:]
                boardAsList = [newboard[i:i+10] for i in range(0,len(newboard),10)]
                boardAsList,cleared = clearRows(boardAsList)
                newboard = "".join(boardAsList)
                last_valid_move,lastCleared = newboard,cleared
                # print_board(newboard)
            else:
                break

    return last_valid_move,lastCleared
def clearRows(board):
    """
    Returns board, rowsCleared
    """
    i = 0
    rowsCleared = 0
    while i < len(board):
        if board[i] == "##########":
            del board[i]
            board.append(" "*10)
            rowsCleared += 1
        else:
            i += 1
    return board,rowsCleared
def mask(piece,board_segment):
    """
    Does a piece mask returning the combined piece and boared segment
    """
    if len(board_segment) != len(piece):
        return None
    combined = ""
    for i in range(len(piece)):
        if piece[i] == "#" and board_segment[i] == "#":
            return None
        elif piece[i] == " " and board_segment[i] == " ":
            combined += " "
        else:
            combined += "#"
    return combined

def play_game(strategy):
    # board = make_new_board()
    board = " "*200 # in reverse order
    # points = 0
    points = 0
    # while game is not over:
    while board != "GAME OVER":
        # piece = randomly chosen pece
        piece = random.choice(PIECE_CHOICES)
        # print(piece)
        bestBoard = None
        bestheur = -float('inf')
        # for each orientation:
        for orient in TETRIS_PIECES[piece]:
            # for each column:
            for col in range(0,10):
                # poss_board = place(piece,orientation,location,board)
                poss_board,cleared = place_piece(board,piece,orient,col)
                # print()
                # print_board(poss_board)
                # input()
                if poss_board is not None :
                # poss_score = heuristic(poss_board,strategy)
                    poss_score = heurestic(poss_board,strategy,cleared)
                    if poss_score > bestheur:
                        bestBoard = poss_board,cleared
                        bestheur = poss_score
        # board = (board with highest heuristic)
        board,rowsCleared = bestBoard
        #print_board(board)
        # print_board(bestBoard)
        # if lines were cleared:
        if rowsCleared == 1:
            points += 40
        elif rowsCleared == 2:
            points += 100
        elif rowsCleared == 3:
            points += 300
        elif rowsCleared == 4:
            points += 1200
            # points += new_points
        # print_board(board)
        # print("Points earned: ",points)
        # input()
    # return points
    return points

# testris values: highest board height, deepest well depth=min, number of holes, last number of rows cleared,
# range betwwen maximum and minimum heights, average column height, 

def highest_heap(board):
    """
    boardItself should be a string
    boardAsList is the list of strings bottom to top, left to right
    returns the highest heap and column where it is
    returns average height, max height, min_height, and range, and number of holes
    """
    boardAsList = [board[i:i+10] for i in range(0,len(board),10)]
    max_height = 0
    min_height = 100
    avg_height = 0
    holes = 0
    for col in range(0,10):
        # get a list with the column itself, then find index of latest # 
        board_column = [boardAsList[i][col] for i in range(20)]
        height = rindex(board_column)
        holes += count_values(board_column," ",0,height)
        max_height = max(max_height,height)
        min_height = min(min_height,height)
        avg_height += height
    avg_height = avg_height/10
    height_diff = max_height - min_height
    return avg_height,max_height,min_height,height_diff,holes

def count_values(iterable,value,start,end):
    count = 0
    for i in range(start,end):
        if iterable[i] == value:
            count += 1
    return count
def count_holes(board):
    """
    counts the number of holes on the board
    """
    count = 0
    for i in range(len(board)):
        if board[i] == " ":
            while i < len(board):
                if board[i] == "#":
                    count += 1
                    break
                i+= 10

    return count
def print_board(board):
    if board == "GAME OVER":
        print(board)
        return
    board_as_list = [board[i:i+10] for i in range(0,len(board),10)]
    board_as_list.reverse()
    test = "".join(board_as_list)
    print("=======================")
    for count in range(20):
        print(' '.join(list(("|" + test[count * 10: (count + 1) * 10] + "|"))), " ", count)
    print("=======================")
    print()
    print("  0 1 2 3 4 5 6 7 8 9  ")
    print()
def rindex(array):
    for i in range(len(array)-1,-1,-1):
        if array[i] == "#":
            return i+1
    return 0
def heurestic(board,strategy,rowsCleared):
    """
    Board shall be stored in reverse row major order
    """
    if board == "GAME OVER":
        return -40000000
    value = 0
    a,b,c,d,e,f = strategy
    avg_val,max_val,wells,diff,numHoles = highest_heap(board)
    # print(" avg_val,max_val,wells,diff",avg_val,max_val,wells,diff)
    # print("numHoles: ",numHoles)
    value += a * avg_val
    value += b * max_val
    value += c * wells
    value += d * diff
    value += e * rowsCleared
    value += f * numHoles
    return value


"""
OWO testing
board = " "*200
board,_=place_piece(board,"J",1,0)
print_board(board)
# input()
board,_ = place_piece(board,"O",0,1)
# input()
board,_ = place_piece(board,"I",1,9)
# board_ = place_piece(board,"I")
print_board(board)
print(heurestic(board,strat,0))

board_seg = "##"+" "*8 + " "*10
piece = " ##        ##       "
print(mask(piece,board_seg))
"""


# Genetic algorithm functions
def generatePop():
    population = set()
    while len(population) < POPULATION_SIZE:
        # generate new strategy
        strat = list()
        for i in range(6):
            strat.append(-1+random.random()*2)
        population.add(tuple(strat))
    return list(population)

# fitness function - average of 5 games
def fitness_function(strategy):
    game_scores = []
    for count in range(5):
        game_scores.append(play_game(strategy))
    return sum(game_scores) / len(game_scores)
# breeds two parents
def breed(strat1,strat2):
    child = [None for i in range(len(strat1))]
    numcross = random.randint(1,len(strat1) - 1)
    indices = random.sample(range(len(strat1)),numcross)
    for i in indices:
        child[i] = strat1[i]
    
    for j in range(len(strat2)):
        if child[j] is None:
            child[j] = strat2[j]
        if random.random() < MUTATION_RATE:
            modindex = random.randint(0,len(child)-1)
            child[modindex] = -1 + random.random() * 2
    return tuple(child)
        

def next_generation(population:list,stratScore):
    new_gen = set()
    population.sort(key=lambda a:stratScore[a],reverse=True)
    for count in range(NUM_CLONES):
        new_gen.add(population[count])

    while len(new_gen) < POPULATION_SIZE:
        # select parents
        tournament_groups = random.sample(population,k=2*TOURNAMENT_SIZE)
        tour1 = tournament_groups[:TOURNAMENT_SIZE]
        tour2 = tournament_groups[TOURNAMENT_SIZE:]
        tour1.sort(key=lambda a:stratScore[a],reverse=True)
        tour2.sort(key=lambda a:stratScore[a],reverse=True)
        parent1 = tour1[0]
        parent2 = tour2[0]
        child = breed(parent1,parent2)
        if child not in new_gen:
            new_gen.add(child)
    return list(new_gen), population[0]
def scoreGeneration(population):
    count = 0
    stratScore = dict()
    popTotalPoints = 0
    for strat in population:
        print("Evaluating strategy ",count," ->",end = " ")
        fitness_score = fitness_function(strat)
        print(fitness_score)
        stratScore[strat] = fitness_score
        popTotalPoints += fitness_score
        count += 1
    average = popTotalPoints / len(population)
    # print("Current generation average score: ",average)
    return stratScore
# genCount = 0
# population = generatePop()
# while genCount < 4:
#     print("generation: ",genCount)
#     population = next_generation(population)
#     genCount += 1

# strategy = list()
# for k in range(6):
#     strategy.append(-1+random.random()*2)
# print(strategy)
# strategy = tuple(strategy)
# start = time.perf_counter()
# avg = fitness_function(strategy)
# end = time.perf_counter()
# print("score=",avg)
# print(end-start, "seconds")
def play_game_nicely(strate):
    # board = make_new_board()
    board = " "*200 # in reverse order
    # points = 0
    points = 0
    # while game is not over:
    while board != "GAME OVER":
        # piece = randomly chosen pece
        piece = random.choice(PIECE_CHOICES)
        bestBoard = None
        bestheur = -float('inf')
        # for each orientation:
        for orient in TETRIS_PIECES[piece]:
            # for each column:
            for col in range(0,10):
                # poss_board = place(piece,orientation,location,board)
                poss_board,cleared = place_piece(board,piece,orient,col)
                # print()
                # print_board(poss_board)
                # input()
                if poss_board is not None :
                # poss_score = heuristic(poss_board,strategy)
                    poss_score = heurestic(poss_board,strate,cleared)
                    if poss_score > bestheur:
                        bestBoard = poss_board,cleared
                        bestheur = poss_score
        # board = (board with highest heuristic)
        board,rowsCleared = bestBoard
        #print_board(board)
        # print_board(bestBoard)
        # if lines were cleared:
        if rowsCleared == 1:
            points += 40
        elif rowsCleared == 2:
            points += 100
        elif rowsCleared == 3:
            points += 300
        elif rowsCleared == 4:
            points += 1200
            # points += new_points
        print_board(board)
        print("Points earned: ",points)
    # return points
    return points
# initialOption = input("Would you like to begin a (N)ew process or (S)aved process? ")
# if initialOption == "N":
#     curr_population = generatePop()
#     stratToScore = scoreGeneration(curr_population)
# else:
#     filename = input("File name: ")
#     stratToScore:dict = pickle.load(open(filename,"rb"))
#     curr_population = stratToScore.keys()

    
# while True:
#     userop = input("Would you like to (W)atch best strategy, (S)ave current generation, or (C)ontinue to evolve? ")

    
#     if userop == "W":
#         print("best strategy: ",bestStrat)
#         play_game_nicely(bestStrat)
#     elif userop == "S":
#         fileToSave = input("Filename to save as: ")
#         pickle.dump(stratToScore,open(fileToSave,"rb"))
#         exit()
#     else:
#         curr_population,bestStrat = next_generation(curr_population,stratToScore)
#         stratToScore = scoreGeneration(curr_population)
strat = (0.75,-0.3,0.05,0.6,0.9,0.7)
value = fitness_function(strat)
print(value)