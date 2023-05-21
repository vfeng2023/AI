"""
Chapter 2: 24, 25, 26
Chapter 4: 31
Chapter 6: 9

"""
# 24:

import nltk
import random
# Natural Language Toolkit: code_random_text

def generate_model(cfdist, word, num=15,n = 5):
    
    for i in range(num):
        words = list(cfdist[word])
        words.sort(key = lambda a: cfdist[word][a],reverse=True)
        words = words[:n]
        print(word, end=' ')
        word = random.choice(words)
"""
# text = nltk.corpus.genesis.words('english-kjv.txt')
text = nltk.corpus.gutenberg.words('austen-emma.txt')
# text2 = nltk.corpus.gutenberg.words('blake-poems.txt')
bigrams = nltk.bigrams(text)
cfd = nltk.ConditionalFreqDist(bigrams) # [_bigram-condition]

generate_model(cfd,'leaves')
"""
# 25
from nltk.corpus import udhr
def find_language(word):
    langWords = dict()
    # make all languages a set
    for id in udhr.fileids():
        if id[-6:] == "Latin1":
            langWords[id] = set(udhr.words(id)) 
    hasWord = []
    for l in langWords:
        if word in langWords[l]:
            hasWord.append(l)

    return hasWord

# result = find_language('the')
# print(result)

# 26:
from nltk.corpus import wordnet as wn
def noun_average():
    total = 0
    synsets = wn.all_synsets('n')
    nouns = 0
    for s in synsets:
        count = len(s.hyponyms())
        if count > 0:
            total += count
            nouns += 1
    return total/nouns
# print(noun_average())

# 29:
def insert(trie, key, value):
    if key:
        first, rest = key[0], key[1:]
        if first not in trie:
            trie[first] = {}
        insert(trie[first], rest, value)
    else:
        trie['value'] = value

def print_nicely(trie,word):
    for key in sorted(trie):
        if key == 'value':
            print(word,":",trie[key])
        else:
            print_nicely(trie[key],word+key)

# trie = {}
# insert(trie, 'chat', 'cat')
# insert(trie, 'chien', 'dog')
# insert(trie, 'chair', 'flesh')
# insert(trie, 'chic', 'stylish')
# print_nicely(trie," ")

# Chapter 6: 9
# from nltk.corpus import ppattach
# nattach = [inst for inst in ppattach.attachments('training') if inst.attachment == "N"]

# Chapter 3: Soundex algorithm 39
def soundex(word):
    """
    SQL implementation
    Save the first letter. Map all occurrences of a, e, i, o, u, y, h, w. to zero(0)
Replace all consonants (include the first letter) with digits as in [2.] above.
Replace all adjacent same digits with one digit, and then remove all the zero (0) digits
If the saved letter's digit is the same as the resulting first digit, remove the digit (keep the letter).
Append 3 zeros if result contains less than 3 digits. Remove all except first letter and 3 digits after it (This step same as [4.] in explanation above).
    """
    word_mappings = {
        'a':0,
        'e':0,
        'i':0,
        'o':0,
        'u':0,
        'y':0,
        'h':0,
        'w':0,
        'b':1,
        'f':1,
        'p':1,
        'v':1,
        'c':2,
        'g':2,
        'j':2,
        'k':2,
        'q':2,
        "s":2,
        "x":2,
        "z":2,
        "d":3,
        "t":3,
        "l":4,
        "m":5,
        "n":5,
        "r":6
    }

    
    word = word.lower()
    result = [word_mappings[w] for w in word]
    l1 = word[0]
    i = 0
    while i < len(result):
        if result[i] == 0:
            del result[i]
        if i-1 >=0 and result[i-1] == result[i]:
            del result[i]
        else:
            i += 1
    if word_mappings[l1] == result[0]:
        del result[0]

    while len(result) < 3:
        result.append(0)
    codeing = l1.upper() + "".join(str(val) for val in result[:3])
    return codeing

print(soundex("Robert"))
print(soundex('Rupert'))

print(soundex('Tymczak'))

print(soundex('Honeyman'))