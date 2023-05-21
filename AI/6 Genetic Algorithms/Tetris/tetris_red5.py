"""
Piece orientations:
See tetris_orientations.py
"""
import sys
import random
import time
import pickle
POPULATION_SIZE = 500
TOURNAMENT_SIZE = 10
NUM_CLONES = 50
NUM_TRIALS = 5
MUTATION_RATE = 0.2
WIN_RATE = 0.75
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
# offset from baseline
TETRIS_OFFSET = {
    "I":{
        0:(0,0,0,0),
        1:(0,),
    },
    "O":{
        0:(0,0),
    },
    "T":{
        0:(0,0,0),
        1:(0,-1),
        2:(-1,0,-1),
        3:(-1,0),
    },
    "S":{
        0:(0,0,-1),
        1:(-1,0),
    },
    "Z":{
        0:(-1,0,0),
        1:(0,-1)
    },
    "J":{
        0:(0,0,0),
        1:(0,-2),
        2:(-1,-1,0),
        3:(0,0)
    },
    "L":{
        0:(0,0,0),
        1:(0,0),
        2:(0,-1,-1),
        3:(-2,0)
    }
}
# tetris heights from baseline
TETRIS_HEIGHTS = {
    "I":{
        0:(1,1,1,1),
        1:(4,),
    },
    "O":{
        0:(2,2),
    },
    "T":{
        0:(1,2,1),
        1:(3,2),
        2:(2,2,2),
        3:(2,3),
    },
    "S":{
        0:(1,2,2),
        1:(3,2),
    },
    "Z":{
        0:(2,2,1),
        1:(2,3)
    },
    "J":{
        0:(2,1,1),
        1:(3,3),
        2:(2,2,2),
        3:(1,3)
    },
    "L":{
        0:(1,1,2),
        1:(3,1),
        2:(2,2,2),
        3:(3,3)
    }
}
PIECE_CHOICES = list(TETRIS_PIECES.keys())
# convert the piece + orientation into a character
# go through the reversed string and try placement in chucks of 10
# if can successfully place:
# return board with that configuration
# else:
    # return None
def place_piece(board,piece,orientation,location,column_heights):
    """
    board is in REVERSE order
    """
    curr_piece = TETRIS_PIECES[piece][orientation]
    # print(piece,orientation)
    # print("location: ",location)
    offset = TETRIS_OFFSET[piece][orientation]
    lastCol = location + len(curr_piece[0]) - 1 # last column
    if lastCol >= len(column_heights):
        return None,0
    # compute the relevant offset, then find the max of the offset
    poss_rows = []
    for col in range(location,lastCol+1):
        height = column_heights[col]
        poss_rows.append(height + offset[col-location])
    base_row = max(poss_rows)
    if base_row < 0 or base_row >= 20:
        return None,0
    fromBase = TETRIS_HEIGHTS[piece][orientation]
    for column in range(location,lastCol+1):
        index = column - location
        column_heights[column] = base_row + fromBase[index]
        if column_heights[column] > 20:
            return "GAME OVER",0
    # do a mask starting from that row with padding and mask    
    board_seg = board[base_row*10:base_row*10+len(curr_piece)*10]
    # location is 0 indexed
    piece_mask = ""
    size = len(curr_piece[0])
    for row in curr_piece:
        piece_mask += (" "*(location)) + row + (" "* (10-size-(location)))
    # the new height would be baseline height + index of the last vertical # in the piece
    new_segment = mask(piece_mask,board_seg)
    new_board = board[0:base_row*10] + new_segment + board[base_row*10 + len(new_segment):]
    # clear rows
    baslist = [new_board[i:i+10] for i in range(0,len(new_board),10)]
    result = clearRows(baslist)
    # print(result)
    # input()
    baslist,rowsCleared = result
    # clears the rows on the column_heights
    for col in range(len(column_heights)):
        column_heights[col] -= rowsCleared
    new_board = "".join(baslist)
    # return new board,number of cleared

    return new_board,rowsCleared

