
import sys
from collections import deque
# read the spec file
sys.argv = ["junk","ab","(ab)|a","junk"]
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
def parseRegex(regex,language):
    """
    Processes regex to be compiled
    """
    # build the NFA w/E
    stateTrans = dict()
    stateTrans[0] = dict()
    stateTrans[1] = dict()
    final = [1]
    # populates the dictionary
    print("initial population of dictionary")
    compileDFA(regex,language,stateTrans,0,1)
    printDFA(["eps"] + list(lang),stateTrans,len(stateTrans))
    print()
    print("NFA without epsilon")
    newNFA,newfinal = makeNFA(stateTrans,final)
    printDFA(language,newNFA,len(newNFA))
    print("Final: ",newfinal)
    print()
    print("Building DFA w/ hybrid nodes")
    input()
    nfa2 = buildhybrid(newNFA,newfinal)
    printDFA(lang,nfa2,len(nfa2))
    
    print("Final: ",newfinal)

    dfa2 = pruneNodes(nfa2,newfinal)
    dfa3 = removeRedundant(dfa2,newfinal)

    return dfa3


def compileDFA(regex,language,stateTransitions,start,end):
    orsindex = find(regex,"|",0,len(regex)-1) # find the locations of ors outside ()
    if len(regex) == 0: # returns none i
        return;
    if len(regex) == 1:
        add_node(stateTransitions,start,regex,end)
        return
    for ind in orsindex:
        firstHalf = regex[0:ind]
        secondHalf = regex[ind+1:]
        if firstHalf.count("(") == firstHalf.count(")"):
            compileDFA(firstHalf,language,stateTransitions,start,end)
            compileDFA(secondHalf,language,stateTransitions,start,end)
            return
    # look at first token:
    if regex[0] in language:
        index=0
    elif regex[0] == "(":
        # need to find the corresponding ()
        stk = list()
        for index,ch in enumerate(regex):
            if regex[index] == "(":
                stk.append("(")
            if regex[index] == ")":
                stk.pop()
                if len(stk) == 0:
                    break
        # index refers to position of end of character
        index = index
    if index + 1 < len(regex) and regex[index+1] not in {"*","+","?"}:
        if regex[0] in language:
            firstHalf = regex[0:1]
        else:
            firstHalf = regex[1:index] # to strip the outer ()
        secondHalf = regex[index+1:]
        if len(secondHalf) > 0:
            newNode = max(stateTransitions.keys() )+1
        else:
            newNode = end
        compileDFA(firstHalf,language,stateTransitions,start,newNode)
        compileDFA(secondHalf,language,stateTransitions,newNode,end)
        return
    elif index+1 < len(regex) and regex[index+1] == "?":
        if regex[0] in language:
            firstHalf = regex[0:1]
        else:
            firstHalf = regex[1:index] # to strip the outer ()
        secondHalf = regex[index+1:]
        add_node(stateTransitions,start,"eps",end)
        if len(secondHalf) > 0:
            newNode = max(stateTransitions.keys()) + 1
        else:
            newNode = end
        compileDFA(firstHalf,language,stateTransitions,start,newNode)
        compileDFA(secondHalf,language,stateTransitions,newNode,end)
        return
    elif index+1 < len(regex) and regex[index+1] == "*":
        if regex[0] in language:
            firstHalf = regex[0:1]
        else:
            firstHalf = regex[1:index] # to strip the outer ()
        secondHalf = regex[index+2:]
        newNode = max(stateTransitions.keys()) + 1
        add_node(stateTransitions,start,"eps",newNode)
        compileDFA(firstHalf,language,stateTransitions,newNode,newNode)

        if len(secondHalf) > 0:
            newNode2 = max(stateTransitions.keys()) + 1
        else:
            newNode2 = end
        
        add_node(stateTransitions,newNode,"eps",newNode2)
        compileDFA(secondHalf,language,stateTransitions,newNode2,end)
        return
    elif index + 1 < len(regex) and regex[index+1] =="+":
        if regex[0] in language:
            firstHalf = regex[0:1]
        else:
            firstHalf = regex[1:index] # to strip the outer ()
        secondHalf = regex[index+2:]
        newNode = max(stateTransitions.keys()) + 1
        compileDFA(firstHalf,language,stateTransitions,start,newNode)
        compileDFA(firstHalf,language,stateTransitions,newNode,newNode)
        if len(secondHalf) > 0:
            newNode2 = max(stateTransitions.keys()) + 1
        else:
            newNode2 = end
        
        add_node(stateTransitions,newNode,"eps",newNode2)
        compileDFA(secondHalf,language,stateTransitions,newNode2,end)
        return

