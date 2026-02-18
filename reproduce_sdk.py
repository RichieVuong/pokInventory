
from pokemontcgsdk import Card
import os
import time

# Set API key if available
api_key = os.getenv('POKEMON_TCG_API_KEY')
if api_key:
    # The SDK configuration for API key might differ, usually it's environment variable or config class.
    # Looking at docs, it seems it reads POKEMONTCG_IO_API_KEY or we set it manually.
    # Let's try setting it if the library exposes a way, or rely on env var if it supports it.
    os.environ['POKEMONTCG_IO_API_KEY'] = api_key
    print("Configured API Key for SDK.")

print("Testing SDK search for 'Charizard'...")
start = time.time()
try:
    # Use the syntax user provided
    cards = Card.where(q='name:charizard', pageSize=1)
    if cards:
        print(f"Found {len(cards)} cards.")
        print(f"First card: {cards[0].name}")
    else:
        print("No cards found.")
    print(f"Time: {time.time() - start:.2f}s")
except Exception as e:
    print(f"SDK Error: {e}")
    print(f"Time: {time.time() - start:.2f}s")

print("\nTesting SDK search for 'ch'...")
start = time.time()
try:
    cards = Card.where(q='name:ch', pageSize=1)
    if cards:
        print(f"Found {len(cards)} cards.")
    else:
        print("No cards found.")
    print(f"Time: {time.time() - start:.2f}s")
except Exception as e:
    print(f"SDK Error: {e}")
    print(f"Time: {time.time() - start:.2f}s")
