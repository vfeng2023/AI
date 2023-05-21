import sys
def part2(number):
    """Number is the questions number"""
    if number == 1:
        # Question 1 dictionary
        dfa = {
            0: {
                "a":1
            },
            1:{
                "a":2
            },
            2:{
                "b":3
            },
            3:{},
        }
        lang = "ab"
        finalStates = [3]
        return lang, dfa,finalStates
    # question 2 dfa
    elif number == 2:
        lang = "012"
        dfa = {
            0:{
                "1":1,
                "0":0,
                "2":0,
            },
            1:{
                "0":0,
                "1":1,
                "2":0,
            }
        }
        finalStates = [1]
        return lang, dfa, finalStates
    elif number == 3:
        lang = "abc"
        dfa = {
            0:{
                "a":0,
                "b": 1,
                "c": 0,
            },
            1:{
                "a":1,
                "b":1,
                "c":1
            }
        }
        finalStates = [1]
        return lang, dfa, finalStates
    elif number == 4:
        lang = "01"
        dfa = {
            0:{
                "0":1,
                "1":0,
            },
            1:{
                "0":0,
                "1":1,
            },
        }
        finalStates = [0]
        return lang,dfa,finalStates
    elif number == 5:
        lang = "01"
        # end up at 0 = no 1s
        dfa = {
            0:{
                "0": 1,
                "1": 2,
            }, # even number of both
            1:{
                "0":0,
                "1":3,
            }, # even 1s, odd 0s
            2:{
                "0":3,
                "1":0,
            }, # odd 1s, even 0s
            3:{
                "0":2,
                "1":1,
            } # odd 1s, odd 0s

        }
        finalStates = [0]
        return lang,dfa, finalStates
    elif number == 6:
        lang = "abc"
        dfa = {
            0:{
                "a":1,
                "b":0,
                "c":0,
            },
            1:{
                "a":1,
                "b":2,
                "c":0,
            },
            2:{
                "c":3,
                "b":0,
                "a":1,
            },
            3:{
                "c":3,
                "b":3,
                "a":3
            }
        }
        finalStates = [0,1,2]
        return lang,dfa,finalStates
    else:
        lang = "01"
        dfa = {
            0:{
                "0":0,
                "1":1,
            },
            1:{
                "0":2,
                "1":1,
            },
            2:{
                "0":2,
                "1":3,
            },
            3:{
                "0":2,
                "1":4,
            },
            4:{
                "0":4,
                "1":4
            }
        }
        finalStates = [4]
        return lang,dfa,finalStates
# read the spec file
filename = sys.argv[1]
try:
    num = int(filename)
    lang,stateTransitions,finalStates = part2(num)
    numStates = len(stateTransitions)
except ValueError:
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
        # print(lines)
        lang = set(lines[0])
        numStates = int(lines[1])
        finalStates = [int(st) for st in lines[2].split()]
        stateTransitions = dict()
        currState = 0
        # reading dfa from spec
        for index in range(3,len(lines)):
            line = lines[index]
            if line.isdigit():
                state = int(line)
                stateTransitions[state] = dict()
                currState = state
            elif len(line) > 0:
                line = line.split()
                letter = line[0]
                nextState = int(line[1])
                stateTransitions[currState][letter] = nextState

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

printDFA(lang,stateTransitions,numStates)
print("Final states: ",finalStates)
with open(sys.argv[2]) as f:
    # open test cases
    cases = [line.strip() for line in f.readlines()]
    for case in cases:
        print(traceExpression(case,stateTransitions,finalStates), case)
# printDFA(lang,stateTransitions,numStates)


