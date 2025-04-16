import socket
from urllib.parse import urlparse
import requests
import time
import ssl

def extract_domain(url):
    """Extracts the domain name from a URL."""
    parsed_url = urlparse(url)
    return parsed_url.netloc if parsed_url.netloc else parsed_url.path

def resolve_domain(domain):
    """Resolves a domain name to its IP address."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def make_request(url, method='get', timeout=5, **kwargs):
    """Makes an HTTP/HTTPS request with basic error handling."""
    try:
        response = requests.request(method, url, timeout=timeout, **kwargs)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request Error for {url}: {e}")
        return None

def get_ssl_certificate(hostname, port=443, timeout=5):
    """Retrieves the SSL certificate for a given hostname and port."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                return ssock.getpeercert()
    except Exception as e:
        print(f"Error retrieving SSL certificate for {hostname}: {e}")
        return None

def measure_response_time(url, timeout=5):
    """Measures the total response time of a URL."""
    try:
        start_time = time.time()
        response = make_request(url, timeout=timeout)
        if response:
            return time.time() - start_time, response.status_code, True
        return None, None, False
    except Exception as e:
        print(f"Error measuring response time for {url}: {e}")
        return None, None, False