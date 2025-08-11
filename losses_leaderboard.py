import json
import os
import random
import requests
import player_provider
import hero_cache
from tabulate import tabulate


def take_second(elem):
    return elem[1]


def create_leaderboard(days):
    try:
        int(days)
    except ValueError:
        return "int pls"

    if int(days) < 0:
        return "greater than 0 pls"

    name_loss_pairs = []
    params = {'win': '0'}
    if days is not None:
        params = {'date': days, 'win': '0'}

    for player_id in player_provider.get_all():
        response = requests.get(url=f"https://api.opendota.com/api/players/{player_id}/matches",
                                params=params)

        loss_arr = json.loads(response.content)
        if len(loss_arr) == 0:
            continue
        name_loss_pairs.append([player_provider.spoken_name(player_id), len(loss_arr)]) 

    name_loss_pairs.sort(key=take_second, reverse=True)

    formatted = tabulate(name_loss_pairs, headers=['Name', 'Losses'])

    return formatted  # todo actually format this


if __name__ == "__main__":
    player_provider.load()
    hero_cache.load()
    print(create_leaderboard(2))
