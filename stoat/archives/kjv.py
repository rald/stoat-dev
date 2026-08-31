#!/usr/bin/env python3
import sqlite3
import xml.etree.ElementTree as ET



conn=sqlite3.connect('kjv.db')
curs=conn.cursor()

curs.execute("DROP TABLE IF EXISTS verses")

curs.execute(
"""
CREATE TABLE `verses` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `bnum` INTEGER,
    `cnum` INTEGER,
    `vnum` INTEGER,
    `text` TEXT
)
""")

tree=ET.parse('kjv.xml')
root=tree.getroot()

for book in root.findall('BIBLEBOOK'):
    for chapter in book.findall('CHAPTER'):
        for verse in chapter.findall('VERS'):

            bnum = book.get('bnumber')
            cnum = chapter.get('cnumber')
            vnum = verse.get('vnumber')
            text = verse.text

            curs.execute("INSERT INTO verses(bnum,cnum,vnum,text) values (?,?,?,?)",(bnum,cnum,vnum,text))

            # print(f"{bname}|{cnumber}|{vnumber}|{text}")

conn.commit()
conn.close()
