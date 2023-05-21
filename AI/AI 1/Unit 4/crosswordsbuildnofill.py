import sys; args = sys.argv[1:]
# myLines = open(args[0],'r').read().splitlines()
import random


def printBoard(grid,numrows,numcols):
    if grid is None:
        print(None)
        return
    for i in range(numrows):
        for j in range(numcols):
            print(grid[i*numcols+j],end = " ")
            # print(i*numcols+j,end = " ")
            
        print()
    print()
def placeBlocks(board,placed,numrows,numcols,allowed):
    """
    Function to call to completely place blocks
    """
    # while placed != allowed:
        # nextsquare = get_next_square()
        # if space up down left right has less than three square:
            # place blocking squares there to fill it
        # get next square(random space on board)
        # check for continuity
        # if not continuous:
            # revert to previous board
            # choose another space
    placed = 0
    center = len(board)//2
    if numrows%2==1 and numcols%2==1:
        if allowed %2 == 1:
            board[center] = "#" # adds a block if oddsized board, odd number of blocking squares
            placed += 1
        else:
            board[center] = "." # add a dot at the center if odd sized board, even squares
    
    filled_board = backtrack(board,allowed,numrows,numcols)
    return filled_board

def backtrack(board,allowed,numrows,numcols):
    """
    Backtracking function to find a good arrangement of blocks
    """
    placed = board.count("#")
    # printBoard(board,numrows,numcols)
    if placed > allowed:
        return None
    # if continuitycheck fails:
        # return None

    if placed == allowed:
        if iscontinuous(board.copy(),numrows,numcols):
            return board
        else:
            return False
    # for space in valid spaces:
        # nb = place_block(space)
        # if nb is not None:
            # result backtrack(nb)
            # if result is valid:
                # return nb
    for space in valid_spaces(board):
        row = space//numCols
        col = space%numCols
        nb = board.copy()
        place_res = place_square(nb,row,col,numrows,numcols)
        # printBoard(nb,numrows,numcols)
        if place_res is False:
            continue
        # if newlplaced == allowed and iscontinuous(nb.copy(),numrows,numcols):
        #     return nb
        nb = fill_gaps(nb,numrows,numcols)
        # printBoard(nb,numrows,numcols)
        if nb is not None:
            result = backtrack(nb,allowed,numrows,numcols)
            if result is not None:
                return result
            
    # should add blocks horizontally and vertically if blocking squares or borders are within 3 block vicinity
        # this step is also symmetric -- terminates if not possible
    
    # increases newly_placed accordingly
    # return board, newly_placed (or None, newly_placed) <-- newly_placed should be added onto placed blocks 

def valid_spaces(board):
    """
    Return a set of valid spaces indexes
    """
    allowed = set()
    for i in range(len(board)):
        if board[i]=="-":
            allowed.add(i)
    return allowed
def fill_gaps(board,numRows,numCols):
    """
    # fills the board such that all blocks with  or less gaps are filled(total_added DOES NOT work)
    """
    for i in range(len(board)):
        if board[i] == "#" and i !=len(board)//2:
            row = i//numCols
            col = i%numCols
            # up down left right
            # up
            # printBoard(board,numRows,numCols)
            # print("index",i)
            for rup in range(row-3,row):
                if rup < 0 or board[rup*numCols+col] == "#":
                    for k in range(row-3,rup):
                        # printBoard(board,numRows,numCols)
                        # print()
                        place_res,ind = place_square(board,k,col,numRows,numCols)
                        # if place_res is not None:
                        if place_res is False:
                            return None         
            # down
            # printBoard(board,numRows,numCols)
            # print("index",i)
            for rdown in range(row+1,row+4):
                if rdown >= numRows or board[rdown*numCols+col] == "#":
                    for k in range(row,rdown):
                        place_res,ind = place_square(board,k,col,numRows,numCols)
                        # if place_res is not None:
                        if place_res is False:
                            return None
                            
            # left
            # printBoard(board,numRows,numCols)
            # print("index",i)
            for cleft in range(col-3,col):
                if cleft < 0 or board[row*numCols+cleft] == "#":
                    for k in range(col-3,cleft):
                        place_res,ind= place_square(board,row,k,numRows,numCols)
                        # if place_res is not None:
                        if place_res is False:
                            return None
            # right
            # printBoard(board,numRows,numCols)
            # print("index",i)

            for cright in range(col,col+4):
                if cright >= numCols or board[row*numCols+cright] == "#":
                    for k in range(col+1,cright):
                        place_res,ind = place_square(board,row,k,numRows,numCols)
                        # if place_res is not None:
                        if place_res is False:
                            return None
    return board


