import re
import urllib.request, urllib.parse, urllib.error
import json
import pandas
import sqlite3

df = pandas.read_excel('book1.xlsx')
conn = sqlite3.connect('poroje.sqlite')
cur = conn.cursor()

cur.executescript('''

CREATE TABLE IF NOT EXISTS professor (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,Name text, Surname text , AOI_ID integer);
CREATE TABLE IF NOT EXISTS AOI (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, NameOfArea TEXT UNIQUE);
CREATE TABLE IF NOT EXISTS AuthorAC (AU_ID INTEGER NOT NULL PRIMARY KEY UNIQUE, H_INDEX INTEGER, CitationCount INTEGER, documentCount INTEGER,Professor_ID INTEGER);
CREATE TABLE IF NOT EXISTS Subject (ID INTEGER NOT NULL PRIMARY KEY UNIQUE, SubName TEXT , Abbrev TEXT );
CREATE TABLE IF NOT EXISTS RelatedSubjects (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE ,Subject_ID INTEGER NOT NULL , Article_ID INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS Article (ID INTEGER NOT NULL PRIMARY KEY UNIQUE, title TEXT ,Citation INTEGER, Type INTEGER,tarikh INTEGER);
CREATE TABLE IF NOT EXISTS RA (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE ,Article_ID_1 INTEGER NOT NULL , Article_ID_0 INTEGER NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS Possession (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE ,Author_ID INTEGER NOT NULL, Article_ID INTEGER NOT NULL);
''')
hindex = df['h-index'].values
authorsid = df['Scopus_ID'].values
doc = df['document_count'].values
cite =df['citation'].values
names=df['professors name'].values
surnames=df['professors surename'].values
AOI =df['AOI'].values

for n in range(len(hindex)):
    cur.execute('''INSERT OR IGNORE INTO AOI (NameOfArea)
        VALUES ( ? )''', ( AOI[n], ) )
    cur.execute('SELECT id FROM AOI WHERE NameOfArea = ?',(AOI[n], ))
    AOI_ID =cur.fetchone()[0]
    cur.execute('''INSERT OR IGNORE INTO professor (Name,Surname,AOI_ID)
        VALUES ( ?,?,? )''', (names[n],surnames[n],AOI_ID, ) )
    cur.execute('SELECT id FROM professor WHERE Surname = ?',(surnames[n], ))
    Professor_ID=cur.fetchone()[0]
    cur.execute('''INSERT OR IGNORE INTO AuthorAC (AU_ID ,H_INDEX,CitationCount,documentCount,Professor_ID)
        VALUES(?,?,?,?,?)''',(int(authorsid[n]),int(hindex[n]),int(cite[n]),int(doc[n]),int(Professor_ID)))

conn.commit()
for ID in authorsid:
    ID = str(ID)
    fehrest= list()
    SCOPUS_URL = 'http://api.elsevier.com/content/search/scopus?'
    for year in ("2015-2016",'2016-2017','2017-2018'):
        n =1
        url = SCOPUS_URL + urllib.parse.urlencode(
            {'apiKey': '60a9dee56e89f7b453b43162cd6b2dc8', 'query':'AU-ID(' + ID +')' , 'Accept':'application/json' })+ '&field=dc:identifier'+'&date='
        connection = urllib.request.urlopen(url)
        data = connection.read().decode()
        js = json.loads(data)
        headers = dict(connection.getheaders())
        print("=========")
        try:
            print(js['search-results']["entry"][0]['dc:identifier'])
        except:
            print(js)
            continue
        print ("====================================================")
        cur.execute('SELECT Article_ID FROM Possession WHERE AUTHOR_ID = ?',(ID, ))
        AR_ID=cur.fetchall()
        lis =list()
        for AR in AR_ID:
            lis.append(AR[0])
        print(lis)
        for r in js['search-results']["entry"]:
            if r['dc:identifier'] not in lis:
                print("wwwwwww")
                fehrest.append(r['dc:identifier'])
            else:
                print(r['dc:identifier'], "is already counted")
                n=0
                break
        if n==0:
            print("bud")
            continue
        print('Remaining:', headers['X-RateLimit-Remaining'])
        for maghale in fehrest:
            paper =  int(maghale[10:])
            cur.execute('SELECT * FROM Possession WHERE (AUTHOR_ID,Article_ID)=(?,?)' , (ID,paper))
            Check=cur.fetchall()
            if len(Check)>0:
                print("ghablan bude")
                continue
            cur = conn.cursor()
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
            area = list()
            code = list()
            abbrev = list()
            print ("====================================================")
            print(js['abstracts-retrieval-response']['coredata']['prism:coverDate'][:4])
            print ("====================================================")
            if int(js['abstracts-retrieval-response']['coredata']['prism:coverDate'][:4])>=2016:
                tarikh =js['abstracts-retrieval-response']['coredata']['prism:coverDate'][:4]
                cited = js['abstracts-retrieval-response']['coredata']['citedby-count']
                subject =js['abstracts-retrieval-response']['coredata']['dc:title']
                type(maghale)
                cur.execute('''INSERT OR IGNORE INTO Article (ID ,title,citation,tarikh)
                    VALUES ( ?,?,?,? )''', (paper,subject,int(cited), int(tarikh)) )
                cur.execute('UPDATE Article SET Type=1 WHERE ID = ?', (paper, ))
                cur.execute('''INSERT OR IGNORE INTO Possession (Author_ID,Article_ID)
                    VALUES ( ?,? )''', (int(ID),paper) )
                for areas in js['abstracts-retrieval-response']['subject-areas']['subject-area']:
                    cur.execute('''INSERT OR IGNORE INTO subject (SubName,Abbrev,ID)
                        VALUES ( ?,?,? )''', ( areas['$'], areas['@abbrev'],int( areas['@code']) ) )
                cur.execute('''INSERT OR IGNORE INTO RelatedSubjects(Article_ID,Subject_ID)
                    VALUES ( ?,? )''', (int( ID),paper), )
            else:
                break
            conn.commit()
