import json
import os
import random
import requests
import player_provider
import hero_cache

# response = requests.get(url="https://api.opendota.com/api/players/117777491/matches", params={'date': 20, 'win': '1'})
# take second element for sort
def take_second(elem):
    return elem[1]


def create_leaderboard(days):
    try:
        int(days)
    except ValueError:
        return "int pls"

    if int(days) < 0:
        return "greater than 0 pls"

    name_wins_pairs = []
    params = {'win': '1'}
    if days is not None:
        params = {'date': days, 'win': '1'}

    for player_id in player_provider.get_all():
        response = requests.get(url=f"https://api.opendota.com/api/players/{player_id}/matches",
                                params=params)

        wins_arr = json.loads(response.content)
        if len(wins_arr) == 0:
            continue
        name_wins_pairs.append([player_provider.spoken_name(player_id), len(wins_arr)]) 

    name_wins_pairs.sort(key=take_second, reverse=True)

    formatted = ""

    for tuple in name_wins_pairs:
        formatted += tuple[0] + "         " + str(tuple[1]) + '\n'

    return formatted  # todo actually format this


if __name__ == "__main__":
    player_provider.load()
    hero_cache.load()
    print(create_leaderboard(2))
