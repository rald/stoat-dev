#!/usr/bin/env python3

import sqlite3
import xml.etree.ElementTree as ET

conn=sqlite3.connect('kjv.db')
curs=conn.cursor()

curs.execute("DROP TABLE IF EXISTS books")

curs.execute(
"""
CREATE TABLE `books` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `bnum` INTEGER,
    `bnam` TEXT,
    `bsnm` TEXT
)
""")

tree=ET.parse('kjv.xml')
root=tree.getroot()

for book in root.findall('BIBLEBOOK'):

    bnum = book.get('bnumber')
    bnam = book.get('bname')
    bsnm = book.get('bsname')

    curs.execute("INSERT INTO books(bnum,bnam,bsnm) values (?,?,?)",(bnum,bnam,bsnm))

conn.commit()
conn.close()
