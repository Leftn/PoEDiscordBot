from discord.utils import oauth_url
from discord.ext import commands

import config, helpers, screenshot

bot = commands.Bot(command_prefix=".")
league = "Bestiary"

@bot.command(pass_context=True)
async def get(ctx, *args):
    item = helpers.titlecase(args)
    message = await bot.say(f"Trying to find {item}...")
    image = screenshot.get_image(item)
    if image:
        with open("temp.png", "wb") as f:
            image.save(f, "png")
        with open("temp.png", "rb") as f:
            await bot.delete_message(message)
            await bot.send_file(ctx.message.channel, f)
    else:
        await bot.delete_message(message)
        await bot.say(f"Could not find {item}")


@bot.command(pass_context=True)
async def pc (ctx, *args):
    item = helpers.titlecase(args)
    message = await bot.say(f"Checking poe.ninja for the price of {item}...")
    data = helpers.pricecheck(item, league)
    await bot.delete_message(message)
    await bot.say(str(data))

if __name__ == "__main__":
    print("Use the following url to connect the bot to your server:")
    print(oauth_url(config.client_id))
    bot.run(config.token_secret)