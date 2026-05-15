import urllib.request
import urllib.error
import json
import sys

BASE_URL = "http://localhost:8000"


def check_health():
    url = f"{BASE_URL}/health"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            body = json.loads(response.read().decode())
            print(f"Status {response.status}: {body}")
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Failed to reach {url}: {e.reason}")
        sys.exit(1)


if __name__ == "__main__":
    check_health()
