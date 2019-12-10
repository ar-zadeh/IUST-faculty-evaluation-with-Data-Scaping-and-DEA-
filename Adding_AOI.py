import csv
import pandas

df = pandas.read_excel('asatid.xlsx')
df1 = pandas.read_excel('maghale.xlsx')
w = csv.writer(open("compelete.csv", "w"))
names = df["professor's surename"].values
major = df['AOI'].values
asatid = df1["professor's surename"].values
w.writerow([ "professor's surename", "AOI"])
temp = list()
for name in names:
    if name not in temp:
        temp.append(name)
for ostad in asatid:
    n = 0
    for prof in temp:
        if prof == ostad:
            w.writerow([ ostad, major[n]])
        else:
            n = n+1
print(temp)
