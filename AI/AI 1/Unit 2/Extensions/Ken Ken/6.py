import sys,random,math
from collections import Counter

#kenken

N=0
conssets=dict()
symbol_set=set()
con=""

def formboard(lis): # board is list of numbers
    global N,conssets,symbol_set,con
    cons=lis[0]
    boardb=[0 for i in range(len(cons))]
    N=int(len(boardb)**0.5)
    symbol_set=set(range(1,N+1))
    for i in lis[1:]:
        a=i.split()
        conssets[a[0]]=(a[2],int(a[1]),set())
    for i in range(len(cons)):
        conssets[cons[i]][2].add(i)
    con=cons
    return boardb

def printb(b):
    for i in range(N):
        print(b[i*N:(i+1)*N])

def countsym(b):
    a=dict()
    for i in symbol_set:
        if i not in a:
            a[i]=0
    for i in b:
        if i in symbol_set:
            a[i]+=1
    return a

def goal_test(st):
    if 0 in st:
        return False
    s=countsym(st)
    for i in s:
        if s[i]!=N:
            return False # make sure correct number of each number in board
    for i in conssets:
        if conssets[i][0]=="+":
            tot=0
            for j in conssets[i][2]:
                tot+=st[j]
            if tot!=conssets[i][1]:
                return False
        elif conssets[i][0]=="x":
            tot=1
            for j in conssets[i][2]:
                tot*=st[j]
            if tot!=conssets[i][1]:
                return False
        elif conssets[i][0]=="-":
            a,b=conssets[i][2]
            tot=max(st[a],st[b])-min(st[a],st[b])
            if tot!=conssets[i][1]:
                return False
        else:
            a,b=conssets[i][2]
            tot=max(st[a],st[b])/min(st[a],st[b])
            if tot!=conssets[i][1]:
                return False
    return True

def next_unassi(st): # find empty space in cons set with highest proportion solved(without being unsolved)
    for i in range(len(st)):
        if st[i]==0:
            return i
    return -1

def newst(s,val,var):
    b=s.copy()
    b[var]=val
    return b

def suitable(nval,var,st):
    c=con[var]
    cset=conssets[c]
    func=cset[0]
    goal=cset[1]
    empty=0
    for i in cset[2]:
        if st[i]==0:
            empty+=1
    if empty==1:
        if func=="+":
            tot=nval
            for j in cset[2]:
                tot+=st[j]
            if tot!=goal:
                return False
        elif func=="x":
            tot=nval
            for j in cset[2]:
                if st[j]!=0:
                    tot*=st[j]
            if tot!=goal:
                return False
        elif func=="-":
            (c,d)=cset[2]
            if c==var:
                c=d
            tot=max(nval,st[c])-min(nval,st[c])
            if tot!=goal:
                return False
        else:
            (c,d)=cset[2]
            if c==var:
                c=d
            tot=max(nval,st[c])/min(nval,st[c])
            if tot!=goal:
                return False
    return True

def getval(st,va):
    #find a value not in the row or column and fitting regarding the constraint set
    if va!=-1:
        res=set()
        all=set()
        batch=set()
        for i in range(N):
            if st[va//N*N+i] in symbol_set:
                res.add(st[va//N*N+i])
            if st[va%N+i*N] in symbol_set:
                res.add(st[va%N+i*N])
        for i in symbol_set:
            if i not in res:
                all.add(i)
        for i in all:
            if suitable(i,va,st):
                batch.add(i)
        return batch
    return set()

def csp_backtracking(state):
    if goal_test(state): 
        return state
    var = next_unassi(state)
    for val in getval(state, var):
        new_state = newst(state,val,var)
        result = csp_backtracking(new_state)
        if result != None:
            return result
    return None

with open(sys.argv[1]) as f:
    l=[line.strip() for line in f]

b=formboard(l)
# print(conssets)
# printb(con)
# printb(b)
sol=csp_backtracking(b)
print(''.join([str(x) for x in sol]))
# printb(sol)