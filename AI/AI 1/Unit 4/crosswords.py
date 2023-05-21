import sys; args = ["11x13","27","wordlist.txt","H0x0begin","V8x12end"]# sys.argv[1:]
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
    # while placeed != allowed:
        # nextsquare = get_next_square()
        # if space up down left right has less than three square:
            # place blocking squares there to fill it
        # get next square(random space on board)
        # check for continuity
        # if not continuous:
            # revert to previous board
            # choose another space
    center = (row-1)//2 *numcols + (col-1)//2
    if numrows%2==1 and numcols%2==1 and allowed %2 == 1:
        board[center] = "#"
    placed = 0
    new_board = board.copy()
    while placed < allowed:
        next = random.choice(next_space(new_board))
        board[next] = "#"
        placed += 1
        left = [-3,-2,-1]
        right = [1,2,3]

    
def isvalid(row,col,numrows,numcols):
    return 0<=row < numrows and 0<=col<numcols

def next_space(board):
    poss_choices = []
    for i in range(len(board)):
        if board[i]=='-':
            poss_choices.append(i)
    return poss_choices

def check_continuity(board,row,col,numrows,numcols,char):
    """
    replaces every instance of char in board with a *.
    if board.find(original_char)!=-1:
        board is not continuous
    """
    if row >= numrows or row < 0 or col >=numcols or col < 0 or board[numcols*row+col]!=char:
        return
    board[row*numcols+col] = "*"
    check_continuity(board,row,col+1,numrows,numcols,char)
    check_continuity(board,row,col-1,numrows,numcols,char)
    check_continuity(board,row+1,col,numrows,numcols,char)
    check_continuity(board,row-1,col,numrows,numcols,char)
    
        
print(numRows,numCols)
printBoard(crossGrid,numRows,numCols)
print("".join(crossGrid))
