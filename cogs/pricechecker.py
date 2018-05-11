import json

from discord.ext import commands
from discord.embeds import Embed
import requests

import helpers
import config

class PriceChecker():
    def __init__(self, bot):
        self.bot = bot
        self.league = {}

    @commands.command(pass_context=True)
    async def pc(self, ctx, *args):
        item = helpers.titlecase(args)
        message = await self.bot.say(f"Checking poe.ninja for the price of {item}...")
        if self.league.get(ctx.message.server):
            data = self.pricecheck(item, self.league.get(ctx.message.server))
            await self.bot.delete_message(message)
            if data:
                for element in data:
                    embed = self.create_embed_pricing(element)
                    await self.bot.say(embed=embed)
            else:
                await self.bot.say(f"Could not find item: {item}")
        else:
            await self.bot.delete_message(message)
            await self.bot.say("No league is currently set, please use `{}` to set the current league".format(self.bot.command_prefix+"set_league"))


    @commands.command(pass_context=True)
    async def set_league(self, ctx, *args):  # TODO: Determine if this command should be protected
        name = helpers.titlecase(args)
        if name in config.leagues:
            server = ctx.message.server
            self.league[server] = name
            await self.bot.say(f"Successfully set default league to: {name}")
        else:
            await self.bot.say(f"League '{name}' not a playable league")

    def pricecheck(self, item, league):
        """

        :param item: String: a titlecased name of the item to search for
        :param league: String: The specified league to search
        :return: 
        """
        data = {"league": league, "name": item}
        headers = {"Content-Type": "application/json"}
        # The server is an API of my own making, I havn't bothered writing documentation/creating a domain name yet
        # The server is in pre-pre-alpha and only this part of the site works
        data = requests.post("http://45.76.116.155/api/v1/get", data=json.dumps(data), headers=headers).json()
        if isinstance(data, dict) and data.get("error"):
            return None
        else:
            return data

    def create_embed_pricing(self, data):
        embed = Embed(colour=0x4f1608, title=data.get("name"))
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

def setup(bot):
    bot.add_cog(PriceChecker(bot))