import requests
import os



def search_card(query):
    """
    Search for cards using the Pokemon TCG API.
    """
    if not query:
        return []
        
    url = "https://api.pokemontcg.io/v2/cards"
    # Use prefix search for faster results and better relevance
    # "char*" instead of "*char*"
    params = {
        "q": f"name:{query}*",
        "pageSize": 12,
        "page": 1,
        "select": "id,name,set,images"
    }
    
    # Temporarily removing API key to isolate issue
    # api_key = os.getenv('POKEMON_TCG_API_KEY')
    # headers = {'X-Api-Key': api_key} if api_key else {}

    try:
        response = requests.get(url, params=params, timeout=5) # Increased timeout slightly
        response.raise_for_status()
        data = response.json()
        
        cards = []
        for item in data.get('data', []):
            cards.append({
                'id': item.get('id'),
                'name': item.get('name'),
                'set_name': item.get('set', {}).get('name'),
                'image_url': item.get('images', {}).get('large'),
                'small_image_url': item.get('images', {}).get('small')
            })
            
        return cards
    except Exception as e:
        print(f"API Error ({e})")
        return []
