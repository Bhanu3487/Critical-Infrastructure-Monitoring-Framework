import requests
import time

def check_response_time(url):
    """Checks the response time of a given URL."""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        end_time = time.time()

        response_time = end_time - start_time
        print(f"Response Time Check: {url} -> {response_time} seconds")  # Debug print
        return {"url": url, "response_time": response_time, "status": "UP" if response.ok else "DOWN", "code": response.status_code}
    except requests.exceptions.RequestException as e:
        print(f"Response Time Check Failed: {url} -> {e}")  # Debug print
        return {"url": url, "response_time": None, "status": "DOWN", "code": None}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python responsetime.py <web_portal_url>")
        sys.exit(1)

    web_portal_url = sys.argv[1]
    print(check_response_time(web_portal_url))
