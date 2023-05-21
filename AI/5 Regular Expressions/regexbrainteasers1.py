import sys;args = sys.argv[1:]
"""
Definitions:
Binary string: a string, possibly empty, that consists exclusively of '0' and '1' characters.
Binary/decimal integer: a non-empty string consisting only of the digits appropriate to the relevant base, such that there are no leading '0' characters, except that the number 0 is represented by '0'.

Each entry in the list should be in the form of:
r"/pattern/options"
The r stands for raw (but could be thought of as standing for regular expression) and allows one to place backslashes in a string without having to escape them.  
It is not, strictly speaking, necessary, but is highly recommended.  options, is zero or more of any of the letters i (for case insensitive), s (for dot all), and m (multiline).

30: Determine whether a string is either 0, 100, or 101.
31: Determine whether a given string is a binary string (ie. composed only of  0 and 1 characters).
32: Given a binary integer string, what regular expression determines whether it is even?
33: What is a regular expression to determine (ie. match) those words in a text that have at least two vowels?
34: Given a string, determine whether it is a non-negative, even binary integer string.
35: Determine whether a given string is a binary string containing 110 as a substring.
36: Match on all strings of length at least two, but at most four.
37: Validate a social security number entered into a field (ie. recognize ddd-dd-dddd where the d represents digits and where the dash indicates an arbitrary number of spaces with at most one dash).  
For example, 542786363,   542  786363, and 542 – 78-6263 are all considered valid.
38: Determine a regular expression to help you find the first word of each line of text with a  d  in it: Match through the end of the first word with a d on each line that has a d.
39: Determine whether a string is a binary string that has the same number of 01 substrings as 10 substrings.
"""
idx = int(args[0])-30


myRegexLst = [
r"/^0$|^10[01]$/",  # 30
r"/^[01]*$/",  # 31
r"/[01]*0$/",  # 32
r"/\w*[aeiou]\w*[aeiou]\w*/i",  # 33
r"/^1[01]*0$|^0$/",  # 34
r"/^[10]*?110[10]*$/",  # 35
r"/^.{2,4}$/s",  # 36,
r"/^\d{3}\s*-?\s*\d\d\s*-?\s*\d{4}\s*$/",  # 37
r"/^.*?d\w*\b/im",  # 38
r"/^1+0[01]*1+$|^0+1[01]*0+$|^0*$|^1*$/"# 39
]


if idx < len(myRegexLst):
    print(myRegexLst[idx])
# Vivian Feng, 4, 2023