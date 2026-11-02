"""Ping the /health endpoint and print the result.

Usage: python health_check.py [base_url]
The base URL defaults to $BASE_URL or http://localhost:8000.
"""
import os
import sys

import httpx


def main() -> int:
    base_url = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BASE_URL", "http://localhost:8000")
    url = base_url.rstrip("/") + "/health"
    try:
        response = httpx.get(url, timeout=5)
    except httpx.HTTPError as exc:
        print(f"Health check FAILED for {url}: {exc}")
        return 1
    print(f"GET {url} -> {response.status_code} {response.text}")
    return 0 if response.status_code == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
