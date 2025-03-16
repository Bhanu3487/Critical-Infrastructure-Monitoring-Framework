import requests

def check_uptime(url):
    try:
        response = requests.get(url, timeout=5)
        print(f"Uptime Check: {url} -> Status Code: {response.status_code}")  # Debug print
        return {"status": "UP" if response.ok else "DOWN", "code": response.status_code}
    except requests.exceptions.RequestException as e:
        print(f"Uptime Check Failed: {e}")  # Debug print
        return {"status": "DOWN", "code": None}

if __name__ == "__main__":
    print(check_uptime("https://www.google.com/"))
