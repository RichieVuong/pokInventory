import requests
import os



def search_card(query):
    """
    Search for cards using the Pokemon TCG API.
    """
    if not query:
        return []
        
    url = "https://api.tcgdex.net/v2/en/cards"
    params = {"name": query}
    
    # User-Agent is good practice
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        cards = []
        # TCGdex returns a list of card summaries or a dict (if error/single). 
        # Typically it's a list for search.
        if isinstance(data, list):
            for item in data:
                # TCGdex image is a base URL without extension
                base_image = item.get('image')
                image_url = f"{base_image}/high.webp" if base_image else None
                small_image_url = f"{base_image}/low.webp" if base_image else None
                
                # Enforce "starts with" logic (API does "contains")
                name = item.get('name', '')
                if not name.lower().startswith(query.lower()):
                    continue

                cards.append({
                    'id': item.get('id'),
                    'name': name,
                    'set_name': None,  # Basic search doesn't return set name
                    'image_url': image_url,
                    'small_image_url': small_image_url
                })
            
        return cards
    except Exception as e:
        print(f"API Error ({e})")
        return []
