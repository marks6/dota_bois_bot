import json
import os
import random
import requests

import discord

TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name="test server")
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    print(guild.members)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    axe_quotes = [
        "There can be no battle till Axe is at hand. And Axe is.",
        "Enemies need killing!",
        "Axe swings his blade."

    ]

    if message.content == '!axe':
        # response = random.choice(axe_quotes)
        response = requests.get(url="https://api.opendota.com/api/players/117777491/recentMatches")
        print(json.loads(response.content))
        # await message.channel.send(json.loads(response.content))


client.run(TOKEN)