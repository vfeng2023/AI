import random
import string
import math
import sys

# constants for genetic algorithm
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE= 20
TOURNAMENT_WIN_PROBABILITY = 0.75
CROSSOVER_POINTS =5
MUTATION_RATE = 0.8
NUM_GENERATIONS = 500

# encodes the message
def encode(alphabet,code,message):
    plaintextToCipher = dict() # dictionary mapping plaintext letters to ciphertext letters
    for i in range(len(alphabet)): # adds each letter in the alphabet to the dictionary for plaintext
        plaintextToCipher[alphabet[i]] = code[i]
    
    encodedMsg = ""
    message = message.upper()
    for ch in message:
        if ch.isalpha():
            encodedMsg += plaintextToCipher[ch]
        else:
            encodedMsg += ch
    return encodedMsg

def decode(alpha,code,message):
    message = message.upper()
    cipherToPlain = dict()
    for i in range(len(code)):
        cipherToPlain[code[i]] = alpha[i]
    plain = ""
    for ch in message:
        if ch in cipherToPlain:
            plain += cipherToPlain[ch]
        else:
            plain += ch
    return plain
# """Testing"""
alpha = list(string.ascii_uppercase)
code = alpha.copy()
random.shuffle(code)

# msg = "Hello, I am Mylzyplkfffffffffff. I like pie. My fac\n color is blueee23456"
# ciphertext = encode(alpha,code,msg)
# plaintext = decode(alpha,code,ciphertext)

# print("encoded: ",ciphertext)
# print("decoded: ",plaintext)

# reads in the freqences of ngram in english
with open("ngrams.txt") as f:
    ALLGRAMS = dict() # dict with length: dict(ngram freq)
    for line in f.readlines():
        ngram, freq = line.split()
        # print(ngram)
        ngram = ngram.upper()
        freq = int(freq)
        size = len(ngram)
        if size in ALLGRAMS:
            ALLGRAMS[size][ngram] = freq
        else:
            ALLGRAMS[size] = dict()
            ALLGRAMS[size][ngram] = freq

def fitnessScore(allngrams, message,base):
    """
    Calculate the fitness score by  adding the log of each found ngram in message occuring in english
    """
    ngramsize = 3
    gramfreq = allngrams[ngramsize]
    total = 0
    # message = message.upper()
    for i in range(len(message)):
        gram = message[i:i+ngramsize]
        if gram in gramfreq:
            total += math.log(gramfreq[gram],base)
    return total

"""Test fitness function"""
msg = """NU XTZEIMYTNEVZ INUHU YM, ZML SPYVI NXILNFFZ XNFF IVPU N API VNTD.  NU PI ILTWU MLI, P XNW YM N FMWY JNZ 
JPIVMLI LUPWY NWZ MC IVNI YFZEV IVNI ITNDPIPMWNFFZ CMFFMJU 'D' NI NFF.  PUW'I IVNI ULTETPUPWY?  P CMLWD 
IVPU ULTETPUPWY, NWZJNZ!  NW NLIVMT JVM NFUM CMLWD IVPU ULTETPUPWY, FMWY NYM, NXILNFFZ FMUI SNWZ SMWIVU 
JTPIPWY N AMMH - N CLFF CPXIPMWNF UIMTZ - JPIVMLI IVNI YFZEV NI NFF.  NSNRPWY, TPYVI?"""

# print(fitnessScore(ALLGRAMS,msg,4,2))

def hillclimb(msg,ALLGRAMS):
    """Performs hillclimbing algorithm
    Take an encoded message 
  Start with a random permutation of the alphabet as a candidate cipher alphabet 
  “Decode” the message using that cipher alphabet 
  Score the results, using the fitness function described above 
  Then: loop infinitely.  Randomly swap a single pair of letters in the cipher alphabet, and repeat the 
decoding/scoring process, keeping the change if it results in a higher score and ignoring it if the score does not 
improve.  Each time, print the “decoded” text out to the console; you can watch the hill climbing process unfold. 
    """
    engAlpha = list(string.ascii_uppercase)
    startCand = engAlpha.copy()
    prevCipher = engAlpha
    random.shuffle(startCand)
    msg = msg.upper()
    plaintext = decode(engAlpha,startCand,msg)
    currScore = fitnessScore(ALLGRAMS,plaintext,2)
    while True:
        prevScore = currScore
        i1 = random.randint(0,len(engAlpha)-1)
        i2 = random.randint(0,len(engAlpha)-1)
        startCand[i1],startCand[i2] = startCand[i2],startCand[i1]
        ptext = decode(engAlpha,startCand,msg)
        score = fitnessScore(ALLGRAMS,ptext,2)
        if score < currScore:
            startCand[i1],startCand[i2] = startCand[i2],startCand[i1]
            # swap back if lower score

        # input()
        print("Decoded message: ",ptext)
        print()
