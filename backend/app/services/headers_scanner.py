import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_session():
    session = requests.Session()

    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def normalize_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url


def check_headers(url):
    url = normalize_url(url)
    session = create_session()

    headers_req = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = session.get(
            url,
            headers=headers_req,
            timeout=5,
            verify=False
        )

        headers = response.headers
        missing = []

        security_headers = [
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Strict-Transport-Security"
        ]

        for h in security_headers:
            if h not in headers:
                missing.append(h)

        if missing:
            return {
                "type": "Headers",
                "severity": "Medium",
                "description": f"Missing headers: {', '.join(missing)}",
                "fix": "Add recommended security headers"
            }

    except requests.exceptions.ConnectTimeout:
        return {
            "type": "Headers",
            "severity": "Error",
            "description": "Connection timed out"
        }

    except requests.exceptions.RequestException as e:
        return {
            "type": "Headers",
            "severity": "Error",
            "description": str(e)
        }

    return {
        "type": "Headers",
        "severity": "Low",
        "description": "All important headers present",
        "fix": "No action needed"
    }