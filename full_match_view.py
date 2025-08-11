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
    # --- Step 1 & 2: Fetching data is the same ---
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

    # --- Step 3: Build the discord.Embed object with the new layout ---
    radiant_won = match.get('radiant_win', False)
    duration_formatted = str(datetime.timedelta(seconds=match.get('duration', 0)))

    player_in_match = next((p for p in match.get('players', []) if p.get('account_id') == int(account_id)), None)
    
    embed_color = discord.Color.dark_grey() # Default color
    if player_in_match:
        player_on_radiant = player_in_match.get('isRadiant', True)
        if (player_on_radiant and radiant_won) or (not player_on_radiant and not radiant_won):
            embed_color = discord.Color.green()
        else:
            embed_color = discord.Color.red()

    embed = discord.Embed(
        title=f"Dota 2 Match Report: {latest_match_id}",
        description=f"**Duration:** `{duration_formatted}`",
        color=embed_color
    )

    all_players = match.get('players', [])
    radiant_players = sorted([p for p in all_players if p.get('isRadiant', True)], key=lambda x: x.get('player_slot'))
    dire_players = sorted([p for p in all_players if not p.get('isRadiant', True)], key=lambda x: x.get('player_slot'))

    # --- CHANGE: Add Radiant Team as a series of inline fields ---
    radiant_result = "🏆 VICTORY" if radiant_won else "DEFEAT"
    # Add a non-inline field to act as a full-width header for the team
    embed.add_field(name=f"⚔️ RADIANT TEAM ({radiant_result})", value="", inline=False)
    for player in radiant_players:
        player_name = player.get('personaname', 'Anonymous')
        hero_id = player.get('hero_id', 0)
        hero_name = hero_cache.name_for_hero(hero_id)
        
        kda = f"{player.get('kills', 0)}/{player.get('deaths', 0)}/{player.get('assists', 0)}"
        gpm_xpm = f"{player.get('gold_per_min', 0)}/{player.get('xp_per_min', 0)}"

        # Each player is a new field, set to inline=True to create a grid
        embed.add_field(
            name=f"`{player_name}`",
            value=f"**{hero_name}**\nKDA: `{kda}`\nGPM/XPM: `{gpm_xpm}`",
            inline=True
        )
        
    # --- CHANGE: Add Dire Team as a series of inline fields ---
    dire_result = "DEFEAT" if radiant_won else "🏆 VICTORY"
    # Add another full-width header for the next team
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

