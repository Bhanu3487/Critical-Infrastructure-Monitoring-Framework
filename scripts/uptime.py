import requests

def check_uptime(url):
    """Checks the uptime of a given URL."""
    try:
        response = requests.get(url, timeout=5)
        print(f"Uptime Check: {url} -> Status Code: {response.status_code}")  # Debug print
        return {"url": url, "status": "UP" if response.ok else "DOWN", "code": response.status_code}
    except requests.exceptions.RequestException as e:
        print(f"Uptime Check Failed: {url} -> {e}")  # Debug print
        return {"url": url, "status": "DOWN", "code": None}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python uptime.py <web_portal_url>")
        sys.exit(1)

    web_portal_url = sys.argv[1]
    print(check_uptime(web_portal_url))
