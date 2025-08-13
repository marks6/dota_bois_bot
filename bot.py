import json
import os
import re
import random
import requests
import leaderboard
import losses_leaderboard
import hero_cache
import player_provider
import nasa_apod
import meta_heros
import logging
import full_match_view
import cocktails
import dotacoach

import discord
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

player_provider.load()
hero_cache.load()

@client.event
async def on_ready():

    print(
        f'{client.user} is connected.\n'
    )


@client.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    print(message.channel.name)
    print(message.content)
    if message.author == client.user:
        return

    parts = message.content.split()

    if parts and parts[0] == '!losses':
        if len(parts) > 1:
            days = parts[1]
            await message.channel.send(losses_leaderboard.create_leaderboard(days))
        else:
            await message.channel.send(losses_leaderboard.create_leaderboard(7))

    if parts and parts[0] == '!wins':
        if len(parts) > 1:
            days = parts[1]
            await message.channel.send(leaderboard.create_leaderboard(days))
        else:
            await message.channel.send(leaderboard.create_leaderboard(7))

    if 'chen' in str.lower(message.content):  # no params
        await message.channel.send(random.choice(chen_resps))
    if 'eewrd' in str.lower(message.content) or 'ewerd' in str.lower(message.content) or 'weerd' in str.lower(message.content):
        for line in meteor:
            await message.channel.send(line)

    if message.content == '!apod':
        apod = nasa_apod.get_apod()

        embed = discord.Embed(
            title=apod['title'],
            description=apod['explanation'] + ' ' + apod['url'],
            color=discord.Color.blue()
        )
        embed.set_image(url=apod['url'])

        await message.channel.send(embed=embed)

    if message.content.startswith("!meta"):
        args = message.content.split()
        if len(args) >= 2 and re.match("-{0,1}[0-9]+",args[1].strip()):
            metaCount = max(-20,min(20,int(args[1]))) # cap between -20 and 20
        else:
            metaCount = 5
        print(meta_heros.get_meta(metaCount))
        await message.channel.send(meta_heros.get_meta(metaCount))

    if message.content.startswith('!lastmatch'):
        parts = message.content.split()
        if len(parts) == 2 and parts[1].isalpha():
            name = parts[1]
            account_id = player_provider.find_by_name(name)            
            if account_id:
                await message.channel.send(f"Searching for last match of player `{name}`...")
                response = full_match_view.create_match_embed(str(account_id))
                if isinstance(response, discord.Embed):
                    await message.channel.send(embed=response)
                else:
                    await message.channel.send(response)
            else:
                await message.channel.send(f"Nobody named '{name}'.")
        else:
            await message.channel.send("Usage: `!lastmatch <name>`")
    
    if message.content.lower().startswith('!cocktail'):
        parts = message.content.split(' ', 1)
        
        if len(parts) < 2:
            await message.channel.send("Usage: `!cocktail <name>` or `!cocktail random`")
            return

        search_term = parts[1]
        recipe = None 

        if search_term.lower() == 'random':
            await message.channel.send("Finding a random cocktail...")
            recipe = cocktails.get_random_cocktail()
        else:
            await message.channel.send(f"Searching for '{search_term}'...")
            recipe = cocktails.get_cocktail_recipe(search_term)

        if recipe:
            embed = cocktails.create_cocktail_embed(recipe)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(f"Sorry, I couldn't find a recipe for '{search_term}'.") 

    if message.content.lower().startswith('!dotacoach'):
        parts = message.content.split(' ', 1)
        if len(parts) == 2:
            name_to_analyze = parts[1]
            
            account_id = player_provider.find_by_name(name_to_analyze)
            
            if not account_id:
                await message.channel.send(f"Sorry, I don't know anyone named '{name_to_analyze}'.")
                return 
            await message.channel.send(f"🤖 Finding and analyzing {name_to_analyze}'s last match, please wait...")

            match_data = dotacoach.get_match_data(str(account_id))

            if not isinstance(match_data, dict):
                await message.channel.send(match_data)
                return             
            analysis_text = dotacoach.analyze_dota_match(match_data, str(account_id), name_to_analyze)
            await message.channel.send(analysis_text)
        else:
            await message.channel.send("Usage: `!analyze <name>`")

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
