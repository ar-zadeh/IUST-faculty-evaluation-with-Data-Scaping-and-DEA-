import pandas
import re
import urllib.request, urllib.parse, urllib.error
import csv
import json
df = pandas.read_excel('maghale.xlsx')
titles =df['title'].values
plot = df['Abbrev'].values
w = csv.writer(open("means.csv", "w"))
area = list()
n = 0
w.writerow(['title' , "avg_citation", "number of papers"])
for name in plot:
    if n%2 !=0:
        area.append(name)
        n = n+1
    else:
        n = n+1
y =1
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
    url = ("https://api.elsevier.com/content/search/scopus?"
          + urllib.parse.urlencode(
              {'apiKey': '60a9dee56e89f7b453b43162cd6b2dc8', 'query':'SUBJAREA(' + h + ')' , 'Accept':'application/json','view':'COMPLETE' })+ '&field=dc:identifier'+'&date=2015-2016')
    h = 0
    fehrest= list()
    print('Retrieving', url)
    req = urllib.request.Request(url,
    data=None,
    headers={
        'Accept':'application/json'})
    connection = urllib.request.urlopen(req)
    data = connection.read().decode()
    js = json.loads(data)
    headers = dict(connection.getheaders())
    area = list()
    print ("====================================================")
    for r in js['search-results']["entry"]:
        fehrest.append(r['dc:identifier'])
    print('Remaining:', headers['X-RateLimit-Remaining'])
    for maghale in fehrest:
        url = ("http://api.elsevier.com/content/abstract/scopus_id/"
              + maghale
              + "?field=title,"+ "view=FULL,"
              + "prism:coverDate,subject-area,citedby-count,prism:aggregationType,")

        print('Retrieving', url)
        req = urllib.request.Request(url,
        data=None,
        headers={
            'Accept':'application/json',
                                 'X-ELS-APIKey': '60a9dee56e89f7b453b43162cd6b2dc8'})
        connection = urllib.request.urlopen(req)
        data = connection.read().decode()
        js = json.loads(data)
        headers = dict(connection.getheaders())
        area = list()
        code = list()
        abbrev = list()
        print ("====================================================")
        print(js)
        print ("====================================================")
        if int(js['abstracts-retrieval-response']['coredata']['prism:coverDate'][:4])>=2016:
            tarikh =js['abstracts-retrieval-response']['coredata']['prism:coverDate'][:4]
            cited =int( js['abstracts-retrieval-response']['coredata']['citedby-count'])
            subject =js['abstracts-retrieval-response']['coredata']['dc:title']
            print("==================================")
            print(abbrev)
            print("==================================")
            print(cited)
            print("==================================")
            print(subject)
            print("================================================================================================")
            h = cited + h
            y = y+2
            print(y)
        mean_of_citation = (h/len(fehrest))
        count = len(fehrest)
        w.writerow([titles[y] , mean_of_citation, count])
