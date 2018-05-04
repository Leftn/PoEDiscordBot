#PoEDiscordBot

PoE Discord Bot is a bot which is a rewrite of PoEWikiBot in the python language.
Since the bot maintainer appears to be inactive, and I have a new idea for some bot functionality, I have decided to create this bot.

### Features

* Wiki Item retrieval (.get)
* poe.ninja pricecheck (.pc)

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

    db
    images

Once done, you need to run database.py once:

    python database.py

After this, you should be able to run the bot with:

    python main.py