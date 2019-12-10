from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3
conn = sqlite3.connect('poroje1.sqlite')
cur = conn.cursor()
browser = webdriver.Chrome()
cur.execute('''
CREATE TABLE IF NOT EXISTS FieldWeightedCitationImpact  (Impact TEXT NOT NULL ,Article_ID INTEGER)
''')
cur.execute('SELECT id FROM Article' )
AOI_ID =cur.fetchall()

for ID in AOI_ID:
    CODE = str(ID[0])
    cur.execute('SELECT * FROM FieldWeightedCitationImpact WHERE Article_ID=(?)',(ID[0],))
    impFac =cur.fetchall()
    if len(impFac)>0:
        print(impFac, "has been retrived")
        continue
    url = 'https://www.scopus.com/record/display.uri?eid=2-s2.0-'+CODE+'&origin=resultslist&sort=plf-f&src=s&sid=b2c8caf10f5e5ac6ea5e8e0a360f4807&sot=autdocs&sdt=autdocs&sl=17&s=AU-ID%286701386322%29&relpos=9&citeCnt=7&searchTerm='
    browser.get(url)
    #try:
    content = browser.find_element_by_xpath("//div[@id='fwciValue']")
    #except:
    #    time.sleep(10)
    #    continue

    element_text = content.text
    print(element_text)
    cur.execute('''INSERT OR IGNORE INTO FieldWeightedCitationImpact (Impact,Article_ID)
        VALUES ( ?,? )''', (element_text,ID[0]))
    time.sleep(10)
    conn.commit()
