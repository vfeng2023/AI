"""
Piece orientations:
See tetris_orientations.py
"""
import sys
import random
import time
import pickle
POPULATION_SIZE = 500
TOURNAMENT_SIZE = 20
NUM_CLONES = 75
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
def rindex(array):
    for i in range(len(array)-1,-1,-1):
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
        print("TOURNAMENT 1 group")
        for i in range(len(tour1)):
            print("strategy",tour1[i])
            print("Score: ",stratScore[tour1[i]])
        print("TOURNAMENT 2 group")
        for i in range(len(tour2)):
            print("strategy",tour2[i])
            print("Score: ",stratScore[tour2[i]])
        input()
        p1index = 0
        while p1index < len(tour1):
            if random.random() < WIN_RATE:
                parent1 = tour1[p1index]
                break
            else:
                p1index += 1
        if p1index == len(tour1):
            parent1 = tour1[-1]
        print("Parent1: ",parent1)
        p2index = 0
        while p2index < len(tour2):
            if random.random() < WIN_RATE:
                parent2 = tour2[p2index]
                break
            else:
                p2index += 1
        if p2index == len(tour2):
            parent2 = tour2[-1]
        print("parent2:",parent2)
        child = breed(parent1,parent2)
        input()
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
    
# while True:
#     userop = input("Would you like to (W)atch best strategy, (S)ave current generation, or (C)ontinue to evolve? ")

    
#     if userop == "W":
#         print("best strategy: ",bestStrat)
#         play_game(bestStrat,nicely=True)
#     elif userop == "S":
#         # save is functional
#         fileToSave = input("Filename to save as: ")
#         pickle.dump(stratToScore,open(fileToSave,"wb"))
#         break
#     else:
#         curr_population,bestStrat = next_generation(curr_population,stratToScore)
#         stratToScore = scoreGeneration(curr_population)
#         bestStrat = curr_population[0]
#         average = 0.0
#         for strat in stratToScore:
#             average += stratToScore[strat]
#             if stratToScore[strat] > stratToScore[bestStrat]:
#                 bestStrat = strat
#         average/= len(stratToScore)
#         print("Best strategy: ",bestStrat)
#         print("Score of best strategy: ",stratToScore[bestStrat])
#         print("Average score of this generation: ",average)
# print to file
genCount = 0
with open("run4.txt","w") as f:
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


#         genCount += 1
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
"""
Stats:
Generation 0: 
Best strategy:  (0.87704289685575, -0.7855812781048153, 0.24008747082523918, 0.10649787343130335, 0.42851146021385955, -0.9007009311361194)
Score of best strategy:  2684.0
Average score of this generation:  193.512
Generation 1:
Best strategy:  (-0.44215296136724014, -0.14624128344358378, -0.47817871869106465, -0.3524127755254687, 0.6773575529976787, -0.9567837208555914)
Score of best strategy:  3348.0
Average score of this generation:  795.16

Generation 2:
Best strategy:  (-0.09896453570452945, 0.0452584096610773, -0.2115581036006895, -0.20940083687536548, -0.017614067456895866, -0.8276698995631122)
Score of best strategy:  3484.0
Average score of this generation:  965.608
Generation 3:
Best strategy:  (-0.44215296136724014, 0.34971918717912964, -0.7938481927042802, -0.3524127755254687, 0.40374964221724374, -0.9567837208555914)
Score of best strategy:  4096.0
Average score of this generation:  1000.264

Generation 4:
Best strategy:  (-0.09896453570452945, 0.0452584096610773, -0.2115581036006895, -0.20940083687536548, 0.22300675500426959, -0.8276698995631122)
Score of best strategy:  3824.0
Average score of this generation:  1137.384
# second run
Best strategy:  (-0.4683971422983395, -0.202114654726542, -0.6524527292669662, -0.18907033817438013, 0.04378635453248858, -0.8580545508879105)
Score of best strategy:  4044.0
Average score of this generation:  1070.184
# third run after fixing breed
Best strategy:  (-0.9731489763848604, 0.3363921402789929, -0.47817871869106465, -0.3524127755254687, 0.4416027082435696, -0.9567837208555914)
Score of best strategy:  4004.0
Average score of this generation:  1341.0
# 4ths run
Best strategy:  (0.38799360079534706, -0.1311962208151709, -0.309459440848745, -0.218616627613897, 0.4299051748694007, -0.9636239078886266)
Score of best strategy:  4308.0
Average score of this generation:  1274.32
Generation 5:
Best strategy:  (-0.45829761936795466, 0.3363921402789929, -0.27479408113890424, -0.36697822783016476, -0.3957981038189615, -0.9567837208555914)
Score of best strategy:  5492.0
Average score of this generation:  1331.552
Generation 6
Current generation average score:  1318.944
Best strategy:  (-0.5688415673654368, -0.032398312716930056, -0.47817871869106465, -0.5320647131196148, -0.8935907658549811, -0.9636239078886266)
Score of best strategy:  5376.0
Average score of this generation:  1318.944
"""
"""
Second run
Current generation average score:  183.392
Best strategy:  (-0.493011158931534, -0.38482271814338787, -0.310820402109252, 0.039636320498527056, 0.281748257935148, -0.7912039619577182)
Score of best strategy:  2720.0
Average score of this generation:  183.392
Generation 1
Best strategy:  (-0.2880428051393329, -0.4498504964430343, 0.01830333276082574, 0.002735089092186227, 0.13834597197922305, -0.5444199232266238)
Score of best strategy:  3252.0
Average score of this generation:  848.872
"""

