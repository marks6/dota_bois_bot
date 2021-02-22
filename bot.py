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

    command = message.content.split()[0]

    if command == '!wins':
        days = message.content.split()[1]

        await message.channel.send(leaderboard.create_leaderboard(days))


client.run(TOKEN)
