from discord.ext import commands
from database import Database
import gggtrackertimer


class GGGTracker():
    """
    This cog is where things might start getting complicated.
    
    First off. Since bot.run() is a looped thread itself, we cannot create a loop traditionally to listen to gggtracker.com
    Instead, we spawn our own thread and have that run the loop.
    
    The loop class which listens to gggtracker.com is in gggtrackertimer.py
    
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

    @commands.command(pass_context=True, help="Enable/Disable certain parts of the ggg tracker\nList of avaliable arguments:\n    -poe\n    -reddit")
    async def toggle_ggg_source(self, ctx, *args):
        """
        We use bitflags to store the data
        1<<0 = 1: reddit
        1<<1 = 2: poe
        1<<2 = 4: twitter
        """
        if self.check_owner(ctx):
            if args[0] == "reddit":
                self.db.toggle_flag_ggg_tracker(ctx.message.channel, 1)
                if self.db.get_flag_ggg_tracker(ctx.message.channel) & 1:
                    await self.bot.say("The GGG Tracker will now update from reddit posts to this channel")
                else:
                    await self.bot.say("Reddit post updates have been disabled in this channel")
            elif args[0] == "poe":
                self.db.toggle_flag_ggg_tracker(ctx.message.channel, 2)
                if self.db.get_flag_ggg_tracker(ctx.message.channel) & 2:
                    await self.bot.say("Posts of Pathofexile.com will now be sent to this channel")
                else:
                    await self.bot.say("pathofexile.com posts have been disabled in this channel")
            else:
                await self.bot.say(f"{args[0]} is not a valid ggg tracker source")
        else:
            await self.bot.say("You must be the server owner to use this command")

    @commands.command(pass_context=True, help="Allows the bot to send ggg tracked infomation to the current channel")
    async def enable_ggg_tracker(self, ctx):
        if self.check_owner(ctx):
            if self.db.check_server_exists(ctx.message.server):
                self.db.set_server_ggg(ctx.message.server, 1, ctx.message.channel)
            else:
                self.db.add_server(ctx.message.server, ctx.message.channel)
            await self.bot.say("Your server has been successfully been added to the notification list, you may soon see a flood of embed cards as the server catches up")
        else:
            await self.bot.say("You must be the server owner to use this command")

    @commands.command(pass_context=True, help="Disables the bot from posting ggg tracked information, this removes all channels too")
    async def disable_ggg_tracker(self, ctx):
        if self.check_owner(ctx):
            if self.db.check_server_exists(ctx.message.server):
                self.db.remove_server(ctx.message.server)
                await self.bot.say("Your server has successfully been removed from the notification list")
            else:
                await self.bot.say("The bot hasn't been setup to post messages here, if you are the server owner, use {}`enable_ggg_tracker` to enable it for this channel".format(self.bot.command_prefix))
        else:
            await self.bot.say("You must be the server owner to use this command")

def setup(bot):
    bot.add_cog(GGGTracker(bot))