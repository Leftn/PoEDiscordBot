import pip, os

import cogs.pricechecker

def install(package):
    pip.main(["install", package])

try:
    import selenium
except ImportError:
    install("selenium")
try:
    import discord
except ImportError:
    install("discord.py")
try:
    import PIL
except ImportError:
    install("Pillow")

try:
    import feedparser
except ImportError:
    install("feedparser")

os.mkdir("db")
os.mkdir("logs")
os.mkdir("images")

cogs.pricechecker.main()