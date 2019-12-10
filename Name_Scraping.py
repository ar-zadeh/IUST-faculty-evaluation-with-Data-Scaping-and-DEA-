import sqlite3
import urllib.request, urllib.parse, urllib.error
import re

conn = sqlite3.connect('poroje.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS AOI;
DROP TABLE IF EXISTS professor;
CREATE TABLE professor (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,Surname text , AOI_ID integer);
CREATE TABLE AOI (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, NameOfArea TEXT);
''')
asatid =list()
n= 0
fhand = urllib.request.urlopen('http://ie.iust.ac.ir/page/5518/Faculty-members')
for lines in fhand:
    name =lines.decode().strip()
    y = re.findall('Dr.(.*?)<' , name)
    x = re.findall('Msc.(.*?)<' , name)
    if  len(y) != 0:
        if re.search('^ .*' ,y[0]):
            y = y[0][1:]
            asatid.append(y)
        else:
            asatid.append(y[0])

        n= n+1
    elif len(x) != 0:
        if re.search('^ .*' ,x[0]):
            x = x[0][1:]
            asatid.append(x)
        else:
            asatid.append(x[0])
wk = ('Productivity Management', 'System Engineering', 'Industrial Engineering' )
for reshte in wk:
    cur.execute('''INSERT OR IGNORE INTO AOI (NameOfArea)
        VALUES ( ? )''', ( reshte, ) )
    print(reshte)
    cur.execute('SELECT id FROM AOI WHERE NameOfArea = ?',(reshte, ))
    AOI_ID =cur.fetchone()[0]
    conn.commit()
for ostad in asatid[:12]:
    cur.execute('''INSERT OR IGNORE INTO professor (surname, AOI_ID)
        VALUES ( ?, ? )''', ( ostad, 3 ) )
for ostad in asatid[12:27]:
    cur.execute('''INSERT OR IGNORE INTO professor (surname, AOI_ID)
        VALUES ( ?, ? )''', ( ostad, 2 ) )
for ostad in asatid[27:]:
    cur.execute('''INSERT OR IGNORE INTO professor (surname, AOI_ID)
        VALUES ( ?, ? )''', ( ostad, 1 ) )
conn.commit()
