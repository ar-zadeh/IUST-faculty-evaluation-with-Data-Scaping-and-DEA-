import pandas
import re
import urllib.request, urllib.parse, urllib.error
import csv
import json
df = pandas.read_excel('maghale.xlsx')
plot = df['Abbrev'].values
area = list()
n = 0
for name in plot:
    if n%2 !=0:
        area.append(name)
        n = n+1
    else:
        n = n+1
for line in area:
    h=""
    codes = line.split(',')
    for member in codes:
        temp =member[1:len(member)-1]
        if temp[0] !="'"  :
            mov = temp
        else:
            mov = temp[1:]
        h= h + mov +","
    print(h)
