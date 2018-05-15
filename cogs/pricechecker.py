"""
original author: Left
github: https://github.com/Leftn
gitlab: https://gitlab.com/g_
reddit: http://reddit.com/u/Leftn
tracker: af4get6hn3m910ffi4ue92id1efj0a12

If you copy just this file, please do not modify this, i'd like to know how much my code is being used.
"""

import json
import os
import sqlite3

from discord.ext import commands
from discord.embeds import Embed
import requests

class Database():
    def __init__(self, dbname=os.path.join("db", "database.db")):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname, check_same_thread=False)
        self.conn.text_factory = str

    def connection(self, dbname):
        conn = sqlite3.connect(dbname)
        return conn

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def create_tables(self):
        cursor = self.cursor()
        sql = """
        DROP TABLE IF EXISTS server;

        CREATE TABLE user
        (
            user_id integer PRIMARY KEY AUTOINCREMENT,
            user_name text,
            user_league text
        );
        """
        cursor.executescript(sql)
        self.commit()


class PriceChecker():
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.command(pass_context=True, help="Pricecheck - Searches poe.ninja for the rough pricing for many items")
    async def pc(self, ctx, *args):
        item = self.titlecase(args)
        message = await self.bot.say(f"Checking poe.ninja for the price of {item}...")
        user = str(ctx.message.author.id)
        if self.check_user_exists(user):
            data = self.pricecheck(item, self.get_league(user))
            await self.bot.delete_message(message)
            if data:
                await self.bot.say("*" + data[0].get("name") + "* in **" + data[0].get("league") + "**")
                for element in data:
                    embed = self.create_embed_pricing(element)
                    await self.bot.say(embed=embed)
            else:
                await self.bot.say(f"Could not find item: {item}")
        else:
            await self.bot.delete_message(message)
            await self.bot.say("Your preffered league is not currently set, please use `{}` to set the current league".format(self.bot.command_prefix+"set_league"))


    @commands.command(pass_context=True)
    async def set_league(self, ctx, *args):
        league = " ".join(args)
        if league in self.get_league_list():
            user = str(ctx.message.author.id)
            if self.check_user_exists(user):
                self.set_league_db(user, league)
            else:
                name = str(ctx.message.author.name)
                self.add_user(user, league, name)
            await self.bot.say(f"Successfully set your league to: {league}")
        else:
            await self.bot.say(f"League '{league}' not a playable league (Case sensitive)")
            string_league = "\n".join(self.get_league_list()) # Just makes a list of strings to a string seperated by \n
            await self.bot.say(f"Here is the full list of leagues:\n`{string_league}`")

    def pricecheck(self, item, league):
        """

        :param item: String: a titlecased name of the item to search for
        :param league: String: The specified league to search, must also be titlecased
        :return: 
        """
        data = {"league": league, "name": item}
        headers = {"Content-Type": "application/json"}
        # The server is an API of my own making, I haven't bothered writing documentation/creating a domain name yet
        # The server is in pre-pre-alpha and only this part of the site works
        data = requests.post("http://45.76.116.155/api/v1/get", data=json.dumps(data), headers=headers).json()
        if isinstance(data, dict) and data.get("error"):
            return None
        else:
            return data

    def create_embed_pricing(self, data):
        """
        Creates a discord embed object and adds the nesscary fields to the embed object depending on what type it is
        
        It also adds the image link to the embed if it exists
        
        :param data: dict: Must contain the field "type", everything else depends on what type it is
        :return: discord.embeds.Embed
        """
        embed = Embed(colour=0x4f1608)
        item_type = data.get("type")
        if item_type != "currency":
            embed.add_field(name="Chaos", value=data.get("chaos"))
            embed.add_field(name="Exalted", value=data.get("exalted"))
        else:
            embed.add_field(name=f"Pay (x {data.get('name')} gets you 1 Chaos", value=data.get("pay"))
            embed.add_field(name=f"Recieve (One {data.get('name')} gets x Chaos)", value=data.get("recieve"))
        if item_type in ["armour", "weapon"]:
            embed.add_field(name="Links", value=data.get("links"))
            if data.get("legacy") == 0:
                embed.add_field(name="Legacy", value="No")
            else:
                embed.add_field(name="Legacy", value="Yes")
        elif item_type == "map":
            embed.add_field(name="Tier", value=data.get("tier"))
            embed.add_field(name="Atlas", value=data.get("atlas"))
        if item_type != "currency":
            embed.set_image(url=data.get("image"))
        return embed

    def set_league_db(self, server, league):
        sql = "UPDATE user SET user_league = ? WHERE user_id = ?"
        self.db.cursor().execute(sql, (league, server))
        self.db.commit()

    def add_user(self, user, league="Standard", name=""):
        sql = "INSERT INTO user(user_id, user_league, user_name) VALUES (?, ?, ?)"
        self.db.cursor().execute(sql, (user, league, name))
        self.db.commit()

    def get_league(self, user):
        sql = "SELECT user_league FROM user WHERE user_id = ?"
        cursor = self.db.cursor()
        cursor.execute(sql, (user,))
        data = cursor.fetchone()
        if data:
            return data[0]
        else:
            return None

    def check_user_exists(self, user):
        sql = "SELECT * FROM user WHERE user_id = ?"
        cursor = self.db.cursor()
        cursor.execute(sql, (user,))
        data = cursor.fetchone()
        if data:
            return True
        else:
            return False

    def get_league_list(self):
        # This is a static method, but I am unsure which scope is best to place this method, so for now, it stays here
        """
        This gets a list of leagues from the official site api
        
        :return: list of strings
        """
        url = "http://www.pathofexile.com/api/trade/data/leagues"
        r = requests.get(url).json()
        if r.get("result"):
            return [x.get("id") for x in r.get("result")]
        else:
            return []

    def titlecase(self, tp):
        # Converts a tuple of strings to titlecasing (Each string should be 1 word)
        # e.g. hand of wisdom and action --> Hand of Wisdom and Action
        tp = [x.lower() for x in tp]  # Convert to list so we can do reassignment
        for i in range(len(tp)):
            if i == 0 or tp[i] not in ["of", "and", "the", "to", "at", "for"]:
                tp[i] = tp[i][0].upper() + tp[i][1:]
            else:
                continue
        return " ".join(tp)

def setup(bot):
    bot.add_cog(PriceChecker(bot))

if __name__ == "__main__":
    # We want to create the database directory in the top level
    path = os.path.join("..","db", "database.db")
    try:
        db = Database(path)
    except sqlite3.OperationalError:
        os.mkdir(os.path.join("..", "db"))
        db = Database(path)
    db.create_tables()