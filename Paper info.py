import re
import urllib.request, urllib.parse, urllib.error
import json
import pandas
import sqlite3
conn = sqlite3.connect('poroje1.sqlite')
cur = conn.cursor()
cur.execute('SELECT ID FROM Article')
papers=cur.fetchall()
cur.execute('CREATE TABLE IF NOT EXISTS Journal (ID INTEGER NOT NULL PRIMARY KEY UNIQUE,Name text,CITESCORE text);')
cur.execute('CREATE TABLE IF NOT EXISTS connection( Article_ID integer,Journal_ID INTEGER);')
cur.execute('CREATE TABLE IF NOT EXISTS conferance( ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,name text);')
for maghale in papers:
    cur.execute('SELECT * FROM connection WHERE Article_ID = ?',(maghale[0], ))
    conc=cur.fetchall()
    if len(conc)!=0:
        print(conc[0],"exists")
        continue
    url = ("http://api.elsevier.com/content/abstract/scopus_id/"
          + str(maghale[0])
          + "?field=title,"+ "view=FULL,"
          + "prism:coverDate,prism:publicationName,prism:issn,subject-area,citedby-count,subtypeDescription,prism:aggregationType,")

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
    issn = list()
    print(js)
    try:
        x =js['abstracts-retrieval-response']['coredata']['prism:issn']
        r = x
        y=js['abstracts-retrieval-response']['coredata']['prism:publicationName']
        w=1
    except:
        confname=js['abstracts-retrieval-response']['coredata']['prism:publicationName']
        w=0
    if w==1:
        x = x.split()
        r = r.split()
        z =  x[0]
        x = x[0]
        print (y)
        print(z)
        if z[len(z)-1]=='X':
            z= z[:len(z)-1]
            print("=====",z)
        cur.execute('''INSERT OR IGNORE INTO connection (Article_ID,Journal_ID)
            VALUES ( ?,? )''', (maghale[0],int(z)) )
        print ("====================================================")
        cur.execute('SELECT ID FROM Journal WHERE ID = ?',(z, ))
        majale=cur.fetchall()
        if len(majale)!=0:
            print("the",y,"is already in datacentre")
            continue
        else:
            try:
                url = ("https://api.elsevier.com/content/serial/title/issn/"+x+"?"
                    +urllib.parse.urlencode({'httpAccept':'application/json'})
                    + "&view=CITESCORE"
                    )
                print('Retrieving', url)
                req = urllib.request.Request(url,
                data=None,
                headers={
                         'X-ELS-APIKey': '60a9dee56e89f7b453b43162cd6b2dc8'})
                connection = urllib.request.urlopen(req)
            except:
                r=r[len(r)-1]
                url = ("https://api.elsevier.com/content/serial/title/issn/"+r+"?"
                    +urllib.parse.urlencode({'httpAccept':'application/json'})
                    + "&view=CITESCORE"
                    )

            print('Retrieving', url)
            req = urllib.request.Request(url,
            data=None,
            headers={
                 'X-ELS-APIKey': '60a9dee56e89f7b453b43162cd6b2dc8'})
            connection = urllib.request.urlopen(req)
            data = connection.read().decode()
            js = json.loads(data)
            headers = dict(connection.getheaders())
            CS=js['serial-metadata-response']['entry'][0]['citeScoreYearInfoList']['citeScoreCurrentMetric']
            print(CS)
            cur.execute('''INSERT OR IGNORE INTO Journal (ID,Name,CITESCORE)
                VALUES ( ?,?,? )''', (int(z),y,CS ) )
    else:
        cur.execute('SELECT name FROM conferance WHERE name = ?',(confname, ))
        con=cur.fetchall()
        if len(con)==0:
            cur.execute('''INSERT OR IGNORE INTO conferance (name)
                        VALUES ( ?)''', (confname, ))
            cur.execute('''SELECT ID FROM conferance WHERE name=?''',(confname,))
            idC=cur.fetchone()[0]
            cur.execute('''INSERT OR IGNORE INTO connection (Article_ID,Journal_ID)
                        VALUES ( ?,? )''', (maghale[0],idC) )
        else:
            print(confname,"is already in database")
        print ("====================================================")

    conn.commit()
