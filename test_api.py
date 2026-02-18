
import requests
import time

def test_url(url, timeout=10):
    print(f"Testing {url} with timeout={timeout}s...")
    start = time.time()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        elapsed = time.time() - start
        print(f"Status: {response.status_code}, Time: {elapsed:.2f}s")
        if response.status_code == 200:
            print("Response preview:", response.text[:200])
    except Exception as e:
        elapsed = time.time() - start
        print(f"Error: {e}, Time: {elapsed:.2f}s")

if __name__ == "__main__":
    test_url("https://api.pokemontcg.io", timeout=30)
    test_url("https://api.pokemontcg.io/v2/cards/xy1-1", timeout=30)
    test_url("https://api.pokemontcg.io/v2/cards?pageSize=1", timeout=30)
