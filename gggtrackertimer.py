import threading, re
from urllib.parse import urlparse
from html import unescape

import discord
import feedparser, hashlib, asyncio

from database import Database
import config

def clean_html(raw_html):
    """
    Retrieved from: https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
    
    Removes all items with <*> 
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)

    return unescape(cleantext)

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
        self.timer = Timer(config.ggg_tracker_interval, self.track_ggg)
        # We still need the instance of the bot to send messages to our listeners
        self.bot = bot
        self.db = Database()

    def create_tracker_embed(self, item):
        url = item.get('links')[0].get('href')
        embed = discord.Embed(colour=0xff2525, title=item.get('title'), url=url)
        url_parts = urlparse(url)
        embed.add_field(name=url_parts.netloc, value="```"+clean_html(item.get("summary"))+"```")
        embed.set_footer(text=item.get("published"))
        return embed

    async def send(self, items):
        for item in items:
            hash = hashlib.md5()
            hash.update(item.get("links")[0].get("href").encode("utf-8"))
            digest = hash.hexdigest()
            embed = self.create_tracker_embed(item)
            for server in self.db.get_ggg_tracker_server_list():
                if digest not in self.db.get_server_ggg_posts(server[0]):
                    self.db.append_server_ggg_post(server[0], digest)
                    await self.bot.send_message(discord.Object(id=server[1]), embed=embed)

    async def track_ggg(self):
        feed = feedparser.parse("https://gggtracker.com/rss")
        items = feed["items"]
        items.sort(key=lambda x: x.published_parsed, reverse=True)  # Sorts items by date, most recent last
        await self.send(items)
        self.timer = Timer(config.ggg_tracker_interval, self.track_ggg)