"""
Run 1:
STATS:
POPULATION_SIZE = 500
TOURNAMENT_SIZE = 20
NUM_CLONES = 75
NUM_TRIALS = 5
MUTATION_RATE = 0.2
Generation 0
Current generation average score:  196.968
Best strategy:  (-0.7851675981217443, -0.48953092057348435, 0.33854604685913703, 0.37663595247563064, -0.5703575624577242, -0.5577501201546666)
Score of best strategy:  3612.0
Average score of this generation:  196.968
Generation 1
Current generation average score:  836.608
Best strategy:  (-0.09617336119820741, 0.1488530626597111, -0.3025513325790077, -0.28063560471049454, 0.38442383474142394, -0.7548800890991691)
Score of best strategy:  3140.0
Average score of this generation:  836.608
Generation 2
Best strategy:  (-0.13379416770664765, -0.5237532610637154, 0.33854604685913703, 0.37663595247563064, -0.13956763416858675, -0.5577501201546666)
Score of best strategy:  4592.0
Average score of this generation:  1025.336
Generation 3:
Current generation average score:  1139.456
Best strategy:  (0.15470737201244678, -0.8174852445731184, 0.7577293739892077, 0.577030689993377, 0.38442383474142394, -0.8816744293718632)
Score of best strategy:  3584.0
Average score of this generation:  1139.456
Generation 4:
Current generation average score:  1179.928
Best strategy:  (-0.386908447521781, -0.6041539599472552, 0.33854604685913703, 0.19099222102623048, -0.6549539531189745, -0.7548800890991691)
Score of best strategy:  4032.0
Average score of this generation:  1179.928

Generation 5:
Current generation average score:  1263.016
Best strategy:  (0.21114406771032712, -0.48953092057348435, 0.33854604685913703, 0.2824972637876879, 0.03689391075154469, -0.8245741830603184)
Score of best strategy:  5116.0
Average score of this generation:  1263.016

Generation 6:
Current generation average score:  1333.496
Best strategy:  (-0.13379416770664765, -0.5852484452074478, 0.6808637913465716, 0.4056257287021887, -0.06532132808810598, -0.8436351892302774)
Score of best strategy:  5680.0
Average score of this generation:  1333.496

Generation 7:
Current generation average score:  1258.584
Best strategy:  (0.15470737201244678, -0.48953092057348435, 0.08208937714279818, 0.2824972637876879, 0.38442383474142394, -0.8816744293718632)
Score of best strategy:  5252.0
Average score of this generation:  1258.584
Generation 8:
Current generation average score:  1302.144
Best strategy:  (-0.5810154835232386, -0.48953092057348435, 0.33854604685913703, 0.19099222102623048, -0.6549539531189745, -0.8245741830603184)
Score of best strategy:  4240.0
Average score of this generation:  1302.144

Generation 9:
urrent generation average score:  1404.936
Best strategy:  (-0.13379416770664765, -0.6041539599472552, 0.4463117930748419, 0.4056257287021887, -0.13956763416858675, -0.8436351892302774)
Score of best strategy:  4244.0
Average score of this generation:  1404.936
"""
"""
RUN 2 (8) generations:
POPULATION_SIZE = 500
TOURNAMENT_SIZE = 20
NUM_CLONES = 75
NUM_TRIALS = 5
MUTATION_RATE = 0.8
Best strategy: (-0.8457106692859053, -0.2335449448977982, 0.25043573008356645, 0.17482527186249563, -0.30938339392800773, -0.9368520226104653)
Score of best strategy: 3192.0
Average score of this generation: 826.624
Best strategy: (-0.9444972786134116, -0.786910862418033, 0.8332695663550571, 0.5977687178703037, -0.7951841871020164, -0.9368520226104653)
Score of best strategy: 3216.0
Average score of this generation: 941.616
Best strategy: (-0.9444972786134116, -0.786910862418033, 0.8332695663550571, 0.5977687178703037, -0.7951841871020164, -0.9917435145877351)
Score of best strategy: 4320.0
Average score of this generation: 1011.744
Best strategy: (-0.9444972786134116, -0.786910862418033, 0.8332695663550571, 0.5977687178703037, -0.838707027944684, -0.9368520226104653)
Score of best strategy: 4520.0
Average score of this generation: 980.48
Best strategy: (-0.42338481084588575, -0.2335449448977982, -0.05634218081266229, 0.06570689629265569, -0.3442869508762665, -0.9368520226104653)
Score of best strategy: 3972.0
Average score of this generation: 1043.808
Best strategy: (-0.18036259323923542, -0.2335449448977982, 0.43948131565564297, 0.09668350866314501, 0.4791461036542728, -0.9313788277136179)
Score of best strategy: 3844.0
Average score of this generation: 969.992
Best strategy: (-0.7474718860115803, -0.30719998627609413, -0.06192635328355167, 0.22916921249288413, -0.1449161365469962, -0.9313788277136179)
Score of best strategy: 3296.0
Average score of this generation: 1003.032
"""
"""
Run 3
Generatiom 0
Current generation average score:  188.648
Best strategy:  (-0.6551579045291827, -0.4070909518676211, -0.07404449465506469, -0.13181439455147914, -0.908601545563088, -0.8806564534467942)
Score of best strategy:  3188.0
Average score of this generation:  188.648


"""