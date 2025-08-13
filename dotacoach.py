# dotacoach.py
import requests
import vertexai
from vertexai.generative_models import GenerativeModel
import hero_cache
import os
from dotenv import load_dotenv

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_REGION = os.getenv("GCP_REGION")

def get_match_data(account_id: str) -> dict | str:
    """
    Fetches the full match data dictionary for a player's last match
    from the OpenDota API. Returns an error string on failure.
    """
    try:
        player_matches_url = f"https://api.opendota.com/api/players/{account_id}/matches?limit=1"
        response = requests.get(player_matches_url)
        response.raise_for_status()
        match_summary_data = response.json()
        if not match_summary_data:
            return f"No recent matches found for player ID `{account_id}`."
        latest_match_id = match_summary_data[0]['match_id']

        match_details_url = f"https://api.opendota.com/api/matches/{latest_match_id}"
        response = requests.get(match_details_url)
        response.raise_for_status()
        return response.json()         

    except requests.exceptions.HTTPError:
        return f"Error: Player with account ID `{account_id}` not found or their data is private."
    except Exception as e:
        return f"An error occurred while fetching match data: {e}"

def analyze_dota_match(match_data: dict, account_id: str, player_name: str) -> str:
    """
    Uses Gemini to generate a coaching analysis of a Dota 2 match.
    """
    try:
        if not GCP_PROJECT_ID or not GCP_REGION:
            print("ERROR: GCP_PROJECT_ID and GCP_REGION environment variables are not set on the server.")
            return "Sorry, the AI analyzer is not configured correctly by the bot owner."

        vertexai.init(project=GCP_PROJECT_ID, location=GCP_REGION)
        model = GenerativeModel("gemini-2.0-flash-001")

        player_stats = next((p for p in match_data.get('players', []) if p.get('account_id') == int(account_id)), None)
        
        if not player_stats:
            return "Could not find that player in the match data."

        result_string = "Win" if (player_stats.get('win') == 1) else "Loss"

        prompt = f"""
        You are a slightly rude but helpful Dota 2 coach. A player named "{player_name}" just finished a match.
        Analyze their performance based on the following data and (if they lost) provide a short, slightly insulting analysis with 2-3 specific tips for improvement and (if they won) provide a positive dissection of the game with 2-3 things that went well/tips to think about. If the player won, don't spew positive keywords, keep it analytical.
        Keep the tone positive. Do not just list the stats; provide insights.

        Player Data:
        - Match Result: {result_string}
        - Hero: {hero_cache.name_for_hero(player_stats.get('hero_id'))}
        - Kills: {player_stats.get('kills')}
        - Deaths: {player_stats.get('deaths')}
        - Assists: {player_stats.get('assists')}
        - Gold Per Minute (GPM): {player_stats.get('gold_per_min')}
        - XP Per Minute (XPM): {player_stats.get('xp_per_min')}
        - Hero Damage: {player_stats.get('hero_damage')}
        - Tower Damage: {player_stats.get('tower_damage')}
        - Last Hits: {player_stats.get('last_hits')}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return "Sorry, I had a problem analyzing the match."

if __name__ == "__main__":
    print("Loading hero cache...")
    if not hero_cache.hero_name_cache:
        hero_cache.load()
    print("Hero cache loaded.")

    test_account_id = "72138164"  # Jakub's ID
    test_player_name = "Jakub"   # The corresponding name to analyze

    print(f"\n--- Testing with player: {test_player_name} (ID: {test_account_id}) ---")
    print("Fetching latest match data from OpenDota...")
    match_data = get_match_data(test_account_id)

    if isinstance(match_data, dict):
        print("Match data fetched successfully. Now analyzing with Gemini...")

        analysis = analyze_dota_match(match_data, test_account_id, test_player_name)

        print("\n--- GEMINI ANALYSIS ---")
        print(analysis)
    else:
        print("\n--- FAILED TO FETCH DATA ---")
        print(match_data) # This will be the error string returned from the function
