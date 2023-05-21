import sys
from heapq import heappush,heappop,heapify
# You are given code to read in a puzzle from the command line.  The puzzle should be a single input argument IN QUOTES.
# A puzzle looks like this: "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
# The code below breaks it down:
puzzle = sys.argv[1].split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]

rect_set = set(rectangles)
# puzzle_height is the height (number of rows) of the puzzle
# puzzle_width is the width (number of columns) of the puzzle
# rectangles is a list of tuples of rectangle dimensions



# INSTRUCTIONS:
#
# First check to see if the sum of the areas of the little rectangles equals the big area.
# If not, output precisely this - "Containing rectangle incorrectly sized."
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
def solve(grid_height,grid_width,rectangles):
    sides = []
    heappush(sides,(0,0,grid_width))
    heappush(sides,(0,grid_height,grid_width))
    backtrack()
def backtrack(sides,rectangles,grid_height,grid_width,solution):
    if len(rectangles) == 0:
        return solution
    # return solution if goal_test is successful
    # next = get_next_unassigned_var
    # for val in get_sorted values:
    for v in rectangles:
        new_sides = sides.copy()
        mod_rect = rectangles.copy()
        mod_rect.remove(v)
        added_rect = add_rect(new_sides,grid_height,grid_width)
        # assign val to var
        if added_rect is not None:
            new_sol = solution.copy()
            new_sol.append(added_rect)
            result = backtrack(new_sides,mod_rect,grid_height,grid_width,new_sol)
        # result = backtrack() with val
        # if result is not None:
            # return result
    # return None
    

def add_rect(sides,rectangle,block_height,block_width):
    # always place in the upper left corner
    # if exceeds edge: return false
    # if exceeds boundary: return false
    # must merge edges in the same
    loc = heappop(sides)
    height,width = rectangle
    
    y,x1,x2 = loc
    edge1 = y,x1+width,x2
    edge2 = y+height,x1,x2+width
    if isValid(sides,edge1,edge2,block_height,block_width):
        if edge2[0] == sides[0][0]:
            toMerge = heappop(sides)
            merged = (edge2[0],toMerge[1],edge2[2])
            heappush(sides,merged)
            heappush(sides,edge1)
        else:
            heappush(sides,edge1)
            heappush(sides,edge2)
        return y,x1,height,width
    return None
def isValid(sides,edge1,edge2,height,width):
    next = sides[0]
    y,x1,x2 = edge1
    ye2,x1e2,x2e2 = edge2
    if x1 > width:
        return False
    if y > height:
        return False
    if x1 > x2:
        return False

    if ye2 > next[0]:
        return False
    if x2e2 > width:
        return False

    return True


    

# If the puzzle is solved, output ONE line for EACH rectangle in the following format:
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