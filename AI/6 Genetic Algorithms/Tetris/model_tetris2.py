"""
Piece orientations:
See tetris_orientations.py
"""
import sys
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

# convert the piece + orientation into a character
# go through the reversed string and try placement in chucks of 10
# if can successfully place:
# return board with that configuration
# else:
    # return None
def place_piece(board,piece,orientation,location):
    curr_piece = TETRIS_PIECES[piece][orientation]
    # location is 0 index
    piece_mask = ""
    size = len(curr_piece[0])
    for row in curr_piece:
        piece_mask += (" "*(location)) + row + (" "* (10-size-(location)))
    if len(piece_mask) > len(curr_piece) * 10:
        return None
    # attempt placement, bottoms up
    for i in range(0,len(board),10):
        board_seg = board[i:i+len(piece_mask)]
        result = mask(piece_mask,board_seg)
        if result is not None:
            board = board[:i] + result + board[i+len(result):]
            boardAsList = [board[i:i+10] for i in range(0,len(board),10)]
            boardAsList = clearRows(boardAsList)
            board = "".join(boardAsList)
            return board

    return "GAME OVER"
def clearRows(board):
    i = 0
    while i < len(board):
        if board[i] == "##########":
            del board[i]
            board.append(" "*10)
        else:
            i += 1
    return board
def mask(piece,board_segment):
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
# test = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
# reverse the board so it is in bottom up order
# test = #"          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
test = sys.argv[1]
bAsList = [test[i:i+10] for i in range(0,len(test),10)]
bAsList.reverse()
board = "".join(bAsList)
outputStates = list()
for piece in TETRIS_PIECES:
    for orient in TETRIS_PIECES[piece]:
        # print("piece=",piece,", orientation=",orient)
        for i in range(0,10):
            newboard = place_piece(board,piece,orient,i)
            
            if newboard is not None:
                row_majorlist = [newboard[i:i+10] for i in range(0,len(newboard),10)]
                row_majorlist.reverse()
                row_major = "".join(row_majorlist)
                outputStates.append(row_major+"\n")
                # print_board(newboard)
        # input()
with open("tetrisout.txt","w") as f:
    f.writelines(outputStates)
f.close()