import requests
import datetime
import discord
import hero_cache

def create_match_embed(account_id: str) -> discord.Embed | str:
    """
    This is the main function for your bot to call.
    It takes a player's account_id and returns a formatted discord.Embed object
    with the details of their last match, or an error string.
    """
    try:
        player_matches_url = f"https://api.opendota.com/api/players/{account_id}/matches?limit=1"
        response = requests.get(player_matches_url)
        response.raise_for_status()
        match_summary_data = response.json()
        if not match_summary_data:
            return f"No recent matches found for player ID `{account_id}`."
        latest_match_id = match_summary_data[0]['match_id']
    except requests.exceptions.HTTPError:
        return f"Error: Player with account ID `{account_id}` not found or their data is private."
    except requests.exceptions.RequestException as e:
        return f"A network error occurred: {e}"

    try:
        match_details_url = f"https://api.opendota.com/api/matches/{latest_match_id}"
        response = requests.get(match_details_url)
        response.raise_for_status()
        match = response.json()
    except Exception as e:
        return f"Could not get details for match `{latest_match_id}`. Error: {e}"

    radiant_won = match.get('radiant_win', False)
    duration_formatted = str(datetime.timedelta(seconds=match.get('duration', 0)))

    start_time_unix = match.get('start_time', 0)
    match_datetime = datetime.datetime.fromtimestamp(start_time_unix)

    player_in_match = next((p for p in match.get('players', []) if p.get('account_id') == int(account_id)), None)
    
    embed_color = discord.Color.dark_grey()
    if player_in_match:
        player_on_radiant = player_in_match.get('isRadiant', True)
        if (player_on_radiant and radiant_won) or (not player_on_radiant and not radiant_won):
            embed_color = discord.Color.green()
        else:
            embed_color = discord.Color.red()

    embed = discord.Embed(
        title=f"Dota 2 Match Report: {latest_match_id}",
        description=f"**Duration:** `{duration_formatted}`",
        color=embed_color,
        timestamp=match_datetime
    )

    all_players = match.get('players', [])
    radiant_players = sorted([p for p in all_players if p.get('isRadiant', True)], key=lambda x: x.get('player_slot'))
    dire_players = sorted([p for p in all_players if not p.get('isRadiant', True)], key=lambda x: x.get('player_slot'))

    # Add Radiant Team as a series of inline fields
    radiant_result = "🏆 VICTORY" if radiant_won else "DEFEAT"
    embed.add_field(name=f"⚔️ RADIANT TEAM ({radiant_result})", value="", inline=False)
    for player in radiant_players:
        player_name = player.get('personaname', 'Anonymous')
        hero_id = player.get('hero_id', 0)
        hero_name = hero_cache.name_for_hero(hero_id)
        
        kda = f"{player.get('kills', 0)}/{player.get('deaths', 0)}/{player.get('assists', 0)}"
        gpm_xpm = f"{player.get('gold_per_min', 0)}/{player.get('xp_per_min', 0)}"

        embed.add_field(
            name=f"`{player_name}`",
            value=f"**{hero_name}**\nKDA: `{kda}`\nGPM/XPM: `{gpm_xpm}`",
            inline=True
        )
        
    # Add Dire Team as a series of inline fields
    dire_result = "DEFEAT" if radiant_won else "🏆 VICTORY"
    embed.add_field(name=f"💀 DIRE TEAM ({dire_result})", value="", inline=False)
    for player in dire_players:
        player_name = player.get('personaname', 'Anonymous')
        hero_id = player.get('hero_id', 0)
        hero_name = hero_cache.name_for_hero(hero_id)
        
        kda = f"{player.get('kills', 0)}/{player.get('deaths', 0)}/{player.get('assists', 0)}"
        gpm_xpm = f"{player.get('gold_per_min', 0)}/{player.get('xp_per_min', 0)}"
        
        embed.add_field(
            name=f"`{player_name}`",
            value=f"**{hero_name}**\nKDA: `{kda}`\nGPM/XPM: `{gpm_xpm}`",
            inline=True
        )
    
    embed.set_footer(text=f"Report generated for player ID {account_id}")
    
    return embed

if __name__ == "__main__":
    if hero_cache.load():
        default_id = "86745912"
        try:
            user_input = input(f"Enter a player's Dota 2 Account ID (or press Enter for default: {default_id}): ")
            account_id_to_search = user_input.strip() or default_id
            if not account_id_to_search.isdigit():
                print("Error: Please enter a valid numerical account ID.")
            else:
                response = create_match_embed(account_id_to_search)
                if isinstance(response, discord.Embed):
                    print("\n--- EMBED DATA ---")
                    print(response.to_dict())
                else:
                    print(response)
        except KeyboardInterrupt:
            print("\nExiting.")
