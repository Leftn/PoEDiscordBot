import json

import requests
from discord.embeds import Embed

import config

def titlecase(tuple):
    # Converts a tuple of strings to titlecasing (Each string should be 1 word)
    # e.g. hand of wisdom and action --> Hand of Wisdom and Action
    tuple = [x.lower() for x in tuple] # Convert to list so we can do reassignment
    for i in range(len(tuple)):
        if i == 0 or tuple[i] not in config.excluded_titlecase_words:
            tuple[i] = tuple[i][0].upper()+tuple[i][1:]
        else:
            continue
    return " ".join(tuple)

def pricecheck(item, league):
    """
    
    :param item: String: a titlecased name of the item to search for
    :param league: String: The specified league to search
    :return: 
    """
    data = {"league":league, "name":item}
    headers = {"Content-Type":"application/json"}
    # The server is an API of my own making, I havn't bothered writing documentation/creating a domain name yet
    # The server is in pre-pre-alpha and only this part of the site works
    data = requests.post("http://45.76.116.155/api/v1/get", data=json.dumps(data), headers=headers).json()
    return data

def create_embed_pricing(data):
    embed = Embed(colour=0x4f1608)
    embed.add_field(name="Chaos", value=data.get("chaos"))
    embed.add_field(name="Exalted", value=data.get("exalted"))
    print(data)
    return embed