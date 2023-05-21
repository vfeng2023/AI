import sys

# You are given code to read in a puzzle from the command line.  The puzzle should be a single input argument IN QUOTES.
# A puzzle looks like this: "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
# The code below breaks it down:
puzzle = "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4".split()
# puzzle = "18 9 3x11 5x7 4x8 6x10 1x2".split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
# puzzle_height is the height (number of rows) of the puzzle
# puzzle_width is the width (number of columns) of the puzzle
# rectangles is a list of tuples of rectangle dimensions


# INSTRUCTIONS:
#
# First check to see if the sum of the areas of the little rectangles equals the big area.
# If not, output precisely this - "Containing rectangle incorrectly sized."
#
def check_sum(puzzle):
    totalArea = puzzle_height*puzzle_width
    actualSum = 0
    for rect in rectangles:
        actualSum += (rect[0]*rect[1])
        if actualSum > totalArea:
            print("Containing rectangle incorrectly sized.")
            return False
    return True
# Then try to solve the puzzle.
# If the puzzle is unsolvable, output precisely this - "No solution."
#
# If the puzzle is solved, output ONE line for EACH rectangle in the following format:
# rectangles should be a 
def backtrack(rectangles,coordinates,puzzle_height,puzzle_width,bounds):
    if len(rectangles) == 0:
        return coordinates
    next = next_space(coordinates,bounds,puzzle_height,puzzle_width)
    print(next)
    print(bounds)
    for val in rectangles:
        print(val)
        new_c = coordinates.copy()
        new_c2 = coordinates.copy()
        new_rectangles = remove(val,rectangles)
        new_rectangles2 = new_rectangles.copy()
        y,x = next
        new_bounds = bounds.copy()
        nbouds2 = bounds.copy()
        rect = (y,x,val[0],val[1])
        if valid_placement(rect,coordinates,puzzle_height,puzzle_width):
            new_c.append(rect)
            new_bounds = set_boundary(coordinates,new_bounds,rect)
            print("-------------------------------")
            result = backtrack(new_rectangles,new_c,puzzle_height,puzzle_width,new_bounds)
            if result is not None:
                return result
        flipped_rect = (y,x,val[1],val[0])
        if valid_placement(flipped_rect,coordinates,puzzle_height,puzzle_width):
            new_c2.append(flipped_rect)
            nbouds1 =set_boundary(coordinates,nbouds2,flipped_rect)
            result = backtrack(new_rectangles2,new_c2,puzzle_height,puzzle_width,nbouds2)
            if result is not None:
                return result
            # try calling backtrack on rectangle but flipped orientation.
    return None


# returns a copy of the array without the item to by removed(only removes once)
def remove(value,array):
    no_itemArr = []
    removed = False
    for item in array:
        if not removed and item == value:
            removed = True
        else:
            no_itemArr.append(item)
    return no_itemArr
def next_space(coordinates,bounds,puzzle_height,puzzle_width):
    # place in the upper left most corner
    if len(bounds) == 0:
        return (0,0) # row column
    miny = puzzle_height
    minx = puzzle_width
    for c in bounds:
        y,x = c
        test_rect = (y,x,1,1)
        if valid_placement(test_rect,coordinates,puzzle_height,puzzle_width) and (y<=miny):
            if miny ==y:
                minx = min(x,minx)
            else:
                miny = y
                minx = x
        # if is_valid(y2,x2,coordinates,puzzle_height,puzzle_width) and y2 <=miny and (y2,x2) in bounds:
        #     if miny == y2:
        #         if x2 < minx:
        #             minx = x2
        #     else:
        #         miny = y2
        #         minx = x2
        
        # if is_valid(y3,x3,coordinates,puzzle_height,puzzle_width) and y3 <=miny and (y3,x3) in bounds:
        #     if miny == y3:
        #         if x3 < minx:
        #             minx = x3
        #     else:
        #         miny = y3
        #         minx = x3
        # if is_valid(y4,x4,coordinates,puzzle_height,puzzle_width) and y4 <=miny and (y4,x4) in bounds:
        #     if miny == y4:
        #         if x4 < minx:
        #             minx = x4
        #     else:
        #         miny = y4
        #         minx = x4
    return miny,minx

def is_valid(y,x,coordinates,puzzle_height,puzzle_width):
    if y > puzzle_height or x > puzzle_width:
        return False
    for c in coordinates:
        cy,cx,height,width = c
        if cy < y < cy+height and cx < x < cx+width:
            return False
    return True

def valid_placement(rect,coordinates,puzzle_height,puzzle_width):
    y1,x1,height,width = rect
    y2,x2 = y1,x1+width
    y3,x3 = y1+height,x1+width
    y4,x4 = y1+height,x1
    # print((y1,x1))
    # print((y2,x2))
    # print((y3,x3))
    # print((y4,x4))

    on_interior = is_valid(y1,x1,coordinates,puzzle_height,puzzle_width) and is_valid(y2,x2,coordinates,puzzle_height,puzzle_width) and is_valid(y3,x3,coordinates,puzzle_height,puzzle_width) and\
        is_valid(y3,x3,coordinates,puzzle_height,puzzle_width)
    return on_interior

def set_boundary(coordinates,bounds,toAdd):
    print("in bounds")
    print(toAdd)
    print(bounds)
    y1,x1,height,width = toAdd
    c1 = y1,x1
    c2 = y1,x1+width
    c3 = y1+height,x1+width
    c4 = y1+height,x1
    for coord in c1,c2,c3,c4:
        print(coord)
        if coord in bounds:
            bounds.remove(coord)
        else:
            bounds.add(coord)
    print("end bounds")
    return bounds
# row column height width
# where "row" and "column" refer to the rectangle's top left corner.
#
# For example, a line that says:
# 3 4 2 1
# would be a rectangle whose top left corner is in row 3, column 4, with a height of 2 and a width of 1.
# Note that this is NOT the same as 3 4 1 2 would be.  The orientation of the rectangle is important.
#
# Your code should output exactly one line (one print statement) per rectangle and NOTHING ELSE.
# If you don't follow this convention exactly, my grader will fail.

if check_sum(puzzle):
    bounds = {(0,puzzle_width),(0,0),(puzzle_height,0),(puzzle_height,puzzle_width)}
    solution = backtrack(rectangles,[],puzzle_height,puzzle_width,bounds)
    if solution is None:
        print("No solution.")
    else:
        for s in solution:
            print(" ".join([str(i) for i in s]))

# test_coords = []
# bounds = {(0,0),(0,3),(2,0),(2,3)}
# test_coords.append((0,0,1,2))
# bounds = set_boundary(test_coords,bounds,(0,0,1,2))
# test_coords.append((0,2,2,1))
# bounds = set_boundary(test_coords,bounds,(0,2,2,1))
# print(bounds)
# for b in bounds:
#     test_rect = (b[0],b[1],1,1)
#     print(valid_placement(test_rect,test_coords,2,3))
# print(valid_placement((1,0,1,1),test_coords,2,3))
# print("Next space: ",next_space(test_coords,bounds,2,3))

# print(is_valid(1,0,test_coords,2,3))