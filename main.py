from urllib.parse import quote
import logging.handlers
import time

from discord.utils import oauth_url
from discord.ext import commands

import config, helpers, screenshot

bot = commands.Bot(command_prefix=".")
startup_extensions = ["pricechecker", "leaderboards"]

log = logging.getLogger("main")
log.setLevel(config.log_level)
log_formatter = logging.Formatter('%(levelname)s: %(message)s')
log_formatter_file = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_stderrHandler = logging.StreamHandler()
log_stderrHandler.setFormatter(log_formatter)
log.addHandler(log_stderrHandler)
if config.log_filename is not None and __name__ == "__main__":
    log_fileHandler = logging.handlers.RotatingFileHandler(config.log_filename, maxBytes=config.log_maxsize, backupCount=config.log_backup_count)
    log_fileHandler.setFormatter(log_formatter_file)
    log.addHandler(log_fileHandler)


@bot.event
async def on_message(message):
    if message.content and message.content[0] == str(bot.command_prefix):
        log.info("Message: "+message.content+"; User: ({}:{})".format(message.author.name, message.author.id))
    await bot.process_commands(message)


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


if __name__ == "__main__":
    while True:
        try:
            print("Use the following url to connect the bot to your server:")
            print(oauth_url(config.client_id))
            for extension in startup_extensions:
                try:
                    bot.load_extension("cogs."+extension)
                except Exception as e:
                    exc = '{}: {}'.format(type(e).__name__, e)
                    print('Failed to load extension {}\n{}'.format(extension, exc))
            bot.run(config.token_secret)
        except Exception as e:
            log.error(e)
        time.sleep(60)
