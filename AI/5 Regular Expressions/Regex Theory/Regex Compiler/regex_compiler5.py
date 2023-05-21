
import sys
from collections import deque
# read the spec file
# sys.argv = ["junk","abcd","(a|b*)c|(a+d*c+|a+(cc)+)?b","dfa_ex_tests_2.txt"]
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
    # print("initial population of dictionary")
    compileDFA(regex,language,stateTrans,0,1)
    print("NFA with epsilon")
    printDFA(["eps"] + list(lang),stateTrans,len(stateTrans))
    # print()
    print("NFA without epsilon")
    newNFA,newfinal = makeNFA(stateTrans,final)
    printDFA(sorted(language),newNFA,len(newNFA))
    print("Final: ",newfinal)
    print()
    print("Building DFA w/ hybrid nodes")
    # input()
    nfa2 = buildhybrid(newNFA,newfinal)
    printDFA(lang,nfa2,len(nfa2))
    
    print("Final: ",newfinal)

    dfa2 = pruneNodes(nfa2,newfinal)
    dfa3 = removeRedundant(dfa2,newfinal)
    printDFA(sorted(lang),dfa3,max(dfa3.keys())+1)
    newfinal = sorted(set(newfinal))
    print("Final: ",newfinal)
    return dfa3,newfinal


def compileDFA(regex,language,stateTransitions,start,end):
    print("Regex: ",regex)
    print("Start node: ",start)
    print("end node: ",end)
    printDFA(["eps","a","b","c","d"],stateTransitions,len(stateTransitions))
    regex = regex.strip()
    orsindex = find(regex,"|",0,len(regex)-1) # find the locations of or
    if len(regex) == 0: # returns none if the regex is empty
        return;
    if len(regex) == 1: # adds the node with corresponding start and end 
        add_node(stateTransitions,start,regex,end)
        return
    for ind in orsindex:
        firstHalf = regex[0:ind]
        secondHalf = regex[ind+1:]
        if firstHalf.count("(") == firstHalf.count(")"):
            print("first Half: ",firstHalf)
            print("SecondHalf: ",secondHalf)
            compileDFA(firstHalf,language,stateTransitions,start,end) # 
            compileDFA(secondHalf,language,stateTransitions,start,end)
            return
     
    # look at first token:
    # print(regex[0])
    if regex[0] in language:
        # print(regex[0])
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
    if (index + 1 < len(regex) and regex[index+1] not in {"*","+","?"}) or (index+1>=len(regex)):
        if regex[0] in language:
            firstHalf = regex[0:1]
        else:
            firstHalf = regex[1:index] # to strip the outer ()
        secondHalf = regex[index+1:]
        if len(secondHalf) > 0:
            newNode = max(stateTransitions.keys() )+1
        else:
            newNode = end
        if newNode not in stateTransitions:
            stateTransitions[newNode] = dict()
        compileDFA(firstHalf,language,stateTransitions,start,newNode)
        compileDFA(secondHalf,language,stateTransitions,newNode,end)
        return
    elif index+1 < len(regex) and regex[index+1] == "?":
        if regex[0] in language:
            firstHalf = regex[0:1]
        else:
            firstHalf = regex[1:index] # to strip the outer ()
        secondHalf = regex[index+2:]
        
        if len(secondHalf) > 0:
            newNode = max(stateTransitions.keys()) + 1
        else:
            newNode = end
        if newNode not in stateTransitions:
            stateTransitions[newNode] = dict()
        add_node(stateTransitions,start,"eps",newNode)
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
        if newNode not in stateTransitions:
            stateTransitions[newNode] = dict()
        add_node(stateTransitions,start,"eps",newNode)
        compileDFA(firstHalf,language,stateTransitions,newNode,newNode)

        if len(secondHalf) > 0:
            newNode2 = max(stateTransitions.keys()) + 1
        else:
            newNode2 = end
        if newNode2 not in stateTransitions:
            stateTransitions[newNode2] = dict()
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
        if newNode not in stateTransitions:
            stateTransitions[newNode] = dict()
        compileDFA(firstHalf,language,stateTransitions,start,newNode)
        compileDFA(firstHalf,language,stateTransitions,newNode,newNode)
        if len(secondHalf) > 0:
            newNode2 = max(stateTransitions.keys()) + 1
        else:
            newNode2 = end
        if newNode2 not in stateTransitions:
            stateTransitions[newNode2] = dict()
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
    print(epsenclosures)
    # create a copy of state transitions
    # print(epsenclosures)
    newNFA = {node:stateTransitions[node].copy() for node in stateTransitions}

    # remove all epsilon connections for a node, if there are any
    for node in newNFA:
        if "eps" in newNFA[node]:
            del newNFA[node]["eps"]
    # add the properties of all nodes in said nodes epsilon enclosures
    for node in epsenclosures:
        inherit = epsenclosures[node] #nodes to be inherited
        for noE in inherit: # no = a node in the epsilon enclosure
            if noE in finalNodes: # add finalty character
                newfinal.append(node)
            vals = stateTransitions[noE] # the links of the node
            for key in vals: # each link
                # append to the appropriate tuples
                if key != "eps":
                    if key in newNFA[node]:
                        for v in newNFA[noE][key]:
                            if v not in newNFA[node][key]:
                                newNFA[node][key] += (v,)
                    else:
                        newNFA[node][key] = vals[key]
    # print(newNFA)
    return newNFA,newfinal
