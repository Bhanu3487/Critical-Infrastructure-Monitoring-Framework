from .utils import make_request

def check_status_and_headers(url):
    """Checks the HTTP status code and specific headers of a URL."""
    response = make_request(url)
    if response:
        headers = response.headers
        return {
            "url": url,
            "status_code": response.status_code,
            "content_type": headers.get('Content-Type', 'Not Available'),
            "cache_control": headers.get('Cache-Control', 'Not Available'),
            "x_request_id": headers.get('X-Request-ID', 'Not Available'),
            "status": "OK"
        }
    return {
        "url": url,
        "status_code": None,
        "content_type": "FAILED",
        "cache_control": "FAILED",
        "x_request_id": "FAILED",
        "status": "FAILED"
    }

def check_errors(url):
    """Flags 4xx and 5xx HTTP error status codes."""
    response = make_request(url)
    if response:
        if 400 <= response.status_code < 500:
            return {"url": url, "status_code": response.status_code, "error_type": "CLIENT_ERROR", "status": "ERROR"}
        elif 500 <= response.status_code < 600:
            return {"url": url, "status_code": response.status_code, "error_type": "SERVER_ERROR", "status": "ERROR"}
        else:
            return {"url": url, "status_code": response.status_code, "error_type": "NONE", "status": "OK"}
    return {"url": url, "status_code": None, "error_type": "REQUEST_FAILED", "status": "FAILED"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python status_check.py <url>")
        sys.exit(1)
    url_to_check = sys.argv[1]
    status_info = check_status_and_headers(url_to_check)
    error_info = check_errors(url_to_check)
    print("Status and Headers:", status_info)
    print("Error Check:", error_info)