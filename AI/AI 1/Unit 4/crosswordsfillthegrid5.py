import sys; args = sys.argv[1:]
myLines = open(args[0],'r').read().splitlines()
import random, time


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
    printBoard(board,numRows,numCols)
    filled_board = fill_gaps(board,numRows,numCols,indices)
    printBoard(filled_board,numRows,numCols)
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
    
    printBoard(filled_board,numRows,numCols)
    printBoard(filled_board,numRows,numCols)
    print(filled_board.count("#"))
    #filled_board = ['#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '-', '-', '-', '#', '#', '#', '-', '-', '-', '#', '#', '-', '-', '-', '#', '#', '-', '-', '-', '#', '#', '#', '-', '-', '-', '#', '#', '#', '-', '-', '-', '#', '#', '#', '-', '-', '-', '-', '-', '-', '-', '-', '#', '#', '#', '-', '-', '-', '#', '#', '#', '-', '-', '-', '#', '#', '#', '-', '-', '-', '#', '#', '-', '-', '-', '#', '#', '-', '-', '-', '#', '#', '#', '-', '-', '-', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#']
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
    # print(board)
    # print("placed",placed)
    # print("Allowed",allowed)
    # input()
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
        # listSpace = sorted(list(spaces))
        # space = listSpace[0]
        spaces.remove(space)
        # print(spaces)
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
            bestSpace.append(s)
        elif count > mostOpen:
            bestSpace = [s]
            mostOpen = count
    # return random.choice(bestSpace)
    return bestSpace[0]
                
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
numRows,numCols = int(args[1].split("x")[0]),int(args[1].split("x")[1])
print(numRows,numCols)
blockedSquares = int(args[2])
# dictionaryfile = args[3]
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
print(horizontal,"Horizontal")
print(vertical,"vertical")


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
printBoard(crossGrid,numRows,numCols)
filled = placeBlocks(crossGrid,0,numRows,numCols,blockedSquares)
if filled[len(filled)//2] == ".":
    filled[len(filled)//2] = "-"
printBoard(filled,numRows,numCols)
# backtrack(['#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '-', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '-', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '#', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '-', '-', '-', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '-', '-', '-', '-', '#', '#', '#', '-', '-', '-', '-', '-', '-', '#', '#', '#', '-', '-', '-', '-', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '-', '-', '-', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '#', '-', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '-', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '-', '-', '-', '-', '#', '#', '#', '#', '#', '#', '#', '-', '-', '-', '#', '#', '-', '-', '-', '#', '#', '#', '#', '#'],184,16,16)


"""PART 2 starts here"""
def getSequence(board,index,mappingToIndex):
    value = ""
    indices = mappingToIndex[index]
    for ind in indices:
        value += board[ind]
    return value


def checkMatch(skeleton,word):
    if len(skeleton)!=len(word):
        return False

    for i in range(len(skeleton)):
        if skeleton[i].isalpha() and skeleton[i]!=word[i]:
            return False
    return True

# with open(dictionaryfile) as f:
letterFreqTable = dict()
all_words = []
for line in myLines:
    line = line.strip().upper()
    if line.isalpha():
        all_words.append(line)
    for l in line:
        if l in letterFreqTable:
            letterFreqTable[l] += 1
        else:
            letterFreqTable[l] = 1
print(letterFreqTable)

# get the corners
horzStarts = []
vertStarts = []
for i in range(len(filled)):
    row = i//numCols
    col = i%numCols
    if filled[i] != "#":
        if row-1 < 0 or filled[(row-1)*numCols+col] == "#":
            vertStarts.append(i)
        if col -1 < 0 or filled[row*numCols+col-1] == "#":
            horzStarts.append(i)
# build start to indicies mappings, indextostart
indexTohorzStart = dict()
horztoIndices = dict() # dict(index:list(indices))
for h in horzStarts:
    row = h//numCols
    col = h %numCols
    indices = list()
    c = col
    while c < numCols and filled[row*numCols+c]!="#":
        indexTohorzStart[row*numCols+c] = h
        indices.append(row*numCols+c)
        c += 1
    horztoIndices[h] = indices

indexTovertStart = dict()
vertToIndices = dict() # dict(index:list(indices))
for v in vertStarts:
    row = v//numCols
    col = v%numCols
    r = row
    indices = []
    while r < numRows and filled[r*numCols+col]!="#":
        indexTovertStart[r*numCols+col] = v
        indices.append(r*numCols+col)
        r += 1
    vertToIndices[v] = indices
# add the existing words
horzWords = dict() # maps horizontal spaces to words corresponding to that space
for horz in horzStarts:
    valid = set()
    sequence = getSequence(filled,horz,horztoIndices)
    for word in all_words:
        if checkMatch(sequence, word):
            valid.add(word)
    horzWords[horz] = valid

vertWords = dict()
for vert in vertStarts:
    valid = set()
    sequence = getSequence(filled,vert,vertToIndices)
    for word in all_words:
        if checkMatch(sequence,word):
            valid.add(word)
    vertWords[vert] = valid
# for each constraint set, add the words

print(horztoIndices)
print(vertToIndices)

# print(vertWords)
# print("Horizontal words",horzWords)
def backtrackFill(board,verttoIndex,horzToIndex,indexToVert,indexToHorz,horzToWords,vertToWords): # and other args

    if "-" not in board:
        return board
    # printBoard(board,numRows,numCols)
    # print("Possible horizontal: ",horzToWords)
    # print("Possible Vertical: ", vertToWords)
    # print("Used",used)
    # input()
    
    all_possible_letters = poss_next(board,indToVert = indexToVert,indexToHorz=indexToHorz,horzToWords=horzToWords,vertToWords=vertToWords)
    if all_possible_letters is not None:
        # print(possible_letters)
    
        next = get_next(all_possible_letters)
        possible_letters = all_possible_letters[next]
        while len(possible_letters) > 0:
            letter = get_next_letter(possible_letters)
            possible_letters.remove(letter)
            newboard = board.copy()
            newboard[next] = letter
            newhor2words = {key:horzToWords[key].copy() for key in horzToWords}
            newvert2words = {key:vertToWords[key].copy() for key in vertToWords}
            newused = used_pieces(horzToWords,vertToWords)
            # flag keeps track if successfully updated
            checked = update(newboard,newhor2words,newvert2words,horzToWords,vertToWords,indexToHorz,indexToVert,horzToIndex,verttoIndex,newused)
            # place letter and structures
            if checked is not None:
                result = backtrackFill(checked,verttoIndex,horzToIndex,indexToVert,indexToHorz,newhor2words,newvert2words)
                if result is not None:
                    return result
def get_next_letter(possible_letters):
    maxCount = 0
    letter = ""
    for l in possible_letters:
        if letterFreqTable[l] > maxCount:
            maxCount = letterFreqTable[l]
            letter = l
    return letter
def update(board,newhorztoWords,newVertToWords,horzToWords,vert2Words,indexToHorz,indexToVert,horzToIndex,vertToIndex,used):
    """
    Updates the data structures to exclude words which do not fit the new pattern

    """
    # obtain relative position
    # vertStart = indexToVert[index]
    # horzstart = indexToHorz[index]
    # relIndv = (index-vertStart)//numCols
    # relIndh = (index-horzstart)
    # update the horizontal sets to fit new configuration
    for horzstart in horzToWords: 
        sequenceH = getSequence(board,horzstart,horzToIndex)
        for word in horzToWords[horzstart]:
            if len(horzToWords[horzstart]) > 1:
                if not checkMatch(sequenceH,word) or word in used:
                    newhorztoWords[horzstart].remove(word)
                if len(newhorztoWords[horzstart]) == 0:
                    return None

    for vertStart in vert2Words:
        sequenceV = getSequence(board,vertStart,vertToIndex)
        for word in vert2Words[vertStart]:
            if len(vert2Words[vertStart]) > 1:
                if not checkMatch(sequenceV,word) or word in used:
                    newVertToWords[vertStart].remove(word)
            if len(newVertToWords[vertStart]) == 0:
                return None
    return board

def used_pieces(horz_words,vert_words):
    used = set()
    for key in horz_words:
        if len(horz_words[key]) == 1:
            used.add(list(horz_words[key])[0])
    for key in vert_words:
        if len(vert_words[key]) == 1:
            used.add(list(vert_words[key])[0])
    return used
        
def get_next(next_possible_letters):
    """
    Returns the next open index in the space the with fewest open spaces
    """
    minChoices = float('inf')
    choices = []
    for i in next_possible_letters:
        if len(next_possible_letters[i]) < minChoices:
            minChoices = len(next_possible_letters[i])
            choices = [i]
        elif len(next_possible_letters) == minChoices:
            choices.append(i)
    return random.choice(choices)
    



            
            
def poss_next(board,indToVert,indexToHorz,horzToWords,vertToWords):
    """
    Returns a dictionary of possible letters for each word
    """
    # obtain the corresponding vertical and horizontal starts
    # obtain the index relative to the each horizontal and vertical start
    # to get possible letters:
    # obtain the letters found in each horz and vert set
    # iterating through set, append the letters common to both sets to a list and return them
    choices = dict()
    for index in range(len(board)):
        if board[index] == "-":
            vertStart = indToVert[index]
            horzStart = indexToHorz[index]

            relVertIndex = (index-vertStart)//numCols
            relHorzIndex = (index-horzStart)

            possHorzChars = set()
            for word in horzToWords[horzStart]:
                possHorzChars.add(word[relHorzIndex])

            possVertChars = set()

            for word in vertToWords[vertStart]:
                possVertChars.add(word[relVertIndex])

            shared = set()
            for ch in possHorzChars:
                if ch in possVertChars:
                    shared.add(ch)
            choices[index] = shared
            if len(choices[index]) == 0:
                return None
    return choices
            
                 

        

used = set()
start = time.perf_counter()
result = backtrackFill(filled,vertToIndices,horztoIndices,indexTovertStart,indexTohorzStart,horzWords,vertWords)
end = time.perf_counter()
print("Time",(end-start))
printBoard(result,numRows,numCols)
# Vivian Feng, 3, 2023