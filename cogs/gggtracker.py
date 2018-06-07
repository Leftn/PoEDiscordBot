

from discord.ext import commands
from database import Database
import gggtrackertimer

class GGGTracker():
    """
    This cog is where things might start getting complicated.
    
    First off. Since bot.run() is a looped thread itself, we cannot create a loop traditionally to listen to gggtracker.com
    Instead, we spawn our own thread and have that run the loop.
    
    The loop class which listens to gggtracker.com is in helpers.py
    
    Look there for more details on how this cog is run
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

        # Start the timer
        self.timer = gggtrackertimer.GGGTrackerListener(self.bot)

    def check_owner(self, ctx):
        owner = ctx.message.server.owner.id
        user = ctx.message.author.id
        if owner == user:
            return True
        else:
            return False

    @commands.command(pass_context=True, help="Allows the bot to send ggg tracked infomation to the current channel")
    async def enable_ggg_tracker(self, ctx):
        if self.check_owner(ctx):
            if self.db.check_server_exists(ctx.message.server):
                self.db.set_server_ggg(ctx.message.server, 1, ctx.message.channel)
            else:
                self.db.add_server(ctx.message.server, ctx.message.channel)
            await self.bot.say("Your server has been successfully been added to the notification list")
        else:
            await self.bot.say("You must be the server owner to use this command")

    @commands.command(pass_context=True, help="Disables the bot from posting ggg tracked information, this removes all channels too")
    async def disable_ggg_tracker(self, ctx):
        if self.check_owner(ctx):
            if self.db.check_server_exists(ctx.message.server):
                self.db.remove_server(ctx.message.server)
                await self.bot.say("Your server has successfully been removed from the notification list")
            else:
                await self.bot.say("The bot isn't registered to post here...")
        else:
            await self.bot.say("You must be the server owner to use this command")




def setup(bot):
    bot.add_cog(GGGTracker(bot))