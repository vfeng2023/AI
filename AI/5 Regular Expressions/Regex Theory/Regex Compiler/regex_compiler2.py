
from audioop import add
import sys

# read the spec file
lang = sys.argv[1]
regEx = sys.argv[2]
filename = sys.argv[3]
LETTERS = set(lang)
def find(regex,symbol,start,end):
    """
    End is inclusive
    """
    vals = []
    for i in range(end+1):
        if regex[i] == symbol:
            vals.append(i)
    return vals
def parseRegex(regex):
    """
    Processes regex to be compiled
    """
    # 1. Look for parenthesis,
def compileDFA(regex,language,currNode,stateTransitions,parent):
    # parse expression
    # precedence: |, () > *+?
    # first look for | and parentheis in that order 
    # the maximum node would be the child
    # the start would be the second smallest node
    if len(regex) ==1:
        lastNode = max(stateTransitions.keys()) # not as in "final" node, rather the last node
        add_node(stateTransitions,parent,regex,lastNode)
    
    
    # 1. check for the highest or -- those not contained in parenthesis
    orindex = find(regex,"|",0,len(regex)-1)
    if orindex!=-1:
        part1 = regex[0:orindex]
        part2 = regex[orindex+1:]
        if part1.count(")")!=part1.count("("):
            pass
        else:
            compileDFA(part1,args)
            compileDFA(part2,args)
            return
    # parse appropriately (parenthesis parsing combined into operation parsing)
    # look for the first higest index ? NOT FUNCTIONAL
    qindex = find(regex,"?",0,len(regex)-1)
    while qindex!=-1:
        if regex[0:qindex].count("(") == regex[0:qindex].count(")"):
            lastNode = max(stateTransitions.keys())
            add_node(stateTransitions,parent,"eps",lastNode)
            compileDFA(regex[0:qindex],args)
            return
    # look for star
    starind = find(regex,"*",0,len(regex)-1)
    if starind !=-1:
        if regex[0:starind].count("(") == regex[0:starind].count(")"):
            lastNode = max(stateTransitions.keys())
            newNode = lastNode + 1
            add_node(stateTransitions,parent,"eps",newNode)
            add_node(stateTransitions,newNode,"eps",lastNode)
            parent = newNode
            compileDFA(rem_regex,args)
            return
    # look for plus
    plusindex = find(regex,"+",0,len(regex)-1)
    if plusindex != -1:
        if regex[0:plusindex].count("(") == regex[0:plusindex].count(")"):
            lastNode = max(stateTransitions.keys())
            newNode = lastNode + 1
            add_node(stateTransitions,newNode,"eps",lastNode)
            compileDFA(relevant_terms)
            return
    
    

def add_node(stateTransitions,parent,link,child):
    """
    stateTransitions is a nested dict: parent:dict(link:child)
    link = letter
    """
    if parent not in stateTransitions:
        stateTransitions[parent] = dict()
    if link in stateTransitions[parent]:
        stateTransitions[parent][link] += (child)
    else:
        stateTransitions[parent][link] = (child)
def printDFA(lang,spec,states):
    """
    Nicely prints a DFA state Transition given language, dictionary, and number of states
    """
    letters = sorted(lang)
    # print the letters
    print("*",end="\t")
    for l in letters:
        print(l,end="\t")
    print()

    for s in range(states):
        nextStates = spec[s]
        print(s,end="\t")
        for ch in letters:
            if ch in nextStates:
                print(nextStates[ch],end="\t")
            else:
                print("_",end="\t")
        print()
def traceExpression(word,dfa,final):
    currState = 0
    for letter in word:
        currDict = dfa[currState]
        if letter not in currDict:
            return False
        else:
            currState = currDict[letter]
    if currState in final:
        return True
    return False

# printDFA(lang,stateTransitions,numStates)