def get_height(piece,column):
    for i in range(len(piece)-1,-1,-1):
        if piece[i][column] == "#":
            return i
    return -1
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

def print_board(board):
    if board is None:
        print("none")
        return
    if board == "GAME OVER":
        print(board)
        return
    board_as_list = [board[i:i+10] for i in range(0,len(board),10)]
    board_as_list.reverse()
    test = "".join(board_as_list)
    print("=======================")
    for count in range(20):
        print(' '.join(list(("|" + test[count * 10: (count + 1) * 10] + "|"))), " ", 20-count-1)
    print("=======================")
    print()
    print("  0 1 2 3 4 5 6 7 8 9  ")
    print()
def clearRows(board):
    count = 0
    i = 0
    while i < len(board):
        if board[i] == "##########":
            del board[i]
            board.append(" "*10)
            count += 1
        else:
            i += 1
    return board,count
def rindex(array,column,currPos):
    finalindex = 0
    for i in range((currPos-1) * 10 + column,0,-10):
        if array[i] == "#":
            return i+1
    return 0

def play_game(strategy,nicely=False):
    # board = make_new_board()
    board = " "*200 # in reverse order
    # points = 0
    points = 0
    column_heights = [0 for i in range(10)]
    # while game is not over:
    while board != "GAME OVER":
        # piece = randomly chosen pece
        piece = random.choice(PIECE_CHOICES)
        # print(piece)
        bestBoard = None
        bestheur = -float('inf')
        best_col = column_heights
        # for each orientation:
        for orient in TETRIS_PIECES[piece]:
            # for each column:
            for col in range(0,10):
                new_col_heights = column_heights.copy()
                # poss_board = place(piece,orientation,location,board)
                poss_board,cleared = place_piece(board,piece,orient,col,new_col_heights)
                # print()
                # print_board(poss_board)
                # input()
                # print_board(poss_board)
                if poss_board is not None :
                # poss_score = heuristic(poss_board,strategy)
                    poss_score = heurestic(poss_board,strategy,cleared,new_col_heights)
                    if poss_score > bestheur:
                        bestBoard = poss_board,cleared
                        bestheur = poss_score
                        best_col = new_col_heights
        # board = (board with highest heuristic)
        if bestBoard is None:
            return points
        board,rowsCleared = bestBoard
        column_heights = best_col
        
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
        if nicely:
            print_board(board)
            print("Points: ",points)
            # points += new_points
        # print_board(board)
        # print("Points earned: ",points)
        # print(heurestic(board,strategy,rowsCleared,column_heights))
        # input()
    # return points
    return points

# testris values: highest board height, deepest well depth=min, number of holes, last number of rows cleared,
# range betwwen maximum and minimum heights, average column height, 

def highest_heap(board,board_columns):
    """
    boardItself should be a string
    boardAsList is the list of strings bottom to top, left to right
    returns the highest heap and column where it is
    returns average height, max height, min_height, and range, and number of holes
    diff updated to roughness measure of abs diff between columsn
    """
    boardAsList = [board[i:i+10] for i in range(0,len(board),10)]
    max_height = 0
    min_height = 100
    avg_height = 0
    holes = 0
    for col in range(0,10):
        # get a list with the column itself, then find index of latest # 
        
        height = board_columns[col]
        if height == 0:
            pass
        else:
            for k in range(col,height*10+col,10):
                if board[k] == " ":
                    holes += 1
        max_height = max(max_height,height)
        min_height = min(min_height,height)
        avg_height += height
    avg_height = avg_height/10
    height_diff = 0
    for col_index in range(1,len(board_columns)):
        height_diff += abs(board_columns[col_index] - board_columns[col_index-1])
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
    if board is None:
        print("none, not a valid move!")
        return
    if board == "GAME OVER":
        print(board)
        return
    board_as_list = [board[i:i+10] for i in range(0,len(board),10)]
    board_as_list.reverse()
    test = "".join(board_as_list)
    print("=======================")
    for count in range(20):
        print(' '.join(list(("|" + test[count * 10: (count + 1) * 10] + "|"))), " ", 20-count-1)
    print("=======================")
    print()
    print("  0 1 2 3 4 5 6 7 8 9  ")
    print()
