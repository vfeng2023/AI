# def get_children(state_dict):
#     board = [[False,False,False,False,False,False] for i in range(6)]
#     # generate unoccupied spaces
#     for k in state_dict:
#         row,col,length,dir = state_dict[k]
#         if dir == "x":
#             for c in range(col,col + length):
#                 board[row][c] = True
#         else:
#             for r in range(row,row+length):
#                 board[r][col] = True

#     # move each car on board
#     children = list()
#     for k in state_dict:
#         # forward
#         # reverse
#         row,col,length,dir = state_dict[k]
#         if dir == "x":
#             for c in range(col+length,6):
#                 if board[row][c]:
#                     break
#                 else:
#                     new = (row,c,length,dir)
#                     child = {k:state_dict[k].copy() for k in state_dict}
#                     state_dict[k] = new

#             for c in range(0,col):
                

#         else:
#             for r in range(row,row+length):
#                 board[r][col] = True
    # consider the ones blocking it in front and rear

# use strings to represent board states
# uses this article for reference: https://www.michaelfogleman.com/rush/#EnumeratingStates

SIZE = 6
size_mask = 2**(SIZE*SIZE) - 1
def get_children(board,row_masks,vert_masks):
    mask = 2**(SIZE*SIZE)-1
    all,horz,vert = board
    #horizontal shifts
    children = list()
    for n in range(SIZE):
        new = move_left(board,row_masks,n)
        if isValid(new):
            children.append(new)

        # new_vert = vert >> 6
        # child2 = new_vert & mask
        # if isValid(child2):
        #     chilren.append(child2)

        # horz2 = horz << 1
        # child3 = horz2 & mask
        # if isValid(child3):
        #     children.append(board)

        # vert2 = vert << 6
        # child4 = vert2 & mask
        # if isValid(child4):
        #     children.append(appropriate board)

    return children

def move_left(board,row_mask,row):
    all,horz,vert = board
    new_horz = horz >> 1
    printboard(board)
    child = new_horz & size_mask
    only_row = child & row_mask[row]
    no_row = all & ~row_mask[row]
    new_b = only_row|no_row
    new_vert = new_b^child
    return new_b,child,new_vert

# board is a tuple with all, horizontal, and vertical states
def isValid(board):
    all,horz,vert = board
    return horz & vert == 0 # otherwise there is a collision

def printboard(board):
    all,horz,vert = board
    for b in board:
        binrep = f"{b & size_mask:036b}"
        print(binrep)
        for i in range(SIZE):
            for j in range(SIZE):
                print(binrep[len(binrep)-1-(i*SIZE + j)], end=" ")
            print()
        print()

#generate masks
row_masks = {}
row = 2**SIZE-1
for i in range(SIZE):
    row_masks[i] = (row * (2**i)) & size_mask

vert_masks = {}
vert = ["0" for i in range(SIZE*SIZE)]
for i in range(SIZE):
    for j in range(len(vert)-1,-1,-1):
        if j%SIZE == i and j > 0 and j < len(vert):
            print(j)
            vert[j] = "1"
    vert_masks[i] = int("".join(vert),2) & size_mask
    vert = list("0"*(SIZE*SIZE))

printboard((3, 3,0))
print("Children")
for b in get_children((3,3,0),row_masks,vert_masks):
    printboard(b)
    print("Next child")