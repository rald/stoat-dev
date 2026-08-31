#!/usr/bin/env python3
import stoat
import sqlite3

class MyClient(stoat.Client):
    __slots__ = ()

    async def on_ready(self, event, /):
        print(f'Logged on as {event.me.tag}!')
    async def on_message(self, message, /):

        if message.author_id == self.me.id:
            return

        if message.content == "ping":
            await message.channel.send("pong")
client = MyClient()
client.run('VOrC54ucVlPeTMP-yaOXLgZNw1nR2_Q_WoALY1VegcrfuDxPuq78yoNZv4Jc_Z_u')

