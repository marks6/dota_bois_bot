import requests

# This will store the mapping of item ID (int) to item Name (str)
item_info_cache = None

def load():
    """
    Fetches all item data from the OpenDota API and creates a simple
    ID -> Name mapping. Should be called once when the application starts.
    """
    global item_info_cache
    if item_info_cache:
        return # Already loaded

    try:
        print("Fetching item data...")
        # This endpoint contains data for all items in the game
        response = requests.get("https://api.opendota.com/api/constants/items")
        response.raise_for_status()
        
        # The API returns a large dictionary where keys are internal names like "blink"
        # The value for each key is another dictionary containing the id and display name ("dname")
        all_item_data = response.json()
        
        item_info_cache = {
            item_data["id"]: item_data["dname"]
            for item_name, item_data in all_item_data.items() if "dname" in item_data
        }
        print("Item data loaded successfully.")

    except Exception as e:
        print(f"Error: Could not load item data. {e}")
        item_info_cache = {}

def name_for_item(item_id: int) -> str | None:
    """Safely gets an item's name from the cache using its ID."""
    if item_info_cache is None:
        return None
    return item_info_cache.get(item_id)

