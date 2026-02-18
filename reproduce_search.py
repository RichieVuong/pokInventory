
import os
import django
from django.conf import settings

# Configure Django settings manually since we are running a standalone script
# We need to point to the settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from collection.utils import search_card

print("Testing search for 'ch'...")
results = search_card("ch")
print(f"Results for 'ch': {len(results)}")
for card in results:
    print(f"- {card['name']}")

print("\nTesting search for 'charizard'...")
results_full = search_card("charizard")
print(f"Results for 'charizard': {len(results_full)}")
