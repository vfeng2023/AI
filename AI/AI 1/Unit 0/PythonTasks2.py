import sys

s = sys.argv[1]

"""
1) …the character at position 2. (Which I don’t need to remind you is not the second character.)
2) …the fifth character. (Which I don’t need to remind you is not the character at position 5.)
3) …the number of characters in the string.
4) …the first character.
5) …the last character.
6) …the penultimate character.
7) …the five character long substring starting at position 3.
8) …a substring consisting of the last five characters of the string.
9) …a substring starting at the third character and continuing to the end of the string.
10) …a string containing every other character from the input string.
11) …a string consisting of every third character from the input string, starting from its second character.
12) …the input string reversed. (One line!)
13) …the position of the first space in the input string.
14) …the string shifted to the right by one (ie, the original string with the last character removed).
15) …the string shifted to the left by one (ie, the original string with the first character removed).
16) …the string all in lower case.
17) …a list of all the space delimited substrings of the input string. Examples: "234" ➔ ["234"] "12 35" ➔ ["12", "35"] "The quick fox" ➔ ["The", "quick", "fox”]
18) …the number of space delimited words there are in your input string.
19) …a list of all characters, including duplicates, in the string (eg, "foo" ➔ ["f", "o", "o"]).
20) …a new string consisting of the characters of the input string rearranged in ascending ascii order (eg, "quick" ➔ "cikqu").
21) …a new string consisting of the substring of your input string starting at the beginning and going up to, but not including, the first space. If there is no space at all, it should give the entire input.
22) …whether or not the input string is a palindrome. (For this question, you can assume the input string is only lower case letters with no grammatical symbols.)
"""
def isPalindrome(s):
    i=0
    j=len(s) -1 
    while i <=j:
        if s[i]!=s[j]:
            return False
        i+= 1
        j-=1
    return True
print("#1: ",s[2])
print("#2: ",s[4])
print("#3: ",len(s))
print("#4: ",s[0])
print("#5: ",s[-1])
print("#6: ",s[-2])
print("#7: ",s[3:8])
print("#8: ",s[-5:])
print("#9: ",s[3:])
print("#10: ",s[::2])
print("#11: ",s[2::3])
print("#12: ",s[::-1])
print("#13: ",s.find(" "))
print("#14: ",s[:-1])
print("#15: ",s[1:])
print("#16: ",s.lower())
print("#17: ",s.split())
print("#18: ",len(s.split()))
print("#19: ",list(s))
print("#20: ","".join(sorted(list(s)))) 
print("#21: ",s) if s.find(" ") == -1 else print("#21: ",s[:s.find(" ")])
print("#22: ",isPalindrome(s))


