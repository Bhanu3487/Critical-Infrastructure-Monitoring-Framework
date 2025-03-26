import socket
from urllib.parse import urlparse
import ipaddress

def check_dns_resolution(url):
    """Checks the DNS resolution and connectivity of a given URL."""
    try:
        domain = urlparse(url).netloc  # Extract domain from URL
        if not domain:
            raise ValueError("Invalid URL format.")
        
        ip_address = socket.gethostbyname(domain)  # Resolve domain to IP

        # Check if the resolved IP is local/loopback
        if ip_address == "127.0.0.1" or ipaddress.ip_address(ip_address).is_private:
            print(f"DNS Resolution Check: {domain} resolved to {ip_address}, but is NOT a public IP")  # Debug print
            return {"url": url, "domain": domain, "resolved_ip": ip_address, "status": "UNRESOLVED"}

        # Check if the resolved IP is reachable
        try:
            socket.create_connection((ip_address, 80), timeout=5)  # Try connecting to port 80 (HTTP)
            status = "REACHABLE"
            print(f"DNS Resolution & Connectivity Check: {domain} resolved to {ip_address} and is REACHABLE")  # Debug print
        except (socket.timeout, ConnectionRefusedError):
            status = "UNREACHABLE"
            print(f"DNS Resolution Check: {domain} resolved to {ip_address}, but is UNREACHABLE")  # Debug print

        return {"url": url, "domain": domain, "resolved_ip": ip_address, "status": status}
    
    except (socket.gaierror, ValueError):
        print(f"DNS Resolution Failed: Could not resolve {url}")  # Debug print
        return {"url": url, "domain": None, "resolved_ip": None, "status": "FAILED"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python DNS_resolution_check.py <web_portal_url>")
        sys.exit(1)

    web_portal_url = sys.argv[1]
    print(check_dns_resolution(web_portal_url))