def makeNFA(stateTransitions,finalNodes):
    # find all epsilon and place into epsilon enclosure.
    newfinal = finalNodes.copy()
    epsenclosures = dict()
    
    for node in stateTransitions:
        result = traceEps(stateTransitions,node,tuple())
        result = tuple(sorted(set(result)))
        epsenclosures[node] = result
        
    # create a copy of state transitions
    # print(epsenclosures)
    newNFA = {node:stateTransitions[node].copy() for node in stateTransitions}

    # remove all epsilon connections for a node, if there are any
    for node in newNFA:
        if "eps" in newNFA[node]:
            del newNFA[node]["eps"]
    # add the properties of all nodes in said nodes epsilon enclosures
    for node in epsenclosures:
        inherit = epsenclosures[node]
        for no in inherit:
            if no in finalNodes:
                newfinal.append(node)
            vals = stateTransitions[no]
            for key in vals:
                # append to the appropriate tuples
                if key != "eps":
                    if key in newNFA[node]:
                        for v in vals[key]:
                            if v not in newNFA[node][key]:
                                newNFA[node][key] += (v,)
                    else:
                        newNFA[node][key] = vals[key]
    # print(newNFA)
    return newNFA,newfinal
def buildhybrid(nfa,finalNodes):
    hybrids = dict() # tuple --> corresponding new node
    nextNode = max(nfa.keys()) + 1
    # print("Before converting to DFA")
    # printDFA(lang,nfa,len(nfa))
    # should be repeated
    nonDFA = True
    while nonDFA:
        # BS copying methodnewNFA = {node:nfa[node].copy() for node in nfa if len(nfa[node]) == 1} 
        # # only add deterministic connections to new graph
        newNFA = dict()
        for node in nfa:
            newNFA[node] = dict()
            nodelinks = nfa[node]
            for nlin in nodelinks:
                if len(nodelinks[nlin]) == 1:
                    newNFA[node][nlin] = nodelinks[nlin]
        nonDFA = False
        for node in nfa:
            links = nfa[node] # refers to the connections from the nodes
            # print("links are ",links)
            for lin in links: # characters
                # aka nondeterministic
                if len(links[lin]) > 1: # if nondeterministic
                    nonDFA = True
                    # create hybrid node
                    hybr = tuple(sorted(links[lin]))
                    if hybr not in hybrids: # makes new node if hybrid node is not already there
                        hybrids[hybr] = nextNode # node number to hybrid
                        currNode = nextNode # set the node to add to
                        newNFA[currNode] = dict() # creates corresponding dictionary
                        nextNode += 1 # increments to the next number if adding
                        # inherit the properties of the hybrid node
                        for part in hybr:
                            # for each of partNodes, port all nondeterministic connections
                            partLink = nfa[part] # gets the links of the component of the hybrid node
                            for plink in partLink: # iterates through each of the links in the part of hybrid
                                if len(partLink[plink]) == 1: # adds to newNFA is the connection is deterministic
                                    if plink in newNFA[currNode]: # incase of double nondeterministic, adds the node to newNFA[currNode]
                                        if partLink[plink][0] == part: # incase of self-reference
                                            newNFA[currNode][plink] += (currNode,)
                                        else:
                                            newNFA[currNode][plink] += partLink[plink]
                                    else:
                                        if partLink[plink][0] == part:
                                            newNFA[currNode][plink] = (currNode,)
                                        else:
                                            newNFA[currNode][plink] = partLink[plink] # instantiates the link in the newNFA
                            if part in finalNodes and currNode not in finalNodes: 
                                finalNodes.append(currNode) # inherits finality if not already in final
                        # eliminate repeats in the hybrid node
                        print("newNFA[currNode] @ 209",newNFA[currNode])
                        for l in newNFA[currNode]: # for each link
                            print("l @ 211",l) # eliminates the 
                            newNFA[currNode][l] = tuple(set(newNFA[currNode][l]))
                    else:
                        currNode = hybrids[hybr] # otherwise, just connect to existing one
                    newNFA[node][lin] = (currNode,) # replace reference in newNFA with link to hybrid node 
                    

        nfa = newNFA
    # turn tuple into dict
    dfa = dict()
    for node in nfa:
        dfa[node] = dict()
        for ln in nfa[node]:
            dfa[node][ln] = nfa[node][ln][0]
    return dfa

