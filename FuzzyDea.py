import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydea
import sqlite3
inputt=list()
fuzzyop=list()
impfac=list()
lowwwer=dict()
Uppper=dict()
conn = sqlite3.connect('FuzzyDeaAnswer.sqlite')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS DMU1 (Alpha TEXT NOT NULL , LowerEfficiency float , UpperEfficiency float )''')
cur.execute('''
CREATE TABLE IF NOT EXISTS DMU2 (Alpha TEXT NOT NULL , LowerEfficiency float , UpperEfficiency float )''')
cur.execute('''
CREATE TABLE IF NOT EXISTS DMU3 (Alpha TEXT NOT NULL , LowerEfficiency float , UpperEfficiency float )''')

for i in range(3):
    iput=list()
    a=input("How many professor are working in this group: ")
    a = int(a)
    iput.append(a)
    a=input("How many Student are attending to this group: ")
    a = int(a)
    iput.append(a)
    print(iput)
    inputt.append(iput)
print(inputt)
for i in range(3):
    a =input("please type down the H-Index")
    a = int(a)
    impfac.append(a)

for b in range(3):
    khuruji=list()
    for a in range(3):
        point=input("please go for 3 fuzzy points respectively: ")
        point=float(point)
        khuruji.append(point)
    print(khuruji)
    fuzzyop.append(khuruji)
print("The upper and lower are")
print(fuzzyop)
inputs = pd.DataFrame(inputt, columns=['gradnpost', 'prof'])
print("========================================")
for a in range(101):
    print("bara lower")
    alpha =a/100
    print('for alpha=',alpha)
    OP=list()
    for op in fuzzyop:
        lower=op[0]+((op[1]-op[0])*alpha)
        upper=op[2]-((op[2]-op[1])*alpha)
        initOP=(lower,upper)
        OP.append(initOP)
    print("=====================axaxaxaxaxaxaxax")
    final=list()
    for it in range(3):
        n=0
        inpaha=list()
        for goruhha in range(3):
            temp =list()
            if n==it:
                outp=[OP[n][0],impfac[n]]
                temp.append(outp)
            else:
                outp=[OP[n][1],impfac[n]]
                temp.append(outp)
            n=n+1
            inpaha.append(temp[0])
        final.append(inpaha)
    n = 0
    ennficency=list()
    for dmu in final:
        print("bara DMU e",n,"inputha: ",inputt,"\n","va outpute: ",dmu)
        print("===========================================")
        outputs = pd.DataFrame(dmu ,columns=['h-index', 'paper'])
        uni_prob = pydea.DEAProblem(inputs, outputs, returns='CRS')
        myresults = uni_prob.solve()
        print("Lower bond of ennficency of",n,"is",myresults['Efficiency'][n])
        ennficency.append(myresults['Efficiency'][n])
        n= n+1
        print(ennficency)
    for thing in ennficency:
        lowwwer[alpha]=ennficency
print(lowwwer,"@@@@@@@@@@@@@@@@@@@@@")
print("==============================================")
print( "for upper")
for a in range(101):
    alpha =a/100
    OP=list()
    for op in fuzzyop:
        lower=op[0]+((op[1]-op[0])*alpha)
        upper=op[2]-((op[2]-op[1])*alpha)
        initOP=(lower,upper)
        OP.append(initOP)
    print(OP)
    print("=====================")
    final=list()
    for it in range(3):
        n=0
        inpaha=list()
        for goruhha in range(3):
            temp =list()
            if n==it:
                outp=[OP[n][1],impfac[n]]
                temp.append(outp)
            else:
                outp=[OP[n][0],impfac[n]]
                temp.append(outp)
            n=n+1
            inpaha.append(temp[0])
        final.append(inpaha)
    print(final)
    n = 0
    ennficency=list()
    for dmu in final:
        print("bara DMU e",n,"inputha: ",inputt,"\n","va outpute: ",dmu)
        print("===========================================")
        outputs = pd.DataFrame(dmu ,columns=['h-index', 'paper'])
        uni_prob = pydea.DEAProblem(inputs, outputs, returns='CRS')
        myresults = uni_prob.solve()
        print("Lower bond of ennficency of",n,"is",myresults['Efficiency'][n])
        ennficency.append(myresults['Efficiency'][n])
        n= n+1
        print(ennficency)
    for thing in ennficency:
        Uppper[alpha]=ennficency
print(Uppper,"@@@@@@@@@@@@@@@@@@@@@")
for a in range(101):
    b=a/100
    c=str(b)
    cur.execute('''INSERT OR IGNORE INTO DMU1 (alpha,LowerEfficiency,UpperEfficiency)
        VALUES ( ?,?,? )''', (c,lowwwer[b][0] , Uppper[b][0]))
    cur.execute('''INSERT OR IGNORE INTO DMU2 (alpha,LowerEfficiency,UpperEfficiency)
        VALUES ( ?,?,? )''', (c,lowwwer[b][1] , Uppper[b][1]))
    cur.execute('''INSERT OR IGNORE INTO DMU3 (alpha,LowerEfficiency,UpperEfficiency)
        VALUES ( ?,?,? )''', (c,lowwwer[b][2] , Uppper[b][2]))
    conn.commit()
