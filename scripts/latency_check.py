import subprocess
import re
import socket
import platform
from urllib.parse import urlparse

def extract_domain(url):
    """Extracts domain from a URL."""
    parsed_url = urlparse(url)
    return parsed_url.netloc if parsed_url.netloc else parsed_url.path  # Handle cases where netloc is empty

def check_latency_packet_loss(url):
    """Checks network latency and packet loss using ping."""
    try:
        domain = extract_domain(url)  # Extract domain from URL
        ip_address = socket.gethostbyname(domain)  # Convert domain to IP
        os_type = platform.system()  # Detect OS

        # Determine command based on OS
        if os_type == "Windows":
            cmd = ["ping", "-n", "5", ip_address]  # Windows: -n (count)
        else:
            cmd = ["ping", "-c", "5", "-W", "5", ip_address]  # Linux/macOS: -c (count), -W (timeout)

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Extract packet loss
        if os_type == "Windows":
            loss_match = re.search(r"Lost = (\d+) \((\d+)% loss\)", result.stdout)
            packet_loss = int(loss_match.group(2)) if loss_match else None
        else:
            loss_match = re.search(r"(\d+)% packet loss", result.stdout)
            packet_loss = int(loss_match.group(1)) if loss_match else None

        # Extract average latency
        if os_type == "Windows":
            latency_match = re.search(r"Average = (\d+)ms", result.stdout)
            avg_latency = float(latency_match.group(1)) if latency_match else None
        else:
            latency_match = re.search(r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+", result.stdout)
            avg_latency = float(latency_match.group(1)) if latency_match else None

        # Determine status
        if packet_loss is None or avg_latency is None:
            status = "ERROR"
        elif packet_loss == 0 and avg_latency < 100:
            status = "HEALTHY"
        else:
            status = "ISSUE_DETECTED"

        print(f"Latency & Packet Loss Check: {url} -> IP: {ip_address}, Avg Latency: {avg_latency}ms, Packet Loss: {packet_loss}%, Status: {status}")  

        return {
            "url": url,
            "ip": ip_address,
            "avg_latency_ms": avg_latency,
            "packet_loss_percent": packet_loss,
            "status": status
        }

    except socket.gaierror:
        print(f"Error: Could not resolve domain {url}")  
        return {"url": url, "ip": None, "avg_latency_ms": None, "packet_loss_percent": None, "status": "ERROR"}

    except Exception as e:
        print(f"Latency Check Failed: {url} -> {e}")  
        return {"url": url, "ip": None, "avg_latency_ms": None, "packet_loss_percent": None, "status": "ERROR"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python latency_check.py <website_url>")
        sys.exit(1)

    website_url = sys.argv[1]
    print(check_latency_packet_loss(website_url))
