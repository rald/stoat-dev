#!/usr/bin/env python3

import re

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
        data["book"] = data["book"].strip()
        data["chapter"] = int(data["chapter"])
        data["start_verse"] = int(data["start_verse"])
        
        # Use a ternary operator to handle missing end verses safely
        data["end_verse"] = int(data["end_verse"]) if data["end_verse"] is not None else None

        print(data)
