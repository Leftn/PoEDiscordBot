import pip, os

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

try:
    os.mkdir("db")
except FileExistsError:
    pass
try:
    os.mkdir("logs")
except FileExistsError:
    pass
try:
    os.mkdir("images")
except FileExistsError:
    pass