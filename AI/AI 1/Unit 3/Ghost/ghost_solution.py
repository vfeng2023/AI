import sys
import time
import string
"""
read in words and build prefix dictionary for all the words
discard any words that are shorter than the minimum length or are composed by adding letters on to an existing word
"""
file =  sys.argv[1]
minlen = int(sys.argv[2])
curr_game = ""
# if len(sys.argv) > 3:
#     curr_game = sys.argv[3]

# start_time = time.perf_counter()
with open(file) as f: # builds the words with each of the prefixes
    wordlist = []
    word_set = set()
    prefix_dict = dict()
    lines =[line.strip().upper() for line in f.readlines()]
    for w in lines:
        if not w.isalpha():
            continue
        if len(w) < minlen:
            continue
        word_set.add(w)
        prefixes = []
        alrWord = False
        for end in range(1,len(w)):
            prefixes.append(pref:=w[0:end])
            if pref in word_set:
                alrWord = True
                break
        if alrWord:
            continue
        for pre in prefixes:
            if pre in prefix_dict:
                prefix_dict[pre].add(w)
            else:
                prefix_dict[pre] = set()
                prefix_dict[pre].add(w)
# print(prefix_dict)
# end_time = time.perf_counter()
# print("Built in ",end_time-start_time," seconds")

def next_move(game,prefix_dict):
    """
    goes through alphabet(possible options)
    checks if game + letter is valid(i.e contained in prefixes)
    if every word in the set associated with the prefix results in an end which is not the AI, then choice garuntees a win
    """
    bestChoice = []
    alphabet = string.ascii_uppercase
    for leeter in alphabet:
        poss_pre = game + leeter
        if poss_pre not in prefix_dict:
            continue
        alwaysWin = True
        for word in prefix_dict[poss_pre]:
            if (len(word) - len(poss_pre))%2 == 0:
                alwaysWin = False
                break
        if alwaysWin:
            bestChoice.append(leeter)
        return bestChoice
# print("abandon",("ABANDON" in prefix_dict["A"]))
# print("abandoning",("ABANDONING" in prefix_dict["A"]))
# print("MISENROL" in prefix_dict["M"])
# print("MISENROLL" in prefix_dict["M"])
print(prefix_dict["M"])
count = 0
for s in sorted(prefix_dict["M"]):
    print(len(s))
    if len(s) % 2 == 0:
        print("AI wins",s)
    else:
        print("AI loses",s)
        count += 1
print(len(prefix_dict["M"]))
print(count)
# print(next_move(curr_game,prefix_dict))

