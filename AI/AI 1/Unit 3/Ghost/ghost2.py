import sys
wordlist = sys.argv[1]
minlen = int(sys.argv[2])
if len(sys.argv) > 3:
    GAME = sys.argv[3]
else:
    GAME = ""
# wordlist = "words_all.txt"
# minlen = 4
# GAME = "A"
with open(wordlist) as f:
    # construct a trie using a dictionary
    # the next letter in a word + the prefix before it is the child
    words = [line.strip().upper() for line in f.readlines()]
    word_set = set()
    possible_paths = dict()
    possible_paths[GAME] = set()
    for word in words:
        if not word.isalpha():
            continue
        if len(word) < minlen:
            continue
        if word[0:len(GAME)]!=GAME:
            continue

        prefixes = [GAME]
        inword_set = False
        for i in range(len(GAME)+1,len(word)+1):
            pre = word[:i]
            prefixes.append(pre)
            if pre in word_set:
                inword_set = True
        if inword_set:
            continue
                

        # adds the children to a the trie 
        for i in range(1,len(prefixes)):
            if prefixes[i-1] in possible_paths:
                possible_paths[prefixes[i-1]].add(prefixes[i])
            else:
                possible_paths[prefixes[i-1]] = set()
                possible_paths[prefixes[i-1]].add(prefixes[i])
        word_set.add(word)


def gameOver(gameSeq,word_set):
    """
    Returns -1 if AI loses, 1 if AI wins, and None if the game isn't over
    """
    if gameSeq in word_set:
        if (len(gameSeq) - len(GAME))%2 == 0:
            return 1
        else:
            return -1
    return None


def max_step(game,game_tree,word_set):
    """
    Represents AI, attempts to maximize score. Returns a max score, calls minstep
    """
    score = gameOver(game,word_set)
    if score is not None:
        return score

    poss_moves = game_tree[game]
    results = []
    for move in poss_moves:
        results.append(min_step(move,game_tree,word_set))

    return max(results)

def min_step(game,game_tree,word_set):
    """
    Represents other players, attempting to minimize score. Returns a min score, calls max_step
    """
    score = gameOver(game,word_set)
    if score is not None:
        return score

    poss_moves = game_tree[game]
    results = []
    for move in poss_moves:
        results.append(max_step(move,game_tree,word_set))
    return min(results)

def find_next_move(game,game_tree,word_set):
    nextMoves = game_tree[game]
    garuntee = []
    for next in nextMoves:
        result = min_step(next,game_tree,word_set)
        if result > 0:
            garuntee.append(next[-1])
    return sorted(garuntee)

# print(possible_paths)
letters = find_next_move(GAME,possible_paths,word_set)
if len(letters) > 0:
    print("Next player can guarantee victory by playing any of these letters:",letters)
else:
    print("Next player will lose!")


