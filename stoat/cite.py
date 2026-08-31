#!/usr/bin/env python3

import sqlite3
import re

conn=sqlite3.connect('kjv.db')
curs=conn.cursor()



# Example citation strings
citations = ["John 3:16", "1 Corinthians 13:4-7", "Genesis 1:1"]

# Regex pattern to match book, chapter, start verse, and optional end verse
pattern = re.compile(
    r"^(?P<book>\d?\s?[A-Za-z\s]+?)\s+(?P<chapter>\d+):(?P<start_verse>\d+)(?:-(?P<end_verse>\d+))?$"
)

for citation in citations:
    match = pattern.match(citation.strip())
    if match:
        data = match.groupdict()
        
        # Clean up extra spaces and convert numbers to integers
        bnam = data["book"].strip()
        cnum = int(data["chapter"])
        svnum = int(data["start_verse"])
        
        # Use a ternary operator to handle missing end verses safely
        evnum = int(data["end_verse"]) if data["end_verse"] is not None else None

        curs.execute(f"""
            SELECT 
                v.id, 
                b.bnam, 
                v.cnum, 
                v.vnum, 
                v.text
            FROM verses v
            JOIN books b ON v.bnum = b.bnum
            WHERE book={bnam} and chapter={cnum} and verse={svnum} <= verse={scnum};
        """)

conn.commit()
conn.close()
