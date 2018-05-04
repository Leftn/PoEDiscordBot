from urllib.parse import quote

from discord.utils import oauth_url
from discord.ext import commands

import config, helpers, screenshot

bot = commands.Bot(command_prefix=".")

try:
    league = {config.base_server:"Standard"} # Don't need to have this set
except AttributeError:
    league = {}

def _set_league(server, new_league):
    global league
    league.update({server:new_league})

def _get_league(server):
    global league
    return league.get(server)

@bot.command(pass_context=True)
async def get(ctx, *args):
    item = helpers.titlecase(args)
    message = await bot.say(f"Trying to find {item}...")
    image = screenshot.get_image(item)
    if image:
        with open(image, "rb") as f:
            # In order to change from a PIL image format to something discord.py can use we need to use a temporary file
            # TODO Determine how bad this is, since the bot is asynchronous; maybe just just rename the images as hashes
            await bot.edit_message(message, "<"+config.wiki.format(quote(item)+">")) # The angle brackets are there to turn off the auto embeding (Makes it look ugly
            await bot.send_file(ctx.message.channel, f)
    else:
        await bot.delete_message(message)
        await bot.say(f"Could not find {item}")


@bot.command(pass_context=True)
async def pc (ctx, *args):
    item = helpers.titlecase(args)
    message = await bot.say(f"Checking poe.ninja for the price of {item}...")
    data = helpers.pricecheck(item, _get_league(ctx.message.server))
    await bot.delete_message(message)
    await bot.say(str(data))

@bot.command(pass_context=True)
async def set_league(ctx, *args): #TODO: Determine if this command should be protected
    name = helpers.titlecase(args)
    if name in config.leagues:
        server = ctx.message.server
        _set_league(server,name)
        await bot.say(f"Successfully set default league to: {name}")
    else:
        await bot.say(f"League '{name}' not a playable league")


if __name__ == "__main__":
    print("Use the following url to connect the bot to your server:")
    print(oauth_url(config.client_id))
    bot.run(config.token_secret)
