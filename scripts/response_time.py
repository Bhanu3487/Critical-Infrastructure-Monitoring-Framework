from .utils import measure_response_time

def check_response_time(url):
    """Checks the response time of a given URL."""
    response_time, status_code, success = measure_response_time(url)
    if success:
        return {"url": url, "response_time_seconds": f"{response_time:.2f}", "status_code": status_code, "status": "OK"}
    return {"url": url, "response_time_seconds": None, "status_code": None, "status": "FAILED"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python response_time.py <url>")
        sys.exit(1)
    url_to_check = sys.argv[1]
    print(check_response_time(url_to_check))