# msg = """
# XMTP CGPQR BWEKNJB GQ OTGRB EL BEQX BWEKNJB, G RFGLI.  GR GQ BEQX 
# ABSETQB RFGQ QBLRBLSB TQBQ EJJ RBL KMQR SMKKML VMPYQ GL BLDJGQF:  
# 'G FEUB RM AB E DMMY QRTYBLR GL RFER SJEQQ GL RFB PMMK MC RFER 
# RBESFBP
# """
# hillclimb(msg,ALLGRAMS)

def generatePop():
    """
    creates intitial population
    """
    count = 0
    pop = set()
    alpha = list(string.ascii_uppercase)
    while len(pop) < POPULATION_SIZE:
        random.shuffle(alpha)
        newcipher = "".join(alpha)
        if newcipher in pop:
            pass
        else:
            pop.add(newcipher)
    return list(pop)

def selection(pop:list,myMsg):
    nextgen = set()
    stratScore = dict()
    for strat in pop:
        plaintext1 = decode(string.ascii_uppercase,strat,myMsg)
        stratScore[strat] = fitnessScore(ALLGRAMS,plaintext1,2)
    pop.sort(key=lambda a:stratScore[a],reverse=True)
    # for cipher in pop:
    #     print(cipher, stratScore[cipher])
    # input()
    # print(pop)
    # print the bet one
    # print(stratScore)
    print("Best cipher result: ")
    print(res:=decode(string.ascii_uppercase,pop[0],myMsg))
    print("Score of best cipher result",fitnessScore(ALLGRAMS,res,2))
    print("score from stratScore",stratScore[pop[0]])
    # print(pop[0])
    # input()
    # print(string.ascii_uppercase)
    for i in range(NUM_CLONES):
        nextgen.add(pop[i])
   #  input()
    print(nextgen)
    # repeat for population size times
    while len(nextgen) < POPULATION_SIZE:
        tournamentgroups = random.sample(pop,k=2*TOURNAMENT_SIZE)
        g1 = tournamentgroups[:TOURNAMENT_SIZE]
        g2 = tournamentgroups[TOURNAMENT_SIZE:]
        g1.sort(key=lambda a:stratScore[a],reverse=True)
        # print("Candidate 1: ")
        # for cand in g1:
        #     print(cand,stratScore[cand])
        g2.sort(key=lambda a:stratScore[a],reverse=True)
        # print("candidate2: ")
        # for cand2 in g2:
        #     print(cand2,stratScore[cand2])
        # input()
        # after creating the tournament, chose next parents
        index1 = 0
        while index1 < len(g1):
            if random.random() < TOURNAMENT_WIN_PROBABILITY:
                parent1 = g1[index1]
                # print("Winning value: ",index1)
                break
            else:
                index1 += 1
        if index1 == len(g1):
            parent1 = g1[index1-1]
       # print("parent1: ",parent1)
        index2 = 0
        
        while index2 < len(g2):
            if random.random() < TOURNAMENT_WIN_PROBABILITY:
                parent2 = g2[index2]
                # print("Winning value: ",index2)
                break
            else:
                index2 += 1

        if index2 == len(g2):
            parent2 = g2[index2-1]
        # print("parent2: ",parent2)
        # once have the parents, breed
        # input()
        newchild = breed(parent1,parent2)
        if newchild not in nextgen:
            nextgen.add(newchild)
        # input()
    return list(nextgen)

def breed(parent1,parent2):
    """
    Returns child in string form
    """
    lettersInChild = set()
    child = ["" for i in range(26)] # creates a list with indexes at each
    indices = random.sample(range(len(parent1)),CROSSOVER_POINTS)
    # print(indices)
    # print("Indices: ",indices)
    for ind in indices:
        child[ind] = parent1[ind]
        lettersInChild.add(child[ind])
    # put the letters of parent 2 in
    childin:int = 0
    p2ind:int = 0
    while childin < len(child) and p2ind < len(parent2):
        char = parent2[p2ind]
        if char not in lettersInChild:
            if len(child[childin]) == 0:
                child[childin] = char
                lettersInChild.add(child[childin])
                p2ind += 1
                childin += 1
            else:
                childin += 1
        else:
            p2ind += 1
    if random.random() < MUTATION_RATE:
        index1 = random.randint(0,len(child) - 1)
        index2 = random.randint(0,len(child) - 1)
        # print(index1,index2)
        while index2 ==index1:
            
            index2 = random.randint(0,len(child)-1)
        # print(index2,index1)
        child[index1],child[index2] = child[index2],child[index1]
    # input()
    return "".join(child)

# print("breed: ")
# print(breed("ABCDFEG","ACBFEGD"))
parent1 = "BCDAEF"

parent2 = "ABDFEC"
print("Breed: ")
print(parent1, "parent1")
print(parent2, "parent2")
child = breed(parent1,parent2)
print(child)

# run ciphers for 500 generations
message = sys.argv[1]
gen = 0
population = generatePop()
while gen < NUM_GENERATIONS:
    print("Generation ",gen)
    # print(sorted(population))
    population = selection(population,message)
    # input()
    print()
    gen += 1





    





    









    





    



