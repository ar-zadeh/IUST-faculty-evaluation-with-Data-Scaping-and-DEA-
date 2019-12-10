import csv
import pandas
import re

df = pandas.read_excel('maghale.xlsx')
w = csv.writer(open("compelete nis.csv", "w"))
area_of_inrtest = df["AOI"].values
names = df["professor's surename"].values
title = df["title"].values
citation = df["citation"].values
area = df["SUBS"].values
w.writerow(["AOI" , "professor's surename", "title", "citation", "Sub-areas"])
temp = list()
n=0
for hoze in area:
    if n%2==1:
        areas = hoze.split("'")
        for subs in areas:
            if len(subs)<=2:
                continue
            else:
                temp.append(subs)
        n=n+1
    else:
        n=n+1
main=list()
for members in temp:
    if members not in main:
        main.append(members)
print(main)
