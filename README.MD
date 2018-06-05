# PoEDiscordBot

PoE Discord Bot is a bot which is a rewrite of PoEWikiBot in the python language.
Since the bot maintainer appears to be inactive, and I have a new idea for some bot functionality, I have decided to create this bot.

### Features

* Wiki Item retrieval (.get)
* poe.ninja pricecheck (.pc)
* Ladder viewer (.top5)


![Heart](/Examples/KaomsHeart.png?raw=true "Kaom's Heart")

There is also a basic spellchecker for the pricechecker

![Spellchecker](/Examples/Spellcheck.png "Spellcheck Example")

The bot also has support for getting the wiki article of most items

![Get](/Examples/GetUsage.png "Get Usage")

Newest feature involves retrieving data from the leaderboards, at the moment, it only supports getting the top 5 of any given league.

![Leaderboards](/Examples/Leaderboards.png "Leaderboards Example")

### Quite notice

As of 12-05-2018 running chrome in headless mode is signifigantly slower than other browsers (Takes ~30s to get a screenshot of a page), the only other browser which is supported is PhantomJS which is being depreciated by selenium.
I do not recommend using the `.get` command because of this until google have fixed their browser

### Requirements

* python 3.6
* discord-python
* Selenium
* Pillow
* A browser + it's driver

### Installation

    
    sudo pip install selenium
    sudo pip install discord.py
    sudo pip install Pillow

At the moment, only phantomjs and chrome are supported. Firefox coming soon.

If you use chrome: https://sites.google.com/a/chromium.org/chromedriver/

You must save the path where you store the driver in config.py under the variable `driver_executable`
    
### Configuration

You must set the following for the bot to work:

    client_id = ""
    token_secret =""

Somehow I managed to delete config forever and I am not good enough at git to add it back in whilst also keeping it .gitignored.
So I will put the default config values here...


    import os, logging
    
    browser_height = 2500
    browser_width = 2500
    excluded_titlecase_words = ["of", "and", "the", "to", "at", "for"]
    driver_executable = ""
    browser = "chrome"
    client_id = ""
    token_secret = ""
    wiki = "https://pathofexile.gamepedia.com/{}"
    
    log_level = logging.INFO
    log_filename = os.path.join("logs","main.log")
    log_maxsize = 1024 * 256
    log_backup_count = 5


### BEFORE YOU RUN

You need to run the setup script with:

    python setup.py

After this, you should be able to run the bot with:

    python main.py

Finally, each user may set their own league, assuming the same bot is on a different server, the setting will follow them too.

    .set_league <league>

It should be noted that when setting a league, the input is case sensitive