import requests
import time

def check_response_time(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        end = time.time()
        response_time = round((end - start) * 1000, 2)  # Convert to milliseconds

        print(f"Response Time Check: {url} -> {response_time}ms (Status: {response.status_code})")  # Debug print
        return {"status": "UP" if response.ok else "DOWN", "response_time": response_time}
    except requests.exceptions.RequestException as e:
        print(f"Response Time Check Failed: {e}")  # Debug print
        return {"status": "DOWN", "response_time": None}

if __name__ == "__main__":
    print(check_response_time("https://www.google.com/"))
