#!/usr/bin/env python3

import sqlite3
import re

conn=sqlite3.connect('kjv.db')
curs=conn.cursor()



# Example citation strings
citations = ["John 3:16"]

# Regex pattern to match book, chapter, start verse, and optional end verse
pattern = re.compile(
    r"^(?P<book>\d?\s?[A-Za-z\s]+?)\s+(?P<chapter>\d+):(?P<start_verse>\d+)(?:-(?P<end_verse>\d+))?$"
)

for citation in citations:
    match = pattern.match(citation.strip())
    if match:
        data = match.groupdict()
        
        # Clean up extra spaces and convert numbers to integers
        book = data["book"].strip()
        cnum = int(data["chapter"])
        svnum = int(data["start_verse"])
        
        # Use a ternary operator to handle missing end verses safely
        evnum = int(data["end_verse"]) if data["end_verse"] is not None else svnum

        curs.execute(f"""
            SELECT 
                b.bnam as BOOK, 
                v.cnum as CHAPTER, 
                v.vnum as VERSE, 
                v.text as TEXT
            FROM verses v
            JOIN books b ON v.bnum = b.bnum
            WHERE BOOK=? and CHAPTER=? and (VERSE >= ? AND VERSE <= ?)
        """,(book,cnum,svnum,evnum))

        rows = curs.fetchall()

        for row in rows:
            print(f"{row[0]} {row[1]}:{row[2]} -> {row[3]}\n")

conn.commit()
conn.close()
