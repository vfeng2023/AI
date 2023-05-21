import sys; args = ["3x3","9","wordlist.txt"]# sys.argv[1:]
# myLines = open(args[0],'r').read().splitlines()
import random
numRows,numCols = int(args[0].split("x")[0]),int(args[0].split("x")[1])
print(numRows,numCols)
blockedSquares = int(args[1])
dictionaryfile = args[2]
# print(args)

# store the seed strings, according to whether they are vertical or horizontal, in the appropriate array
# format: (row,col,"WORD) if word is empty, then there is a blocking square.
horizontal = []
vertical = []

for i in range(3,len(args)):
    seedstring = args[i]
    rem = seedstring[1:]
    for alphaInd in range(rem.index("x")+1,len(rem)):
        if rem[alphaInd].isalpha():
            break
    stuff = rem[:alphaInd].split("x")
    row = int(stuff[0])
    col = int(stuff[1])
    if seedstring[0] == "H":
        horizontal.append((row,col,rem[alphaInd:].upper()))
    else:
        vertical.append((row,col,rem[alphaInd:].upper()))
print(horizontal,"Horizontal")
print(vertical,"vertical")
# print("height,width",height,width)
# print("blocked squares=",blockedSquares)
# print(dictionaryfile)
# print("Horizontal requirements",horizontal)
# print("vertical requirements,",vertical)

# create list of characters representation of the crossword
crossGrid = ["-"]*numRows*numCols
# fill in the "given" values
for H in horizontal:
    row,col,word = H
    if word == "":
        crossGrid[numRows*row + col] = "#"
    else:
        for c in range(col,col+len(word)):
            crossGrid[numRows*row + c] = word[c-col]

for V in vertical:
    row,col,word = V
    if word == "":
        crossGrid[numRows*row+col] = "#"
    else:
        for r in range(row,row+len(word)):
            crossGrid[numCols*r+col] = word[r-row]

def printBoard(grid,numrows,numcols):
    for i in range(numrows):
        for j in range(numcols):
            print(grid[i*numcols+j],end = " ")
            # print(i*numcols+j,end = " ")
            
        print()
def placeBlocks(board,placed,numrows,numcols,allowed):
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
    # - = allowed to go there
    # . = don't put blocking square here
    prev_board = board
    curr_board = board.copy()
    while placed < allowed:
        next_spot = random.choice(next_space(curr_board))
        row = next_spot//numcols
        col = next_spot % numrows
        result = place(row,col,curr_board)
        
        if result:
            # adds if successfully placed
            placed += 2
        else:
            prev_board[row*numCols+col] = "."
            curr_board = prev_board
            continue
        check_board = curr_board.copy()
        try:
            index = check_board.index("-")
        except ValueError:
            index = -1
        check_continuity(check_board,index//numcols,index%numrows,numrows,numcols,"-.")
        if "-" in check_board or "." in check_board:
            prev_board[row*numCols+col] = "."
            curr_board = prev_board
            placed -= 2
            continue
        prev_board = curr_board
        curr_board = curr_board.copy()
    return curr_board
# def placeBlocks(board,placed,allowed):
#     """
#     Backtracking algorithm for placing the squares on the block
#     """
#     if placed == allowed:
#         return board
    # next space = get_next_space(board)
    # new_board = board.copy()
    # new_board = place on new_board blocking square
    # if new_board is invalid(check_continuity fails or placed location overlaps):
        # return None
def isvalid(row,col,numrows,numcols,board):
    if row < 0 or row >= numrows or col < 0 or col >= numcols:
        return False
    if board[row*numCols + col] == "#":
        return False
    return True

def next_space(board):
    poss_choices = []
    for i in range(len(board)):
        if board[i]=='-':
            poss_choices.append(i)
    return poss_choices
def place(r,c,board):
    """
    places block at space r, c and also opposite location. Adds a total of 2 placed pieces
    """
    board[r*numCols + c] = "#"
    oppr = numRows-1 - r
    oppc = numCols-1 - c
    opposite_spot = oppr*numCols+oppc
    if board[opposite_spot] == '-':
        board[oppr*numCols+oppc] = "#"
        return True
    else:
        return False
def check_continuity(board,row,col,numrows,numcols,char): # char is "-."
    """
    replaces every instance of char in board with a *.
    if board.find(original_char)!=-1:
        board is not continuous
    """
    if row >= numrows or row < 0 or col >=numcols or col < 0 or board[numcols*row+col] not in char:
        return
    board[row*numcols+col] = "*"
    check_continuity(board,row,col+1,numrows,numcols,char)
    check_continuity(board,row,col-1,numrows,numcols,char)
    check_continuity(board,row+1,col,numrows,numcols,char)
    check_continuity(board,row-1,col,numrows,numcols,char)


printBoard(placeBlocks(crossGrid,0,numRows,numCols,blockedSquares),numRows,numCols)