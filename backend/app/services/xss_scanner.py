import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ✅ Create reusable session with retry
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


# ✅ Normalize URL
def normalize_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url


# ✅ XSS Scanner
def check_xss(url):
    url = normalize_url(url)
    session = create_session()

    payloads = [
        "<script>alert('xss')</script>",
        "'><script>alert(1)</script>",
        "<img src=x onerror=alert(1)>"
    ]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        for payload in payloads:
            test_url = f"{url}?q={payload}"

            response = session.get(
                test_url,
                headers=headers,
                timeout=5,
                verify=False
            )

            if payload.lower() in response.text.lower():
                return {
                    "type": "XSS",
                    "severity": "High",
                    "description": f"Reflected XSS detected using payload: {payload}",
                    "fix": "Sanitize inputs and use output encoding"
                }

    except requests.exceptions.ConnectTimeout:
        return {
            "type": "XSS",
            "severity": "Error",
            "description": "Connection timed out"
        }

    except requests.exceptions.RequestException as e:
        return {
            "type": "XSS",
            "severity": "Error",
            "description": str(e)
        }

    return {
        "type": "XSS",
        "severity": "Low",
        "description": "No XSS detected",
        "fix": "No action needed"
    }