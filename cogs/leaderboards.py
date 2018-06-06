from discord.embeds import Embed
from discord.ext import commands
import requests
from database import Database

class Leaderboards():
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.command(pass_context=True, help="Retrieves the top 5 leaderboard rankings of a specified league")
    async def top5(self, ctx):
        league = self.db.get_league(ctx.message.author)
        if league:
                data = self.get_leaderboard(league, 5)
                for player in data:
                    await self.bot.say(embed=self.create_embed(player))
        else:
            await self.bot.say(f"You have not set your league, please set it with `{self.bot.command_prefix}set_league <league>`")

    def create_embed(self, player):
        embed = Embed(colour=0x4f1608)
        embed.add_field(name="Name", value=player.get("name"))
        embed.add_field(name="Rank", value=player.get("rank"))
        embed.add_field(name="\u200b", value="\u200b") # Empty field to make spacing of the object look much nicer
        embed.add_field(name="Level", value=player.get("level"))
        embed.add_field(name="Class", value=player.get("class"))
        embed.add_field(name="Alive", value=str(not player.get("dead")))
        if player.get("twitch"):
            embed.set_author(name=player.get("twitch"), url="https://www.twitch.tv/"+player.get("twitch"), icon_url="https://cdn1.iconfinder.com/data/icons/micon-social-pack/512/twitch-256.png")
        return embed

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
            if x.get("account").get("twitch"):
                d.update({"twitch":x.get("account").get("twitch").get("name")})
            return_list.append(d)
        return return_list

def setup(bot):
    bot.add_cog(Leaderboards(bot))