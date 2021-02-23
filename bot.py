import json
import os
import random
import requests
import leaderboard

import discord

TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


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

client.run(TOKEN)
