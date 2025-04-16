import subprocess
import re
import platform
from .utils import extract_domain, resolve_domain

def check_latency(url, count=3, timeout=5):
    """Checks network latency and packet loss using ping."""
    domain = extract_domain(url)
    ip_address = resolve_domain(domain)
    if not ip_address:
        return {"url": url, "ip": None, "avg_latency_ms": None, "packet_loss_percent": None, "status": "DNS_FAILED"}

    os_type = platform.system()
    if os_type == "Windows":
        cmd = ["ping", "-n", str(count), ip_address]
    else:
        cmd = ["ping", "-c", str(count), "-W", str(timeout), ip_address]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        packet_loss = None
        avg_latency = None

        if os_type == "Windows":
            loss_match = re.search(r"Lost = (\d+)", result.stdout)
            sent_match = re.search(r"Sent = (\d+)", result.stdout)
            if loss_match and sent_match and int(sent_match.group(1)) > 0:
                packet_loss = (int(loss_match.group(1)) / int(sent_match.group(1))) * 100
            latency_match = re.search(r"Average = (\d+)ms", result.stdout)
            avg_latency = float(latency_match.group(1)) if latency_match else None
        else:
            loss_match = re.search(r"(\d+)% packet loss", result.stdout)
            packet_loss = float(loss_match.group(1)) if loss_match else None
            latency_match = re.search(r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+", result.stdout)
            avg_latency = float(latency_match.group(1)) if latency_match else None

        status = "OK"
        if packet_loss is not None and packet_loss > 0:
            status = "PACKET_LOSS"
        if avg_latency is not None and avg_latency > 200:  # Adjust threshold as needed
            status = "HIGH_LATENCY"
        if packet_loss is not None and packet_loss > 0 and avg_latency is not None and avg_latency > 200:
            status = "ISSUES"

        return {
            "url": url,
            "ip": ip_address,
            "avg_latency_ms": avg_latency,
            "packet_loss_percent": packet_loss,
            "status": status
        }

    except Exception as e:
        return {"url": url, "ip": ip_address, "avg_latency_ms": None, "packet_loss_percent": None, "status": f"PING_ERROR: {e}"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python latency.py <url>")
        sys.exit(1)
    url_to_check = sys.argv[1]
    print(check_latency(url_to_check))