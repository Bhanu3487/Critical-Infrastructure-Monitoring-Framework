from .utils import make_request

def check_protocol(url):
    """Checks the HTTP protocol version of a URL."""
    response = make_request(url)
    if response:
        version = response.raw.version
        if version == 10:
            protocol = "HTTP/1.0"
        elif version == 11:
            protocol = "HTTP/1.1"
        elif version == 20:
            protocol = "HTTP/2"
        else:
            protocol = "Unknown"
        return {"url": url, "protocol": protocol, "status_code": response.status_code, "status": "OK"}
    return {"url": url, "protocol": None, "status_code": None, "status": "FAILED"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python protocol.py <url>")
        sys.exit(1)
    url_to_check = sys.argv[1]
    print(check_protocol(url_to_check))