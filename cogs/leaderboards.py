from discord.ext import commands
import requests

import helpers

class Leaderboards():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def top10(self, *args):
        if args:
            if args[0] in self.get_league_list():
                data = self.get_leaderboard(args[0], 10)
        else:
            await self.bot.say("You must specify a league to search")

    def create_embed(self, data):
        pass

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

    def get_leaderboard(self, league, limit=10):
        url = f"http://api.pathofexile.com/ladders/{league}?limit={limit}"
        r = requests.get(url).json().get("entries")
        return_list = []
        for x in r:
            d = {
                    "rank":x.get("rank"),
                    "name":x.get("character").get("name"),
                    "level":x.get("character").get("level"),
                    "class":x.get("character").get("class"),
                    "dead":x.get("dead")
                }
            if x.get("twitch"):
                d.update({"twitch":x.get("twitch").get("name")})
            return_list.append(d)
        return return_list

def setup(bot):
    bot.add_cog(Leaderboards(bot))