from .utils import extract_domain, get_ssl_certificate
import time
from datetime import datetime

def check_ssl(url):
    """Checks SSL certificate validity and handshake time for HTTPS URLs."""
    if not url.startswith("https"):
        return {"url": url, "ssl_valid": None, "expiry_date": None, "handshake_time_seconds": None, "status": "NOT_HTTPS"}

    hostname = extract_domain(url)
    start_time = time.time()
    cert = get_ssl_certificate(hostname)
    handshake_time = time.time() - start_time

    if cert:
        expiry_date_str = cert.get('notAfter')
        if expiry_date_str:
            try:
                expiry_date = datetime.strptime(expiry_date_str, "%b %d %H:%M:%S %Y %Z")
                is_expired = expiry_date < datetime.now()
                return {
                    "url": url,
                    "ssl_valid": not is_expired,
                    "expiry_date": expiry_date.isoformat(),
                    "handshake_time_seconds": f"{handshake_time:.2f}",
                    "status": "OK" if not is_expired else "EXPIRED"
                }
            except ValueError:
                return {
                    "url": url,
                    "ssl_valid": None,
                    "expiry_date": expiry_date_str,
                    "handshake_time_seconds": f"{handshake_time:.2f}",
                    "status": "EXPIRY_PARSE_ERROR"
                }
        else:
            return {
                "url": url,
                "ssl_valid": None,
                "expiry_date": None,
                "handshake_time_seconds": f"{handshake_time:.2f}",
                "status": "NO_EXPIRY_INFO"
            }
    else:
        return {"url": url, "ssl_valid": False, "expiry_date": None, "handshake_time_seconds": f"{handshake_time:.2f}", "status": "CERTIFICATE_ERROR"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python ssl_check.py <https_url>")
        sys.exit(1)
    url_to_check = sys.argv[1]
    print(check_ssl(url_to_check))