def buildhybrid(nfa,finalNodes):
    hybrids = dict() # tuple(in sorted order) --> corresponding new node
    nextNode = max(nfa.keys()) + 1
    # print("Before converting to DFA")
    # printDFA(lang,nfa,len(nfa))
    # should be repeated
    newNFA = dict()
    # copies all nondeterministic nodes t the dict dfa
    for node in nfa:
        newNFA[node] = dict()
        nodelinks = nfa[node]
        for nlin in nodelinks:
            if len(nodelinks[nlin]) == 1:
                newNFA[node][nlin] = nodelinks[nlin]
    for node in nfa:
        links = nfa[node] # refers to the connections from the nodes
        # print("links are ",links)
        for lin in links: # characters
            # aka nondeterministic
            if len(links[lin]) > 1: # if nondeterministic
                newNFA[node][lin] = (hybridizeNodes(links[lin],finalNodes,nfa,newNFA,hybrids),)

                

    nfa = newNFA
    # print(newNFA)
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
    visited.add(startNode)
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
                        if node == 4 or node2 == 4:
                            print(node,node2)
                        for link in dict1:
                            if link in dict2 and dict2[link] == dict1[link]:
                                pass
                            else:
                                same = False
                                break
                        if same and node2 in finalNodes and node in finalNodes:
                            duplicates.add((node2,node))
                    else:
                        continue
        if len(duplicates) == 0:
            return dfa
        intermediateDFA = dfa.copy()
        # print("intermediateDFA, ",intermediateDFA)
        # print("Dublicates:",duplicates)
        for dup in duplicates:
            d1,d2 = sorted(dup)
            # eliminate the first one in the pair, reroute all connections to said pair
            if d2 in intermediateDFA:
                del intermediateDFA[d2]
            if d1 in intermediateDFA:
                for node in intermediateDFA:
                    for link in intermediateDFA[node]:
                        if intermediateDFA[node][link] == d2:
                            intermediateDFA[node][link] = d1
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
def hybridizeNodes(nodestohybr, finalNodes,stateTransitions,newNFA,hybridNodes):
    """
    add to the new NFA, but node is added(do not create new node outside of this function!)
    returns the number of the new hybrid node to add
    """
    # for each node to hybridize 
    nodestohybr = tuple(sorted(set(nodestohybr))) # get in sorted order 
    if nodestohybr in hybridNodes:
        return hybridNodes[nodestohybr]
    newNode = max(newNFA.keys()) + 1
    # adding to the new DFA 
    newNFA[newNode] = dict()
    hybridNodes[nodestohybr] = newNode
    # assign appropriate properties from each constitutent node
    for node in nodestohybr:
        if node in finalNodes:
            finalNodes.append(newNode)
        for link in stateTransitions[node]:
            if link in newNFA[newNode]:
                newNFA[newNode][link] += stateTransitions[node][link]
            else:
                newNFA[newNode][link] = stateTransitions[node][link]
    # recursively create any new hybrid nodes which result from the formation of the current hybrid node and replace those links
    for link in newNFA[newNode]:
        if len(newNFA[newNode][link]) > 1:
            newNFA[newNode][link] = (hybridizeNodes(newNFA[newNode][link],finalNodes,stateTransitions,newNFA,hybridNodes),)
    return newNode    
        
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
        if s in spec:
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
dfa,finalizedfinal = parseRegex(regEx,languageSet)
with open(filename) as f:
    cases = [line.strip() for line in f.readlines()]

for test in cases:
    result = traceExpression(test,dfa, finalizedfinal)
    print(result,test)
