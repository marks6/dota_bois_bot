import requests
import json

json_heroes = None
hero_name_cache = None

def load():
    global json_heroes , hero_name_cache

    resp = requests.get("https://api.opendota.com/api/heroes?")
    assert resp.status_code == 200

    json_heroes = resp.json()
    hero_name_cache = {hero["id"] : hero["localized_name"] for hero in json_heroes}

def name_for_hero(id):
    return hero_name_cache[id]

if __name__ == "__main__":
    load()
    print(name_for_hero(56))
    
