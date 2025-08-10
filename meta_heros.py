import requests
from math import ceil

# KOTL is the current longest hero name (19 chars)
header = f"Hero - Immortal Pick Rate (30 days)\n---------------------------------------\n"

def get_meta(num_heros):
    """ numHeros Can be negative"""
    # returns the string response to chat
    response = requests.get("https://api.opendota.com/api/herostats")
    json_herostats = response.json()

    immortal_games = sum((x["8_pick"] for x in json_herostats))

    top_by_immortal_picks = sorted(json_herostats, key=lambda x:x["8_pick"], reverse=num_heros>0)[:abs(num_heros)]

    body = [f"{x['localized_name']} - {1000*x['8_pick']/immortal_games:2.3}%" for x in top_by_immortal_picks]

    return header+"\n".join(body)

if __name__ == "__main__":
    print(get_meta(6))
    print(get_meta(-6))