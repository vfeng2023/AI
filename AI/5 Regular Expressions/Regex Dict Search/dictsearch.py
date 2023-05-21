import sys
import re
wordfile = sys.argv[1]


with open(wordfile) as f:
    wordlist = [line.strip().lower() for line in f.readlines()]


# 1
exp1=r"^(?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u)\w*$"
regex1 = re.compile(exp1,re.I)
all_matches = []
for word in wordlist:
    for result in regex1.finditer(word):
        all_matches.append(word)

print("#1", "/",exp1,"/i")
minlen = float('inf')
for match in all_matches:
    if len(match) < minlen:
        minlen = len(match)
lst = []
for word in all_matches:
    if len(word) == minlen:
        lst.append(word)
lst.sort()
print(len(lst), "total matches")
for i in range(5):
    if i < len(lst):
        print(lst[i])
print()

#2  
exp2 = r"^[^aeiou]*([aeiou][^aeiou]*){5}$"
regex2 = re.compile(exp2,re.I)
all_matches = []
for word in wordlist:
    for result in regex2.finditer(word):
        all_matches.append(word)

print("#2", "/",exp2,"/i")
maxlen = -float('inf')
for match in all_matches:
    if len(match) > maxlen:
        maxlen = len(match)
lst = []
for word in all_matches:
    if len(word) == maxlen:
        lst.append(word)
lst.sort()
print(len(lst), "total matches")
for i in range(5):
    if i < len(lst):
        print(lst[i])
print()
# 3: Match all words of maximum length where the first letter reappears as the last letter but does not appear
# anywhere else in the word.
exp3 = r"^([a-z])(\w(?!\1))*\w?\1$"
regex3 = re.compile(exp3,re.I)
all_matches = []
for word in wordlist:
    for result in regex3.finditer(word):
        all_matches.append(word)

print("#3", "/",exp3,"/i")
maxlen = -float('inf')
for match in all_matches:
    if len(match) > maxlen:
        maxlen = len(match)
lst = []
for word in all_matches:
    if len(word) == maxlen:
        lst.append(word)
lst.sort()
print(len(lst), "total matches")
for i in range(5):
    if i < len(lst):
        print(lst[i])
print()
# 4: Match all words where the first three letters, reversed, are the last three letters. Overlapping is ok; for instance,
# "ada" and "abba" should both count.

exp4 = r"^(?=(\w)(\w)(\w))(?=\w*\3\2\1$)\w*$"
regex4 = re.compile(exp4,re.I)
matches = []
for word in wordlist:
    if re.fullmatch(regex4,word):
        matches.append(word)
print("#4: ","/",exp4,"/i")
print(len(matches), "total matches")
for i in range(5):
    if i < len(matches):
        print(matches[i])
print()
# 5:Match all words where there is exactly one “b”, exactly one “t”, and they are adjacent to each other.
exp5 = r"^[^bt]*(bt|tb)[^bt]*$"
regex5 = re.compile(exp5,re.I)
matches = []
for word in wordlist:
    if re.fullmatch(regex5,word):
        matches.append(word)
print("#5: /",exp5,"/i")
print(len(matches)," total matches")
for i in range(5):
    if i < len(matches):
        print(matches[i])
print()
#6: Match all words with the longest contiguous block of a single letter.
# find the longest repeating substring
maxrepeat = 0
for word in wordlist:
    index = 0
    occurence = 0
    repeat = word[index]
    while index < len(word):
        if word[index] == repeat:
            occurence += 1
            index += 1
        else:
            maxrepeat = max(maxrepeat,occurence)
            occurence = 0
            repeat = word[index]
    maxrepeat = max(maxrepeat,occurence)

exp6 = r"^(\w)*(\1){"+str(maxrepeat-1)+r"}\w*$"
print("#6: /",exp6,"/i")
regex6 = re.compile(exp6,re.I)
matches = []
for word in wordlist:
    if re.fullmatch(exp6,word):
        matches.append(word)
print(len(matches), "total matches")
for i in range(5):
    if i < len(matches):
        print(matches[i])
print()

#7 : Match all words with the greatest number of a repeated letter (which may occur anywhere in the word).  Same 
# additional instructions as #6
maxoccurence = 0
for word in wordlist:
        count = dict()
        for ch in word:
            if ch not in count:
                count[ch] = 0
            count[ch] += 1
        for letter in count:
            maxoccurence = max(count[letter],maxoccurence)
exp7 = r"^\w*(\w)(?=(\w*\1){%s})\w*$" % (maxoccurence-1)
regex7 = re.compile(exp7,re.I)
# if re.fullmatch(regex7,"possessednesses"):
#     print("match")
matches = []
for word in wordlist:
    if re.fullmatch(regex7,word):
        matches.append(word)
print("#7: /",exp7,"/i")
print(len(matches), "total matches")
for i in range(5):
    if i < len(matches):
        print(matches[i])
print()

#8: Match all words with the greatest number of adjacent pairs of identical letters.  Order matters; that is, "ab" is 
# not the same pair as "ba".


maxoccurence = 0
for word in wordlist:
    index = 0
    prdict = dict()
    prev = ""
    while index < len(word)-1:
        pr = word[index:index+2]
        if  pr not in prdict:
            prdict[pr] = 0
        prdict[pr] += 1
        maxoccurence = max(prdict[pr],maxoccurence)
        if pr == prev:
            index += 2
        else:
            index += 1
        prev = pr
print(maxoccurence)

exp8 = r"^\w*(\w\w)(\w*\1){"+str(maxoccurence-1)+r"}\w*$"

regex8 = re.compile(exp8,re.I)
matches = []
for word in wordlist:
    if re.fullmatch(regex8,word):
        matches.append(word)
print("#8: /",exp8,"/i")
print(len(matches), "total matches")
for i in range(5):
    if i < len(matches):
        print(matches[i])
print()
# 9: Match all words with the greatest number of consonants.  
consonants = set("bcdfghjklmnpqrstvwxyz")
maxconsonants = 0
for word in wordlist:
    count = 0
    for ch in word:
        if ch in consonants:
            count += 1
    maxconsonants = max(count,maxconsonants)
exp9 = r"^(?=(\w*?[bcdfghjklmnpqrstvwxyz]){%s})\w*$"%maxconsonants
regex9 = re.compile(exp9,re.I)
matches = []
for word in wordlist:
    if re.fullmatch(regex9,word):
        matches.append(word)
print("#9: /",exp9,"/i")
print(len(matches), "total matches")
for i in range(5):
    if i < len(matches):
        print(matches[i])
print()

# 10
exp10a = r"^((\w)(?!\w*\2\w*\2))*$"
regex10 = re.compile(exp10a, re.I)
matches = []
maxlen = 0
for word in wordlist:
    if re.fullmatch(regex10,word):
        matches.append(word)
        maxlen = max(maxlen,len(word))

results = list()
for match in matches:
    if len(match) == maxlen:
        results.append(match)
print("#10: /",exp10a,"/i")
print(len(results), "total matches")
for i in range(5):
    if i < len(results):
        print(results[i])

print()