def place_square(board,r,c,numRows,numCols):
    """
    Places square at (r,c) and opposite if valid. Returns True + index if placement successful(other wise, bool,-1)
    """
    index = r*numCols + c
    if 0<=r < numRows and 0<=c< numCols and (board[index] == "-" or board[index] == "#"):
        prev = board[index]
        board[r*numCols+c] = "#"
        oppr = numRows-1-r
        oppc = numCols-1-c
        opp = oppr*numCols+oppc
        
        if board[opp] == "-" or board[opp]=="#":
            board[opp] = "#"
            if prev == "#":
                return True,-1
            else:
                return True,index
        else:
            board[r*numCols+c] = prev
            return False,-1
    return None,-1

def check_continuity(board,row,col,numrows,numcols): # char is "-."
    """
    replaces every instance of char in board with a *.
    call board.find("-") to find location to start  
    if board.find(original_char)!=-1:
        board is not continuous
    """
    if row >= numrows or row < 0 or col >=numcols or col < 0 or board[row*numcols+col]=="*" or board[row*numcols+col] == "#":
        return
    # printBoard(board,numrows,numcols)
    board[row*numcols+col] = "*"
    check_continuity(board,row,col+1,numrows,numcols)
    check_continuity(board,row,col-1,numrows,numcols)
    check_continuity(board,row+1,col,numrows,numcols)
    check_continuity(board,row-1,col,numrows,numcols)

def iscontinuous(board,numRows,numCols):
    """
    Checks if board is continuous
    """
    try:
        start = board.index("-")
    except ValueError:
        return True
    else:
        check_continuity(board,start//numCols,start%numCols,numRows,numCols)
        if "-" in board:
            return False
        if board[len(board)//2]==".":
            return False
    return True
# # testing place_squares
# board = ["-"]*25
# board[11] = "#"
# board[13] = "#"

# printBoard(board,5,5)
# print("call")
# # place_square(board,1,1,5,5)
# fill_gaps(board,5,5)
# print("fill_gaps call")
# printBoard(board,5,5)

"""Grid building code starts here"""
numRows,numCols = int(args[0].split("x")[0]),int(args[0].split("x")[1])
blockedSquares = int(args[1])
dictionaryfile = args[2]
# print(args)

# store the seed strings, according to whether they are vertical or horizontal, in the appropriate array
# format: (row,col,"WORD") if word is empty, then there is a blocking square.
horizontal = []
vertical = []

for i in range(3,len(args)):
    seedstring = args[i]
    rem = seedstring[1:]
    for alphaInd in range(rem.index("x")+1,len(rem)):
        if rem[alphaInd].isalpha() or rem[alphaInd]=="#":
            break
    stuff = rem[:alphaInd].split("x")
    row = int(stuff[0])
    col = int(stuff[1])
    if seedstring[0].upper() == "H":
        horizontal.append((row,col,rem[alphaInd:].upper()))
    else:
        vertical.append((row,col,rem[alphaInd:].upper()))
# print(horizontal,"Horizontal")
# print(vertical,"vertical")


# create list of characters representation of the crossword
crossGrid = ["-"]*numRows*numCols
# fill in the "given" values
for H in horizontal:
    row,col,word = H
    if word == "":
        place_square(crossGrid,row,col,numRows,numCols)
    else:
        for c in range(col,col+len(word)):
            crossGrid[numRows*row + c] = word[c-col]

for V in vertical:
    row,col,word = V
    if word == "":
        place_square(crossGrid,row,col,numRows,numCols)
    else:
        for r in range(row,row+len(word)):
            crossGrid[numCols*r+col] = word[r-row]

# print(blockedSquares)
# place_square(crossGrid,0,3,5,5)
# # place_square(crossGrid,2,0,5,5)
# # printBoard(crossGrid,5,5)
# printBoard(crossGrid,5,5)
# # filled = fill_gaps(crossGrid,5,5)
# fill_gaps(crossGrid,numRows,numCols)
# filled = placeBlocks(crossGrid,0,numRows,numCols,blockedSquares)
# printBoard(filled,numRows,numCols)
filled = placeBlocks(crossGrid,0,numRows,numCols,blockedSquares)

if filled[len(filled)//2] == ".":
    filled[len(filled)//2] = "-"

printBoard(filled,numRows,numCols)
# Vivian Feng, 3, 2023