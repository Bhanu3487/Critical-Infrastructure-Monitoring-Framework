from .utils import extract_domain, resolve_domain
import ipaddress
import socket

def check_dns(url):
    """Checks DNS resolution and whether the resolved IP is public."""
    domain = extract_domain(url)
    if not domain:
        return {"url": url, "domain": None, "resolved_ip": None, "status": "INVALID_URL"}

    ip_address = resolve_domain(domain)
    if not ip_address:
        return {"url": url, "domain": domain, "resolved_ip": None, "status": "DNS_FAILED"}

    if ip_address == "127.0.0.1" or (ip_address and ipaddress.ip_address(ip_address).is_private):
        return {"url": url, "domain": domain, "resolved_ip": ip_address, "status": "PRIVATE_IP"}

    try:
        socket.create_connection((ip_address, 80), timeout=3)  # Quick check for basic connectivity
        connectivity_status = "REACHABLE"
    except (socket.timeout, ConnectionRefusedError):
        connectivity_status = "UNREACHABLE"

    return {"url": url, "domain": domain, "resolved_ip": ip_address, "status": "RESOLVED", "connectivity": connectivity_status}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python dns_check.py <url>")
        sys.exit(1)
    url_to_check = sys.argv[1]
    print(check_dns(url_to_check))