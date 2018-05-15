# PoEDiscordBot

PoE Discord Bot is a bot which is a rewrite of PoEWikiBot in the python language.
Since the bot maintainer appears to be inactive, and I have a new idea for some bot functionality, I have decided to create this bot.

### Features

* Wiki Item retrieval (.get)
* poe.ninja pricecheck (.pc)

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

For now, there is no way to automate which leagues are available, so they need to be manually altered for your server


### BEFORE YOU RUN

Since I am lazy and haven't created a setup script, you need to do this yourself.

In the root folder, create the following directories:

    images

You then need to initialise the database with:

    cd cogs
    python pricechecker.py

After this, you should be able to run the bot with:

    python main.py

Finally, each user may set their own league, assuming the same bot is on a different server, the setting will follow them too.

    .set_league <league>

It should be noted that when setting a league, the input is case sensitive

## Notes

You can import the entirety of the pricechecker into your own bot by copying `pricecheker.py` to your cogs directory
and import with 
    
    bot.load_extension("<path to pricechecker.py>")

