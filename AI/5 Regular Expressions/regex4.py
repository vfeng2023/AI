import sys;args = sys.argv[1:]
"""
Word problems are case insensitive by default, string problems are not.  Target count for length of all 10 regular expressions is 253.  However, it may be that some of the solution regex's can be improved upon.

Q60: Match all binary strings that do not contain the forbidden substring 010.  (14)
Q61: Match all binary strings containing neither 101 nor 010 as substrings.  (20)
Q62: Match on all non-empty binary strings with the same number of 01 substrings as 10 substrings.  (14)
Q63: Match all words whose final letter is not to be found elsewhere in the word.  (21)  
Q64: Match all words that have at least two pairs of doubled letters (two pairs of distinct letters or four of the same letter are both OK).  (43)
Q65: Match all words that have no duplicate letter, except for one, which occurs at least 3 times.  (42)
Q66: Match all words where each of the five vowels occurs exactly once.  (39)
Q67: Match all binary strings that have an odd number of 0s and an even number of 1s.  (22)
Q68: Match all binary integer strings that are divisible by 3.  (19)
Q69: Match all binary integer strings that are not divisible by 3.  (19)
"""

idx = int(args[0])-60
myRegexLst = [
r"/^(?!.*010)[01]*$/", #60
r"/^(?!.*101)(?!.*010)[01]+$|^$/", #61
r"/^([01])[01]*\1$|^[01]$/", #62
r"/\b(?=(\w)*\b)(\w(?!\1))*\w\1\b/i" # 63
]


if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Vivian Feng, 3, 2023