def rindex(array):
    for i in range(len(array)-1,-1,-1):
        if array[i] == "#":
            return i+1
    return 0
def heurestic(board,strategy,rowsCleared,columns):
    """
    Board shall be stored in reverse row major order
    """
    if board == "GAME OVER":
        return -40000000
    value = 0
    a,b,c,d,e,f = strategy
    avg_val,max_val,wells,diff,numHoles = highest_heap(board,columns)
    # print("avg_val,max_val,wells,diff,numHoles",avg_val,max_val,wells,diff,numHoles)
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
    numcross = random.randint(1,len(strat1) - 1) # number of values to copy from parent 1
    indices = random.sample(range(len(strat1)),numcross) # indices to copy
    for i in indices:
        child[i] = strat1[i]
    
    for j in range(len(strat2)):
        if child[j] is None:
            child[j] = strat2[j]

    # mutation rate should only occur once
    if random.random() < MUTATION_RATE:
        modindex = random.randint(0,len(child)-1)
        child[modindex] = -1 + random.random() * 2
    return tuple(child)
        

def next_generation(population:list,stratScore):
    new_gen = set()
    population.sort(key=lambda a:stratScore[a],reverse=True)
    # # the values are being correctly chosen
    # index = 0
    # for p in population:
    #     print("strategy in population",p)
    #     print("score: ",stratScore[p])
    #     index += 1
    #     if index == NUM_CLONES:
    #         break
    
    # for count in range(NUM_CLONES):
    #     new_gen.add(population[count])
    #     print("ITEM: ",population[count])
    #     print("Score: ",stratScore[population[count]])
    # input()
    while len(new_gen) < POPULATION_SIZE:
        # select parents
        tournament_groups = random.sample(population,k=2*TOURNAMENT_SIZE)
        tour1 = tournament_groups[:TOURNAMENT_SIZE]
        tour2 = tournament_groups[TOURNAMENT_SIZE:]

        tour1.sort(key=lambda a:stratScore[a],reverse=True)
        tour2.sort(key=lambda a:stratScore[a],reverse=True)
        # best one is frist in the list
        # print("TOURNAMENT 1 group")
        # for i in range(len(tour1)):
        #     print("strategy",tour1[i])
        #     print("Score: ",stratScore[tour1[i]])
        # print("TOURNAMENT 2 group")
        # for i in range(len(tour2)):
        #     print("strategy",tour2[i])
        #     print("Score: ",stratScore[tour2[i]])
        # input()
        p1index = 0
        while p1index < len(tour1):
            if random.random() < WIN_RATE:
                parent1 = tour1[p1index]
                break
            else:
                p1index += 1
        if p1index == len(tour1):
            parent1 = tour1[-1]
        # print("Parent1: ",parent1)
        p2index = 0
        while p2index < len(tour2):
            if random.random() < WIN_RATE:
                parent2 = tour2[p2index]
                break
            else:
                p2index += 1
        if p2index == len(tour2):
            parent2 = tour2[-1]
       #print("parent2:",parent2)
        child = breed(parent1,parent2)
        # input()
        # print("Child",child)
        # print("parent1", parent1)
        # print("parent2: ",parent2)
        # input()
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
    print("Current generation average score: ",average)
    return stratScore


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

# parent1 = tuple([-1 + random.random() * 2 for k in range(6)])
# parent2 = tuple([-1 + random.random() * 2 for k in range(6)])
# child = breed(parent1,parent2)
# print("CHild: ",child)
# print("parent1: ",parent1)
# print("parent2: ",parent2)

