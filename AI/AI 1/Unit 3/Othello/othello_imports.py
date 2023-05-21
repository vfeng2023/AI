"""
Functions used to run othello
"""

def possible_moves(board, token):
    """
     Returns a list of all possible squares that can be played into by token
    """
    other = "x"
    if token == "x":
        other = "o"
    mod_board = add_border(board,8)
    # print_board(mod_board,10)
    valid_squares = []
    for square in range(len(mod_board)):
        if mod_board[square] == ".":
            directions = [-11,-10,-9,-1,1,9,10,11]
            
            for d in directions:
                space = square + d
                while 0 <= space < len(mod_board):
                    if mod_board[space] == other:
                        space += d
                    else:
                        break
                if mod_board[space] == token and space!=square+d:
                    row = square//10
                    col = square%10

                    board_row = (row-1)
                    board_col = col - 1
                    board_space = board_row*8+board_col
                    valid_squares.append(board_space)
                    break
    return valid_squares
                

def make_move(board,token,index):
    other = "x"
    if token == "x":
        other = "o"
    bordered = list(add_border(board,8))
    bordered_index = (index//8+1)*10 + (index%8+1)
    bordered[bordered_index] = token
    direction = [-11,-10,-9,-1,1,9,10,11]
    for d in direction:
        space = bordered_index + d
        changed = 0
        while 0 <=space < len(bordered):
            if bordered[space] == other:
                bordered[space] = token
                changed += 1
                space += d
            else:
                break
        if bordered[space] != token:
            for i in range(changed):
                space -= d
                bordered[space] = other
    stripped = strip_border("".join(bordered))
    return stripped

def add_border(board,size):
    """
    adds question mark border
    size is the size of the board
    """
    final = "??????????"
    for i in range(0,size):
        final += ("?"+board[i*size:(i+1)*size]+"?")
    final += "??????????"

    return final
def strip_border(board):
    toRet = ""
    for ch in board:
        if ch!="?":
            toRet += ch
    return toRet

def print_board(board,size):
    for i in range(size):
        for j in range(size):
            print(board[i*size+j],end= "")
        print()
#print(possible_moves("xxoo.xox.....oox......oxo..ooxooo..oox.ox.xxx..oxoox...o.....xox","x"))
# print(s:=add_border("...........................ox......xo...........................",8))
# print(len(s))