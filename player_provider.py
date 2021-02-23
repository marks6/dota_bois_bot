
# For now we can keep a list of the players we want to keep track of, along with our given nick names
# First name will be the spoken one
_players = [
    (164675486,["Ryan","Chen"]),
    (117777491,["Mark","Jew","Jewgod"]),
    (120513334,["Nick","Skinny",]),
    (122270163,["Riley"]),
    (86854720, ["Logan","Trento"]),
    (72138164, ["Kub","Kuba","Jakub"]),
    (45882730, ["Jummy","Jimmy"]),
    (61424293, ["Wilson"]),
    (119261670,["Flynn","Jeremy"]),
    (76572928, ["Jason"])
]

_nickname_lookup = {}
_spoken_nickname = {}

def load():
    for id, custom_nicknames in _players:

        # record spoken nickname
        _spoken_nickname[id] = custom_nicknames[0]

        for custom_nickname in custom_nicknames:
            _nickname_lookup[custom_nickname.lower()] = id

def printout():
    print(_nickname_lookup)
    print(_spoken_nickname)

def lookup(name):
    name = name.strip().lower()
    return _nickname_lookup[name]

def get_all():
    return [a for a,b in _players ]

def spoken_name(id):
    return _spoken_nickname[id]
 

if __name__ == "__main__":
    load()
    id = 164675486
    name = spoken_name(id)
    print(f"{id}, {name}")
    print(get_all())
