# scripts/uptime.py
from .utils import make_request

def check_uptime(url):
    """Checks the uptime of a given URL by checking the HTTP status code."""
    response = make_request(url)
    if response:
        return {"url": url, "status_code": response.status_code, "status": "UP" if response.ok else "DOWN"}
    return {"url": url, "status_code": None, "status": "DOWN"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python uptime.py <url>")
        sys.exit(1)
    url_to_check = sys.argv[1]
    print(check_uptime(url_to_check))