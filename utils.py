import requests

def get_pokemon_data(pokemon_name: str):
    """Clean, centralized API fetcher with error handling."""
    try:
        clean_name = pokemon_name.strip().lower()
        if not clean_name:
            return None
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{clean_name}", timeout=5)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None