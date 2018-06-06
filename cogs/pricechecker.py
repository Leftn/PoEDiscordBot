"""
original author: Left
github: https://github.com/Leftn
gitlab: https://gitlab.com/g_
reddit: http://reddit.com/u/Leftn
tracker: af4get6hn3m910ffi4ue92id1efj0a12

If you copy just this file, please do not modify this, i'd like to know how much my code is being used.
"""

import json
import difflib

from discord.ext import commands
from discord.embeds import Embed
import requests
from database import Database

class PriceChecker():
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.command(pass_context=True, help="Pricecheck - Searches poe.ninja for the rough pricing for many items")
    async def pc(self, ctx, *args):
        item = self.titlecase(args)
        message = await self.bot.say(f"Checking poe.ninja for the price of {item}...")
        user = ctx.message.author
        if self.db.check_user_exists(user):
            data = self.pricecheck(item, self.db.get_league(user))
            await self.bot.delete_message(message)
            if data:
                await self.bot.say("*" + data[0].get("name") + "* in **" + data[0].get("league") + "**")
                for element in data:
                    embed = self.create_embed_pricing(element)
                    await self.bot.say(embed=embed)
            else:
                suggested = self.get_suggested_item(item)
                await self.bot.say("Could not find item: {}\nDid you mean:\n{}".format(item, "\n".join(suggested)))
        else:
            await self.bot.delete_message(message)
            await self.bot.say("Your preffered league is not currently set, please use `{}` to set the current league".format(self.bot.command_prefix+"set_league <league>"))


    @commands.command(pass_context=True)
    async def set_league(self, ctx, *args):
        league = " ".join(args)
        if league in self.db.get_league_list():
            user = ctx.message.author
            if self.db.check_user_exists(user):
                self.db.set_league_db(user, league)
            else:
                name = str(user.name)
                self.db.add_user(user, league, name)
            await self.bot.say(f"Successfully set your league to: {league}")
        else:
            await self.bot.say(f"League '{league}' not a playable league (Case sensitive)")
            string_league = "\n".join(self.db.get_league_list()) # Just makes a list of strings to a string seperated by \n
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
        elif item_type == "gem":
            embed.add_field(name="Level", value=data.get("gem_level"))
            embed.add_field(name="Quality", value=data.get("gem_quality"))
            if data.get("gem_corrupted") == 1:
                embed.add_field(name="Corrupted", value="True")
            else:
                embed.add_field(name="Corrupted", value="False")
        elif item_type == "flask":
            if data.get("legacy") == 0:
                embed.add_field(name="Legacy", value="No")
            else:
                embed.add_field(name="Legacy", value="Yes")
        if data.get("image"):
            embed.set_image(url=data.get("image"))
        return embed


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

    def get_suggested_item(self, item):
        all_names = requests.get("http://45.76.116.155/api/v1/names").json()
        return difflib.get_close_matches(item, all_names)


def setup(bot):
    bot.add_cog(PriceChecker(bot))