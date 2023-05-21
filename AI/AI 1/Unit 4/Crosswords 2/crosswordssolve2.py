import sys
args = ['3x3','0',"sample.txt"]# sys.argv[1:]
import random,string
def printBoard(grid,numRows,numCols):
    if grid is None:
        print(None)
        return
    for i in range(numRows):
        for j in range(numCols):
            print(grid[i*numCols+j],end = " ")
            # print(i*numCols+j,end = " ")
            
        print()
    print()
def placeBlocks(board,placed,numRows,numCols,allowed):
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
    if numRows%2==1 and numCols%2==1:
        if allowed %2 == 1:
            board[center] = "#" # adds a block if oddsized board, odd number of blocking squares
            placed += 1
        else:
            if not board[center].isalpha():
                board[center] = "." # add a dot at the center if odd sized board, even squares
    # blocked squares already on board
    indices = []
    for i in range(len(board)):
        if board[i] == "#":
            place_square(board,i//numCols,i%numCols,numRows,numCols)
            indices.append(i)
    # printBoard(board,numRows,numCols)
    filled_board = fill_gaps(board,numRows,numCols,indices)
    # printBoard(filled_board,numRows,numCols)
    # fills the board
    original_board = filled_board.copy()
    spaces = list(valid_spaces(original_board,numRows,numCols))
    while iscontinuous(copy:=filled_board.copy(),numRows,numCols)==False or filled_board.count("#") > allowed:
        filled_board = original_board.copy()
        start = random.choice(spaces)
        # printBoard(copy,numRows,numCols)
        initial_fill_continuity(filled_board,start//numCols,start%numCols,numRows,numCols,replacement="#")
        # print("Current trial start board")
        # printBoard(filled_board,numRows,numCols)
    
    # printBoard(filled_board,numRows,numCols)
    # printBoard(filled_board,numRows,numCols)
    # print(filled_board.count("#"))
    filled_board = backtrack(filled_board,allowed,numRows,numCols)
    return filled_board

def backtrack(board,allowed,numRows,numCols):
    """
    Backtracking function to find a good arrangement of blocks
    """
    placed = board.count("#")
    # 
    # print(placed)
    # print(placed)
    # printBoard(board,numRows,numCols)
    if placed > allowed:
        return None
    # if continuitycheck fails:
        # return None
    # if not iscontinuous(board.copy(),numRows,numCols):
    #     return None
    if placed == allowed:
        if iscontinuous(board.copy(),numRows,numCols):
            return board
        else:
            return None
    # for space in valid spaces:
        # nb = place_block(space)
        # if nb is not None:
            # result backtrack(nb)
            # if result is valid:
                # return nb
    spaces = valid_spaces(board,numRows,numCols)
    while len(spaces) > 0:
        # choose next move
        # if placed > 0.90*allowed:
            # if not iscontinuous(board.copy(),numRows,numCols):
            #     return None
            # printBoard(board,numRows,numCols)
        # printBoard(board,numRows,numCols)
        space = next_space(board,numRows,numCols,spaces)
        # space = random.choice(list(spaces))
        spaces.remove(space)
        if len(board) - space - 1 in spaces:
            spaces.remove(len(board)-space-1)
        # get the rows and columns
        row = space//numCols
        col = space%numCols
        nb = board.copy()
        # attempt initial placement
        place_res,ind = place_square(nb,row,col,numRows,numCols)
        # printBoard(nb,numRows,numCols)
        # print(nb)
        # printBoard(nb,numRows,numCols)
        if place_res is True and ind !=-1:
            checked_board = fill_gaps(nb,numRows,numCols,[space])
            # printBoard(checked_board,numRows,numCols)
            # printBoard(nb,numRows,numCols)
            if checked_board is not None and iscontinuous(checked_board.copy(),numRows,numCols):           
                result = backtrack(checked_board,allowed,numRows,numCols)
                
                if result is not None:
                    return result
            
    # should add blocks horizontally and vertically if blocking squares or borders are within 3 block vicinity
        # this step is also symmetric -- terminates if not possible
    
    # increases newly_placed accordingly
    # return board, newly_placed (or None, newly_placed) <-- newly_placed should be added onto placed blocks 

def valid_spaces(board,numRows,numCols):
    """
    Return a set of valid spaces indexes
    """
    corners = {0,numCols-1,(numRows-1)*numCols,len(board)-1}
    allowed = set()
    for i in range(len(board)):
        if board[i]=="-":
            # check up down left right if there are blocking squares within its vicinity
            row = i//numCols
            col = i%numCols
            # # checking left to right 
            # for r in range(row-3,row+4):
            #     if r < 0 or r >=numRows:
            #         continue
            #     if board[numCols*r+col] == "#":
            #         continue
            # # checking up and down
            # for c in range(col-3,col+4):
            #     if c < 0 or c >= numCols:
            #         continue
            #     if board[numCols*row+c] == "#":
            #         continue
            allowed.add(i)
    return allowed
def fill_gaps(board,numRows,numCols,indices):
    """
    # fills the board such that all blocks with  or less gaps are filled(total_added DOES NOT work)
    """

    for i in range(len(board)):
        if board[i] == "#":
            row = i//numCols
            col = i%numCols
            # up down left right
            # up
            # printBoard(board,numRows,numCols)
            # print("index",i)
            for rup in range(row-3,row):
                if rup < 0 or board[rup*numCols+col] == "#":
                    for k in range(rup,row):
                        # printBoard(board,numRows,numCols)
                        # print()
                        place_res,ind = place_square(board,k,col,numRows,numCols)
                        # if place_res is not None:
                        if place_res is False:
                            return None
                        # if ind!=-1:
                        #     indices.append(ind)         
            # # down
            # printBoard(board,numRows,numCols)
            # print("index",i)
            for rdown in range(row+1,row+4):
                if rdown >= numRows or board[rdown*numCols+col] == "#":
                    for k in range(row,rdown+1):
                        place_res,ind = place_square(board,k,col,numRows,numCols)
                        # if place_res is not None:
                        if place_res is False:
                            return None
                        # if ind !=-1:
                        #     indices.append(ind)
                            
            # left
            # printBoard(board,numRows,numCols)
            # print("index",i)
            for cleft in range(col-3,col):
                if cleft < 0 or board[row*numCols+cleft] == "#":
                    for k in range(cleft,col):
                        place_res,ind= place_square(board,row,k,numRows,numCols)
                        # if place_res is not None:
                        if place_res is False:
                            return None
                        # if ind!=-1:
                        #     indices.append(ind)
                        
            # right
            # printBoard(board,numRows,numCols)
            # print("index",i)

            for cright in range(col,col+4):
                if cright >= numCols or board[row*numCols+cright] == "#":
                    for k in range(col,cright+1):
                        place_res,ind = place_square(board,row,k,numRows,numCols)
                        # if place_res is not None:
                        if place_res is False:
                            return None
                        # if ind!=-1:
                        #     indices.append(ind)
                        # printBoard(board,numRows,numCols)
    return board


def place_square(board,r,c,numRows,numCols):
    """
    Places square at (r,c) and opposite if valid. Returns True + index if placement successful(other wise, bool,-1)
    """
    index = r*numCols + c
    if 0<=r < numRows and 0<=c< numCols:
        if board[index] == "-" or board[index] == "#":
            prev = board[index]
            board[r*numCols+c] = "#"
            oppr = numRows-1-r
            oppc = numCols-1-c
            opp = oppr*numCols+oppc
            # printBoard(board,numRows,numCols)
            if board[opp] == "-" or board[opp]=="#":
                board[opp] = "#"
                # printBoard(board,numRows,numCols)
                if prev == "#":
                    return True,-1
                else:
                    return True,index
            else:
                board[r*numCols+c] = prev
                return False,-1
        return False,-1
    return None,-1

def check_continuity(board,row,col,numRows,numCols,replacement="*"): # char is "-."
    """
    replaces every instance of char in board with a *.
    call board.find("-") to find location to start  
    if board.find(original_char)!=-1:
        board is not continuous
    """
    if row >= numRows or row < 0 or col >=numCols or col < 0 or board[row*numCols+col]=="*" or board[row*numCols+col] == "#":
        return
    #printBoard(board,numRows,numCols)
    board[row*numCols+col] = replacement
    check_continuity(board,row,col+1,numRows,numCols,replacement)
    check_continuity(board,row,col-1,numRows,numCols,replacement)
    check_continuity(board,row+1,col,numRows,numCols,replacement)
    check_continuity(board,row-1,col,numRows,numCols,replacement)
def next_space(board,numRows,numCols,spaces):
    bestSpace = []
    mostOpen = -float('inf')
    for s in spaces:
        row = s//numCols
        col = s%numCols
        count = 0
        # count the number of open spaces up down left firhg 
        for r in range(row-3,row+4):
            if 0<=r<numRows and board[r*numCols+col] !="#":
                count += 1

        for c in range(col-3,col+4):
            if 0 <=c < numCols and board[row*numCols+c]!="#":
                count += 1
        # count diagonal pieces
        if count == mostOpen:
            bestSpace = s 
        elif count > mostOpen:
            bestSpace = s
            mostOpen = count
    return bestSpace
                
# does the intial placement of the blocks
def initial_fill_continuity(board,row,col,numRows,numCols,replacement = "#"):
    if row >= numRows or row < 0 or col >=numCols or col < 0 or board[row*numCols+col]=="*" or board[row*numCols+col] == "#":
        return
    boolean,ind = place_square(board,row,col,numRows,numCols)
    if boolean is False:
        return
    initial_fill_continuity(board,row,col+1,numRows,numCols,replacement)
    initial_fill_continuity(board,row,col-1,numRows,numCols,replacement)
    initial_fill_continuity(board,row+1,col,numRows,numCols,replacement)
    initial_fill_continuity(board,row-1,col,numRows,numCols,replacement)

def iscontinuous(board,numRows,numCols):
    """
    Checks if board is continuous
    """
    try:
        if board[len(board)//2]==".":
            start = len(board)//2
        start = board.index("-")
    except ValueError:
        return True
    else:
        check_continuity(board,start//numCols,start%numCols,numRows,numCols)
        if "-" in board:
            return False
    return True


"""Grid building code starts here"""
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
    for alphaInd in range(rem.index("x")+1,len(rem)+1):
        if alphaInd >= len(rem) or rem[alphaInd].isalpha() or rem[alphaInd] == "#":
            break
    stuff = rem[:alphaInd].split("x")
    row = int(stuff[0])
    col = int(stuff[1])
    if seedstring[0].upper() == "H":
        horizontal.append((row,col,rem[alphaInd:].upper()))
    else:
        vertical.append((row,col,rem[alphaInd:].upper()))


# create list of characters representation of the crossword
crossGrid = ["-"]*numRows*numCols
# fill in the "given" values
for H in horizontal:
    row,col,word = H
    if word == "":
        place_square(crossGrid,row,col,numRows,numCols)
    else:
        for c in range(col,col+len(word)):
            crossGrid[numCols*row + c] = word[c-col]

for V in vertical:
    row,col,word = V
    if word == "":
        place_square(crossGrid,row,col,numRows,numCols)
    else:
        for r in range(row,row+len(word)):
            crossGrid[numCols*r+col] = word[r-row]

filled = placeBlocks(crossGrid,0,numRows,numCols,blockedSquares)
if filled[len(filled)//2] == ".":
    filled[len(filled)//2] = "-"
# printBoard(filled,numRows,numCols)

"""Part 2 starts here"""
# read valid words
with open(dictionaryfile) as f:
    all_words = set()
    lengthMapping = dict() # dict(length:dict(letter:set(words)))
    prefix_tree = dict() # dict(pre:set(letters))
    prefix_tree[""] = set(string.ascii_uppercase)
    lengthPrefixTree = dict() # dict(length: dict(prefix_words of that length))
    
    for line in f.readlines():
        word = line.strip().upper()
        if len(word) >= 3 and word.isalpha():
            all_words.add(word)
            for i in range(1,len(word)+1):
                if (pre:=word[:i]) not in prefix_tree:
                    prefix_tree[pre] = set()
                prefix_tree[pre].add(pre)

            if (length:=len(word)) not in lengthMapping:
                lengthMapping[len(word)] = dict()
            if word[0] not in lengthMapping[length]:
                lengthMapping[length][word[0]] = set()
            lengthMapping[length][word[0]].add(word)

            for i in range(1,len(word)+1):
                if (pre:=word[:i]) not in prefix_tree:
                    prefix_tree[pre] = set()
                prefix_tree[pre].add(pre)
                if length not in lengthPrefixTree:
                    lengthPrefixTree[length] = dict()
                if pre not in lengthPrefixTree[length]:
                    lengthPrefixTree[length][pre] = set()
                if i < len(word):
                    lengthPrefixTree[length][pre].add(word[i:i+1]) # prefix tree maps each prefix to possible next letters
                    # empty set indicates complete word


        
    # build the prefix tree for words
    # build length --> word --> words of length which start with letter mapping dict(len:dict(letter: list w/ words of that length))
# get corners of the grid filled
corners = []
horzStart = dict() # dict(int:list(int)) for that horizontal
vertStart = dict() # dict(int: list(int)) for that vertical
print(numRows,numCols)
for sq in range(len(filled)):
    if filled[sq] == "-":
        row = sq//numCols
        col = sq % numCols
        if (row - 1 < 0 or filled[(row-1)*numCols + col] == "#") and (col-1 < 0 or filled[row*numCols+col-1] == "#"):
            corners.append(sq)
        if row - 1 < 0 or filled[(row-1)*numCols + col] == "#":
            vertStart[sq] = []
            r = row
            while r < numRows and filled[r*numCols+col] != "#":
                vertStart[sq].append(r*numCols+col)
                r+= 1
        if col-1 < 0 or filled[row*numCols+col-1] == "#":
            horzStart[sq] = []
            c = col
            while c < numCols and filled[row*numCols+c] != "#":
                horzStart[sq].append(row*numCols + c)
                c += 1
print(corners)
print(horzStart)
print(lengthMapping)
print(lengthPrefixTree)
startToIndex = dict() # dict(int:dict("H:hstart, "V":vstart))
for key in horzStart:
    for ind in horzStart[key]:
        if ind not in startToIndex:
            startToIndex[ind] = dict()
        startToIndex[ind]["H"] = key
for key in vertStart:
    for ind in vertStart[key]:
        if ind not in startToIndex:
            startToIndex[ind] = dict()
        startToIndex[ind]["V"] = key
# get startsToIndex, indexTostarts mapping
horzwords = dict()
vertWords = dict()
usedWords = set()
for h in horizontal:
    row,col,word = h 
    if word in all_words:
        horzwords[row*numCols+col] = h
        usedWords.add(word)
for v in vertical:
    row,col,word = v
    if word in all_words:
        vertWords[row*numCols+col] = v
        usedWords.add(word)
def add_letters(filled,all_words):
    for c in corners:
        
        for letter in prefix_tree[""]:# prefix_tree[""]:
            new_board = filled.copy()
            new_board[c] = letter
            result = build_subgrid(c,new_board.copy(),horzStart,vertStart,startToIndex,prefix_tree,lengthMapping,all_words)
            if result is not None:
                return result

def build_subgrid(corner,board,horzStart,vertStart,indexToStart,prefix_tree,lengthMapping,all_words,vertWords,HorzWords):
    """
    places the initial subgrid condition
    """
    # horzSpaces = horzStart[corner]
    # vertSpaces = vertStart[corner]
    # startChar = board[corner]
    # possHorzChar = lengthMapping[len(horzSpaces)][startChar]
    # possVertChar = lengthMapping[len(vertSpaces)][startChar]
    # horizontalWords = dict() #index --> words at index
    # verticalWords = dict() # index --> words at vertical index
    # startRow = corner//numCols
    # startCol = corner%numCols
    lengthMapping[]


def build_vertical(board,row,column,prevRow,prevCol,indexToStart): # other constants and auxillary variables
    """
    -->
      |
      V
    should have an initial horizontal "seed" placed, only places one row's vertical words
    """
    
    # if row,column is blocking square:
    if row >=numRows or board[row*numCols+column] == "#":
        # get the prev row, col.
        # check the word that was placed
        space = prevRow*numCols+prevCol
        vert = indexToStart[space]["V"]
        vertWord = vertWords[vert]
        if vert in all_words:
            return board
        else:
            return None
        # if word not in used and is word:
            # return Board
        # otherwise:
            # return None
    # if row <= numRows or col >= numCols:

        # get the word above
        # if word is in used:
            # return None
        # otherwise: 
            # return board

    # get the start of the square(aka the index of the initial word)
    index = row*numCols+column
    vertConstr = indexToStart[index]["V"]
    
    # get the prefix
    prefix = get_prefix(board,vertStart[vertConstr])
    # get the valid next_letters from length prefix tree
    next_letters = lengthPrefixTree[len(vertStart)][prefix]
    # for l in next_letter:
    index = row*numCols+column
    for l1 in next_letters:
        # if next square has a letter on it:
        if board[index].isalpha() and l1!=board[index]:
            return None
            # if l != next square letter:
                # return None
        # if next_square is -:
        if board[index] == "-":
            # place the letter
            nb = board.copy()
            nb[index] = l1
            # get the prefix from that cell for horizontal the cell belongs to
            horzConstr = indexToStart[index]["H"]
            horzpref = get_prefix(board,horzConstr)
            # if there is no prefix:
            if horzpref == "":
                # get the vertical block the start cell is in
                startVertCell = indexToStart[horzConstr]["V"]
                if startVertCell == horzConstr:
                    seedwords = lengthMapping[len(vertStart[startVertCell])]
                    for startletter in seedwords:
                        for word in seedwords[startletter]:
                            if test_placement(nb,word,horzStart[horzConstr]):
                                result = build_vertical(nb,row,column+1,row,column)
                                if result is not None:
                                    return result
                else:
                    possHorzpref = lengthPrefixTree[len(horzStart[horzConstr])] # refers to a dictionary
                    end = horzStart[horzConstr].index(index) 
                    for pref in possHorzpref:
                        if len(pref) == end+1 and l1 in possHorzpref[pref]:
                            test_placement(board,pref,horzStart[horzConstr])
                            result = build_vertical(nb,row,column+1,row,column,indexToStart)


                # if square is corner:
                    # build_subgrid from the corner
                    # tried seed words = set()
                    # find seed word which satisfies current conditions, return seed word
                    # if there is not valid seed word:
                        # return None
                    # else:
                        # add seedword to used
                        # continue building the grid by recursion on board
                # for l2 in valid prefixes for horz cell:
                    # place that prefix
                     # if l1 does not produce a valid prefix:
                        # continue
                    # recur by calling build_vertical on board,row,col+1
                   
            # else:
                # check if horz+l1 is a valid prefix
                # if not - return None
            else:
                if horzpref+l1 in lengthPrefixTree[len(horzStart[horzConstr])]:
                    result = build_vertical(board,row,column+1,row,column)
                    if result is not None:
                        return result
            
def test_placement(board,stem,locations): # and additional arguments
    """
    Places stems horizontally in a row
    """
    for i in range(len(stem)):
        if board[locations[i]] == "-":
            pass
        elif board[locations[i]] == stem[i]:
            pass
        else:
            return False
    for i in range(len(stem)):
        board[locations[i]] = stem[i]
    return True
def get_prefix(board,indices):
    pref = ""
    for b in indices:
        if board[b] != "-":
            pref += board[b]
    return pref 
words = list(all_words)
solved = add_letters(filled,words)
printBoard(solved,5,5)
# Vivian Feng, 3, 2023