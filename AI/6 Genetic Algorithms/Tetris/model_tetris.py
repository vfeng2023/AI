"""
Piece orientations:
See tetris_orientations.py
"""

# the board is modeled by a list of 20 strings, each one 10 long. A string is a row, an entry in the array in the column
# zero is the bottommost piece


def placeI(board,orientation,loc):
    """
    board - the board. 
    orientation - the direction of the piece
    loc - the place where the leftmost square on the piece goes.
    returns a reference to the board with the modified strings if possible, else None
    board is modified in place, does not return a copy
    """
    if orientation == 0:
        # flat: ####
        # get the highest column
        # for that column-1: replace the start_col,end_col spaces with # 
        col,max_height = highest_heap(board,loc,loc+3)
        row = max_height
        if row >=20:
            return None
        else:
            row_squares = list(board[row])
            for col in range(loc,loc+4):
                row_squares[col] = "#"
            board[row] = "".join(row_squares)
        # remove cleared rows
        board = clearRows(board)
        return board
    elif orientation == 1:
        #
        # 
        #
        # piece
        row,max_height = highest_heap(board,loc,loc)
        if max_height + 3 >= 20:
            return None
        else:
            for i in range(max_height,max_height+4):
                row_list = list(board[i])
                row_list[loc] = '#'
                board[i] = "".join(row_list)
        # remove cleared rows
        board = clearRows(board)
        return board
def placeO(board,start):
    """
    start -- location of leftmost piece
    board- self-evident
    ##
    ## places the O piece
    """
    thing,max_height = highest_heap(board,start,start+1) # max_height is where I start
    if max_height + 1 >= 20:
        return None
    row1 = board[max_height]
    row_squares1 = list(row1)
    row_squares1[start] = "#"
    row_squares1[start+1] = "#"
    board[max_height] = "".join(row_squares1)
    row_squares2 = list(board[max_height+1])
    row_squares2[start] = "#"
    row_squares2[start+1] = "#"
    # remove cleared rows
    i = 0
    board = clearRows(board)
    return board

def placeT(board,orientation,location):
    """
    Places the T block given orientation
    """
    if orientation == 0:
         #
        ###
        _,max_height = highest_heap(board,location,location+2)
        if max_height+1 >=20:
            return None
        row = max_height
        row_squares = list(board[row])
        row_squares[location] = "#"
        row_squares[location+1] = "#"
        row_squares[location+2] = "#"
        board[row] = "".join(row_squares)

        # the tip
        row2 = row+1
        row_squars2 = list(board[row2])
        row_squars2[location+1] = "#"
        board = clearRows(board)
        return board
    elif orientation == 1:
        #
        ## 
        #
        loc,height = highest_heap(board,location,location+1)
        if loc == location:
            row = height
        else: # if the stub occupies the higher spot
            row = height-1
        if row+2 >= 20:
            return None
        board[row] = board[row][:loc] + "#" + board[row][loc+1:]
        board[row+1] = board[row+1][:loc] + "##" + board[row+1][loc+2:]
        board[row+2] = board[row+2][:loc] + "#" + board[row+1][loc+1:]
        board = clearRows(board)
        return board
    elif orientation == 2:
        ###
         #
        loc,height = highest_heap(board,location,location+2)
        # account for the stub
        if loc == location+1:
            row = height
        else:
            if board[height][location] == board[height][location+1] and board[height][location+1] == board[height][location+2]:
                # if the same level
                row = height
            else:
                row = height-1
        if row+1 >= 20:
            return None
        board[row] = board[row][:loc+1] + "#" + board[row][loc+2:]
        board[row+1] = board[row+1][:loc] + "###" + board[row][loc+3:]
        board = clearRows(board)
        return board
    else:
         #
        ##
         #
        loc,height = highest_heap(board,location,location+1)
        if loc == location+1:
            row = height-1
        else:
            row = height
        board[row] = board[row][:loc+1]+"#" + board[row][loc+2:]
        board[row+1] = board[row+1][:loc]+"##" + board[row+1][loc+2:]
        board[row+2] = board[row+2][:loc+1] +"#" + board[row+2][loc+2:] 
        board = clearRows(board)
        return board


def clearRows(board):
    i = 0
    while i < len(board):
        if board[i] == "##########":
            del board[i]
            board.append(" "*10)
        else:
            i += 1
    return board
def highest_heap(board,start_col,end_col):
    """
    returns the highest heap and column where it is
    returns column, height of maximum heap
    """
    max_col = start_col
    max_height = -1
    for col in range(start_col,end_col+1):
        # get a list with the column itself, then find index of latest # 
        board_column = [board[i][col] for i in range(20)]
        height = rindex(board_column)
        if height > max_height:
            max_height = height
            max_col = col
    return max_col,max_height+1
def rindex(array):
    for i in range(len(array)-1,-1,0):
        if array[i] == "#":
            return i
    return -1
def lowest_heap(board,start_col,end_col):
    """
    returns the lowest heap and column where it is
    returns column, height of minimum heap
    """
    min_col = start_col
    min_height = 20
    for col in range(start_col,end_col+1):
        # get a list with the column itself, then count the number of "#"
        board_column = list(board[i][col] for i in range(20))
        height = rindex(board_column)
        if height < min_height:
            min_height = height
            min_col = col
    return min_col,min_height+1

board = [" "*10 for i in range(20)]
for i in range(2):
    placeI
