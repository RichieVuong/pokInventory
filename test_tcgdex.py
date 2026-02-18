
import requests
import time

def test_tcgdex(query):
    # TCGdex endpoint for searching cards
    url = "https://api.tcgdex.net/v2/en/cards"
    params = {"name": query}
    
    print(f"Testing TCGdex search for '{query}'...")
    start = time.time()
    try:
        # response = requests.get(url, params=params, timeout=10)
        # Fetch specific card to see full details
        response = requests.get("https://api.tcgdex.net/v2/en/cards/pl4-1", timeout=10)
        elapsed = time.time() - start
        print(f"Status: {response.status_code}, Time: {elapsed:.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            # TCGdex usually returns a list
            print(f"Data type: {type(data)}")
            if isinstance(data, list):
                print(f"Result count: {len(data)}")
                if len(data) > 0:
                    print(f"First item: {data[0]}")
            else:
                print(f"Full data: {data}") 
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_tcgdex("Charizard")