initialOption = input("Would you like to begin a (N)ew process or (S)aved process? ")
if initialOption == "N":
    curr_population = generatePop()
    stratToScore = scoreGeneration(curr_population)
    bestStrat = curr_population[0]
    average = 0.0
    for strat in stratToScore:
        average += stratToScore[strat]
        if stratToScore[strat] > stratToScore[bestStrat]:
            bestStrat = strat
    average/= len(stratToScore)
    print("Best strategy: ",bestStrat)
    print("Score of best strategy: ",stratToScore[bestStrat])
    print("Average score of this generation: ",average)

else:
    filename = input("File name: ")
    stratToScore:dict = pickle.load(open(filename,"rb"))
    curr_population = list(stratToScore.keys())
    bestStrat = curr_population[0]
    average = 0.0
    for strat in stratToScore:
        average += stratToScore[strat]
        if stratToScore[strat] > stratToScore[bestStrat]:
            bestStrat = strat
    average/= len(stratToScore)
    print("Best strategy: ",bestStrat)
    print("Score of best strategy: ",stratToScore[bestStrat])
    print("Average score of this generation: ",average)
# with open("run7.txt","w") as f:
#     while True:
#         userop = input("Would you like to (W)atch best strategy, (S)ave current generation, or (C)ontinue to evolve? ")

        
#         if userop == "W":
#             print("best strategy: ",bestStrat)
#             play_game(bestStrat,nicely=True)
#         elif userop == "S":
#             # save is functional
#             fileToSave = input("Filename to save as: ")
#             pickle.dump(stratToScore,open(fileToSave,"wb"))
#             break
#         else:
#             curr_population,bestStrat = next_generation(curr_population,stratToScore)
#             stratToScore = scoreGeneration(curr_population)
#             bestStrat = curr_population[0]
#             average = 0.0
#             for strat in stratToScore:
#                 average += stratToScore[strat]
#                 if stratToScore[strat] > stratToScore[bestStrat]:
#                     bestStrat = strat
#             average/= len(stratToScore)
#             print("Best strategy: ",bestStrat)
#             print("Score of best strategy: ",stratToScore[bestStrat])
#             print("Average score of this generation: ",average)

#             f.write("Best strategy: "+str(bestStrat)+"\n")
#             f.write("Score of best strategy: " + str(stratToScore[bestStrat]) + "\n")
#             f.write("Average score of this generation: " + str(average) + "\n")

#             f.write("\n")


# print to file
genCount = 0
with open(input("Save run stats to file: "),"w") as f:
    while genCount < 10:
        curr_population,bestStrat = next_generation(curr_population,stratToScore)
        stratToScore = scoreGeneration(curr_population)
        bestStrat = curr_population[0]
        average = 0.0
        for strat in stratToScore:
            average += stratToScore[strat]
            if stratToScore[strat] > stratToScore[bestStrat]:
                bestStrat = strat
        average/= len(stratToScore)
        f.write("Generation " + str(genCount))
        print("Best strategy: ",bestStrat)
        print("Score of best strategy: ",stratToScore[bestStrat])
        print("Average score of this generation: ",average)
        f.write("Best strategy: "+str(bestStrat)+"\n")
        f.write("Score of best strategy: " + str(stratToScore[bestStrat]) + "\n")
        f.write("Average score of this generation: " + str(average) + "\n")

        f.write("\n")


        genCount += 1
# strat = (0.75,-0.3,0.05,0.6,0.9,0.7)
# value = fitness_function(strat)
# print(value)
# play_game(strat)

# genCount = 0
# population = generatePop()
# while genCount < 4:
#     print("generation: ",genCount)
#     stratScore = scoreGeneration(population)
#     next_one,bestOfCurrent = next_generation(population,stratScore)
#     print("Best strategy of current generation: ",bestOfCurrent)
# strat = list()
# for i in range(6):
#     strat.append(-1+random.random()*2)
# strat2 = list()
# for i in range(6):
#     strat2.append(-1+random.random()*2)

# print(breed(strat,strat2))