def pruneNodes(stateTransitions,finalNode):
    startNode = 0
    fringe = deque()
    fringe.append(startNode)
    visited = set()
    while len(fringe) > 0:
        node = fringe.popleft()
        children = stateTransitions[node]
        for link in children:
            child = children[link]
            if child not in visited:
                fringe.append(child)
                visited.add(child)

    modTransitions = stateTransitions.copy()
    for node in stateTransitions:
        if node not in visited:
            del modTransitions[node]

    ind = 0
    while ind < len(finalNode):
        if finalNode[ind] not in visited:
            del finalNode[ind]
        else:
            ind += 1
    return modTransitions
            
def removeRedundant(dfa,finalNodes):
    # for node in nodes:
        # for node 2 in nodes:
            # if node2 < node:
                # loop over the links of both nodes, if links are the same then pair them and add to the set
    while True:
        duplicates = set()
        for node in dfa:
            for node2 in dfa:
                if node2 < node:
                    dict1 = dfa[node]
                    dict2 = dfa[node2]
                    if len(dict1) == len(dict2):
                        same = True
                        for link in dict1:
                            if link in dict2 and dict2[link] == dict1[link]:
                                pass
                            else:
                                same = False
                                break
                        if same:
                            duplicates.add((node2,node))
                    else:
                        break
        if len(duplicates) == 0:
            return dfa
        intermediateDFA = dfa.copy()
        for dup in duplicates:
            d1,d2 = dup
            # eliminate the first one in the pair, reroute all connections to said pair
            if d2 in dfa:
                del intermediateDFA[d2]
            for node in dfa:
                for link in dfa[node]:
                    if dfa[node][link] == d2:
                        dfa[node][link] = d1
            if d2 in finalNodes:
                finalNodes.remove(d2)
        dfa = intermediateDFA
    # remove the second one in each pair from the set
def traceEps(stateTransitions,currentState,nodes):
    """
    nodes is a tuple
    """
    if "eps" not in stateTransitions[currentState]:
        return nodes
    else:
        nodes += stateTransitions[currentState]["eps"]
        for val in stateTransitions[currentState]["eps"]:
               nodes += traceEps(stateTransitions,val,nodes)
        return nodes 

    
    

def add_node(stateTransitions,parent,link,child):
    """
    stateTransitions is a nested dict: parent:dict(link:child)
    link = letter
    """
    if parent not in stateTransitions:
        stateTransitions[parent] = dict()

    if child not in stateTransitions:
        stateTransitions[child] = dict()
    
    if link in stateTransitions[parent]:
        stateTransitions[parent][link] += (child,)
    else:
        stateTransitions[parent][link] = (child,)
def printDFA(lang,spec,states):
    """
    Nicely prints a DFA state Transition given language, dictionary, and number of states
    """
    letters = lang
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

languageSet = set(lang)
nfa = parseRegex(regEx,languageSet)
# printDFA(lang,stateTransitions,numStates)


