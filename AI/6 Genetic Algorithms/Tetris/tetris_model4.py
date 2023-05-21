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
    print(piece,orientation)
    print("location: ",location)
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
test = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
# reverse the board so it is in bottom up order
# test = #"          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
# test = sys.argv[1]
# test = " "*200 # try empty board
bAsList = [test[i:i+10] for i in range(0,len(test),10)]
bAsList.reverse()
board = "".join(bAsList)
column_heights = [0 for i in range(10)]
for i in range(10):
    column_heights[i] = rindex([bAsList[row][i] for row in range(len(bAsList))])
print(column_heights)
# input()
outputStates = list()
print_board(board)
# input()
for piece in TETRIS_PIECES:
    for orient in TETRIS_PIECES[piece]:
        # print("piece=",piece,", orientation=",orient)
        for i in range(0,10):
            # print("pice",piece,orient)
            # print("location",i)
            new_col_heights = column_heights.copy()
            newboard,_ = place_piece(board,piece,orient,i,new_col_heights)
            # if newboard is not None:
                
            #     print_board(newboard)
            if newboard is not None:
                row_majorlist = [newboard[i:i+10] for i in range(0,len(newboard),10)]
                row_majorlist.reverse()
                row_major = "".join(row_majorlist)
                outputStates.append(row_major+"\n")
            # else:
            #     outputStates.append("GAME OVER\n")
        # print_board(newboard)
        # input()
new_board,_ = place_piece(board,"I",1,0,column_heights)
print_board(new_board)
with open("tetrisout.txt","w") as f:
    f.writelines(outputStates)
f.close()

# new_board,_ = place_piece(board,"J",2,0,column_heights)
# print_board(new_board)
# board = [" "*10 for i in range(20)]
# board[0] = "####      "
# columns = [1,1,1,1,0,0,0,0,0,0]
# newboard = "".join(board)
# newboard,_ = place_piece(newboard,"J",1,1,columns)
# print_board(newboard)

# board = " "*200
# columns = [0 for _ in range(10)]
# for piece in TETRIS_PIECES:
#     for orient in TETRIS_PIECES[piece]:
#         new_columns = columns.copy()
#         new_board,_ = place_piece(board,piece,orient,0,new_columns)
#         print_board(new_board)
#         print("Columns",new_columns)
#         input()
