import json
import os
import random
import requests
import leaderboard
import hero_cache
import player_provider
import nasa_apod

import discord

TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

player_provider.load()
hero_cache.load()

@client.event
async def on_ready():

    print(
        f'{client.user} is connected.\n'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!wins':  # no params
        await message.channel.send(leaderboard.create_leaderboard(None))

    elif message.content.split()[0] == '!wins':  # days provided
        days = message.content.split()[1]
        await message.channel.send(leaderboard.create_leaderboard(days))

    if 'chen' in str.lower(message.content):  # no params
        await message.channel.send(random.choice(chen_resps))

    if 'eewrd' in str.lower(message.content) or 'ewerd' in str.lower(message.content) or 'weerd' in str.lower(message.content):
        for line in meteor:
            await message.channel.send(line)

    if message.content == '!apod':  # no params
        apod = nasa_apod.get_apod()

        await message.channel.send(apod['title'])
        await message.channel.send(apod['url'])
        await message.channel.send(apod['explanation'])


chen_resps = [
    "All are healed.",
    'So begins the persecution.',
    'For Obelis, the one God.',
    'The Inquisitor has arrived.',
    'Knight of the faith.',
    'God willing.',
    'Say your prayers.',
    'The recusant shall pay!',
    'Your judgment comes.',
    "Can't escape your sins."
]

meteor = [
    ".  0",
    ".   0",
    ".    0",
    ".     0",
    ".      000000000"
]

client.run(TOKEN)
