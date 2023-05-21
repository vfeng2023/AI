import sys;args = sys.argv[1:]
"""
Intermediate to Advanced Intermediate RegEx Lab with back references, look aheads, and negative lookaheads.  
Submission is a command line script which receives an integer in [50,59] and returns the corresponding regex, delimited between forward slashes, with any options trailing (eg. /hi mom/i)

Word problems are case insensitive by default, string problems are not.  Q50-52 do not allow for lookarounds.

Q50: Match all words where some letter appears twice in the same word.
Q51: Match all words where some letter appears four times in the same word.
Q52: Match all non-empty binary strings with the same number of 01 substrings as 10 substrings.
Q53: Match all six letter words containing the substring cat.
Q54: Match all 5 to 9 letter words containing both the substrings bri and ing.
Q55: Match all six letter words not containing the substring cat.
Q56: Match all words with no repeated characters.
Q57: Match all binary strings not containing the forbidden substring 10011.
Q58: Match all words having two different adjacent vowels.
Q59: Match all binary strings containing neither 101 nor 111 as substrings.
"""
idx = int(args[0])-50
# myRegexLst = [
# r"/\b\w*(\w)\w*\1\w*\b/i", # 50
# r"/\b\w*(\w)(\w*\1){3}\w*\b/i", #51
# r"/^([01])(\1*[01]*\1+)?$/",#52
# r"/\b(?=\w*cat)\w{6}\b/i", #53
# r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i", #54
# r"/\b(?!\w*cat)\w{6}\b/i",#55
# r"/\b((\w)(?!\w*\2))+\b/i", #56
# r"/^(?!.*10011)[01]*$/", #57
# r"/\b\w*([aeiou])(?!\1)[aeiou]\w*\b/i", #58
# r"/^(?!.*101)(?!.*111)[10]*$/" #59
# ]
# myRegexLst = [
# r"/\b(\w)*\w*\1\w*\b/i", # 50
# r"/\b\w*(\w)(\w*\1){3}\w*\b/i", #51
# r"/^([01])(\1*[01]*\1+)?$/",#52
# r"/\b(?=\w*cat)\w{6}\b/i", #53
# r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i", #54
# r"/\b(?!\w*cat)\w{6}\b/i",#55
# r"/\b((\w)(?!\w*\2))+\b/i", #56
# r"/^(?!.*10011)[01]*$/", #57
# r"/\b\w*([aeiou])(?!\1)[aeiou]\w*\b/i", #58
# r"/^(?!.*101)(?!.*111)[10]*$/" #59
# ]
# 227
myRegexLst = [
r"/\b(\w)*\w*\1\w*\b/i", # 50
r"/\b(\w)*(\w*\1){3}\w*\b/i", #51
r"/^([01])(\1*[01]*\1+)?$/",#52
r"/\b(?=\w*cat)\w{6}\b/i", #53
r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i", #54
r"/\b(?!\w*cat)\w{6}\b/i",#55
r"/\b((\w)(?!\w*\2))+\b/i", #56
r"/^(?!.*10011)[01]*$/", #57
r"/\b\w*([aeiou])(?!\1)[aeiou]\w*\b/i", #58
r"/^(?!.*101)(?!.*111)[10]*$/" #59
]


if idx < len(myRegexLst):
    print(myRegexLst[idx])
# Vivian Feng, 3, 2023
