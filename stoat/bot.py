#!/usr/bin/env python3
import stoat
import sqlite3
import re


class MyClient(stoat.Client):
    __slots__ = ()

    # Regex pattern to match book, chapter, start verse, and optional end verse
    pattern = re.compile(
        r"^(?P<book>\d?\s?[A-Za-z\s]+?)\s+(?P<chapter>\d+):(?P<start_verse>\d+)(?:-(?P<end_verse>\d+))?$"
    )

    async def on_ready(self, event, /):
        print(f'Logged on as {event.me.tag}!')

    async def on_message(self, message, /):

        if message.author_id == self.me.id:
            return

        msg = message.content

        if msg.lower().startswith(".kjv"):

            cite = msg[5:].lower()
            passages=[]

            match = self.pattern.match(cite.strip())
            if match:
                data = match.groupdict()
                
                # Clean up extra spaces and convert numbers to integers
                book = data["book"].strip().lower()
                cnum = int(data["chapter"])
                svnum = int(data["start_verse"])
                
                # Use a ternary operator to handle missing end verses safely
                evnum = int(data["end_verse"]) if data["end_verse"] is not None else svnum

                conn=sqlite3.connect('kjv.db')
                curs=conn.cursor()

                curs.execute(f"""
                    SELECT 
                        b.bnam as BOOK, 
                        v.cnum as CHAPTER, 
                        v.vnum as VERSE, 
                        v.text as TEXT
                    FROM verses v
                    JOIN books b ON v.bnum = b.bnum
                    WHERE LOWER(BOOK)=? and CHAPTER=? and (VERSE >= ? AND VERSE <= ?)
                """,(book,cnum,svnum,evnum))

                rows = curs.fetchall()
                for row in rows:
                    passages.append(f"{row[0]} {row[1]}:{row[2]} -> {row[3]}\n")

                conn.commit()
                conn.close()

            for passage in passages:
                await message.channel.send(passage)

client = MyClient()
client.run('VOrC54ucVlPeTMP-yaOXLgZNw1nR2_Q_WoALY1VegcrfuDxPuq78yoNZv4Jc_Z_u')

