import requests
import discord

def _parse_drink_data(drink_data: dict) -> dict:
    """Internal helper to parse the drink JSON from the API into a clean dict."""
    ingredients = []
    for i in range(1, 16):
        ingredient = drink_data.get(f"strIngredient{i}")
        measure = drink_data.get(f"strMeasure{i}")
        if ingredient is None or ingredient.strip() == "":
            break
        line = f"{measure.strip()} - {ingredient.strip()}" if measure and measure.strip() else ingredient.strip()
        ingredients.append(line)
    
    return {
        'name': drink_data.get('strDrink'),
        'instructions': drink_data.get('strInstructions'),
        'image_url': drink_data.get('strDrinkThumb'),
        'ingredients': ingredients
    }

def get_cocktail_recipe(search_term: str) -> dict | None:
    """
    Searches for a specific cocktail by name using a case-insensitive method.
    """
    if not search_term:
        return None
        
    first_letter = search_term[0]
    
    api_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={first_letter}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if not data or not data.get('drinks'):
            return None

        all_drinks = data['drinks']
        lower_search_term = search_term.lower()

        for drink in all_drinks:
            if drink.get('strDrink').lower() == lower_search_term:
                return _parse_drink_data(drink)
        
        return None

    except requests.exceptions.RequestException as e:
        print(f"An API or network error occurred: {e}")
        return None

def get_random_cocktail() -> dict | None:
    """Fetches a single random cocktail."""
    api_url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if not data or not data.get('drinks'):
            return None
        return _parse_drink_data(data['drinks'][0])
    except requests.exceptions.RequestException as e:
        print(f"An API or network error occurred: {e}")
        return None

def create_cocktail_embed(recipe: dict) -> discord.Embed:
    """Takes a recipe dictionary and formats it into a Discord Embed."""
    embed = discord.Embed(
        title=f"🍹 {recipe['name']}",
        description=recipe['instructions'],
        color=discord.Color.blurple()
    )
    if recipe['image_url']:
        embed.set_thumbnail(url=recipe['image_url'])
    if recipe['ingredients']:
        embed.add_field(
            name="Ingredients",
            value="\n".join(f"• {item}" for item in recipe['ingredients']),
            inline=False
        )
    return embed
