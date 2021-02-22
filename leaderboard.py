import json
import os
import random
import requests
import player_provider


# response = requests.get(url="https://api.opendota.com/api/players/117777491/matches", params={'date': 20, 'win': '1'})
# take second element for sort
def takeSecond(elem):
    return elem[1]


def create_leaderboard(days):
    # kv pairs w/ name + wins ?
    name_wins_pairs = []
    for player in player_provider._players:
        response = requests.get(url=f"https://api.opendota.com/api/players/{player[0]}/matches",
                                params={'date': days, 'win': '1'})

        wins_arr = json.loads(response.content)
        if len(wins_arr) == 0:
            continue
        name_wins_pairs.append([player[1][0], len(wins_arr)])

    name_wins_pairs.sort(key=takeSecond, reverse=True)

    formatted = ""

    for tuple in name_wins_pairs:
        formatted += tuple[0] + "         " + str(tuple[1]) + '\n'

    return formatted  # todo actually format this


if __name__ == "__main__":
    print(create_leaderboard(365))
