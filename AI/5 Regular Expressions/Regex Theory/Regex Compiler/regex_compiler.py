
import sys

# read the spec file
lang = sys.argv[1]
regEx = sys.argv[2]
filename = sys.argv[3]
LETTERS = set(lang)
# def compileDFA(regex):
#     """
#     Compiles the DFA
#     """
#     states = [0,1]
#     final = [1]
#     # 1. refex to NFA w/ ε
#         # parsing the regex espression: using a stack
#         # stk = new Stack()
#         # for ch in regex:
#             # if ch in language: 
#                 # if stack is not empty:
#                     # pop characters and add as node until encounter an operator
#                 # else:
#                    # push onto the stack
#             # else:
#                 #  # if op is (:
#                         # add ( to stack
#                     # if op is ):
#                         # connect current state onto previous state
#                     # if op is |:
#                     #   make current state a final state
#                         # go back to previous state
#                     # if op is ?:
#                         # add special link
#                     # if op is *:
#                     #   add E self ref E
#                     # if op is + : add self self E 
#     stk = list()
#     stateTransitions = dict()
#     for ch in regex:
#         if ch in LETTERS:
#             while len(stk) > 0:
#                 if stk[-1] in LETTERS:
#                     add_node()
#                     stk.pop()
#                 else:
#                     break
#             stk.append(ch)
#         else: # is an operator
#             if ch == "(":
#                 stk.append("(")
#             elif ch == ")":
#                 pass
            
    # 2. NFAwE --> NFA
    # 3 NFA to DFA
    # remove redundant states
def find(regex,symbol):
    for i in range(len(regex)):
        if regex[i] == symbol:
            return i
    return -1
def compileDFA(regex,language,currNode,stateTransitions):
    # parse expression
    # precedence: |, () > *+?
    # first look for | and parentheis in that order 
    orindex = find(regex,"|")
    if orindex > 0:
        o
    
    

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
def add_node(transition,parent,val):
    pass
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


