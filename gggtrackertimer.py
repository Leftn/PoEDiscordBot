import threading, re

import discord
import feedparser, hashlib, asyncio

from database import Database

def clean_html(raw_html):
    """
    Retrieved from: https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
    
    Removes all items with <*> 
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

class Timer:
    """
    We need a timer class which is asynchronous, retrieved from: https://stackoverflow.com/questions/45419723/python-timer-with-asyncio-coroutine
    """
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()

class GGGTrackerListener(threading.Thread):
    """
    So, the idea is that we need to run a loop asynchronously to the existing bot loop.

    Threading is the way to solve this. First: Create the thead object with thread = GGGTrackerListener()
    Next, each loop iteration, we query gggtracker.com/rss for the most recent news article
    Then we check each server to see if it has already recieved the notification, if it has, we send the message.

    """

    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.keep_running = True
        self.timer = Timer(5, self.track_ggg)
        # We still need the instance of the bot to send messages to our listeners
        self.bot = bot

    def create_tracker_embed(self, item):
        embed = discord.Embed(colour=0xff2525)
        embed.add_field(name="Summary", value="```"+clean_html(item.get("summary"))+"```")
        embed.set_footer(text=item.get("published"))
        embed.set_author(name=item.get("title"), url=item.get("links")[0].get("href"))
        return embed

    async def send(self, item):
        db = Database()
        sql = "SELECT server_id, server_channel FROM server WHERE server_track_ggg = 1 AND server_most_recent_item_id IS NOT ?"
        cursor = db.cursor()
        hash = hashlib.md5()
        hash.update(item.get("links")[0].get("href").encode("utf-8"))
        digest = hash.hexdigest()
        cursor.execute(sql, (digest, ))
        data = cursor.fetchall()
        embed = self.create_tracker_embed(item)
        for server in data:
            sql = "UPDATE server SET server_most_recent_item_id = ?"
            cursor.execute(sql, (digest,))
            await self.bot.send_message(discord.Object(id=server[1]), embed=embed)
        db.commit()


    async def track_ggg(self):
        feed = feedparser.parse("https://gggtracker.com/rss")
        items = feed["items"]
        items.sort(key=lambda x: x.published_parsed, reverse=True)  # Sorts items by date, most recent first
        await self.send(items[0])
        self.timer = Timer(5, self.track_ggg)