from .utils import make_request
import time

def check_performance(url):
    """Measures the performance metrics of a URL."""
    start_time = time.time()
    response = make_request(url)
    end_time = time.time()

    if response:
        total_time = end_time - start_time
        ttfb = response.elapsed.total_seconds()
        content_length = len(response.content)
        content_download_time = total_time - ttfb
        return {
            "url": url,
            "total_time_seconds": f"{total_time:.2f}",
            "ttfb_seconds": f"{ttfb:.2f}",
            "content_download_time_seconds": f"{content_download_time:.2f}",
            "content_length_bytes": content_length,
            "status_code": response.status_code,
            "status": "OK"
        }
    return {"url": url, "total_time_seconds": None, "ttfb_seconds": None, "content_download_time_seconds": None, "content_length_bytes": None, "status_code": None, "status": "FAILED"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python performance.py <url>")
        sys.exit(1)
    url_to_check = sys.argv[1]
    print(check_performance(url_to_check))