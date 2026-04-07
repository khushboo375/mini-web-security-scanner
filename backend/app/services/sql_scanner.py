import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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


def scan_sql_injection(url):
    url = normalize_url(url)
    session = create_session()

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    vulnerabilities = []

    payloads = [
        "' OR '1'='1",
        "' OR 1=1--",
        "' OR 'a'='a",
        "'; DROP TABLE users;--"
    ]

    error_signatures = [
        "sql syntax",
        "mysql",
        "syntax error",
        "unclosed quotation",
        "database error",
        "warning",
        "odbc",
        "pdo"
    ]

    try:
        for payload in payloads:
            test_url = f"{url}?id={payload}"

            response = session.get(
                test_url,
                headers=headers,
                timeout=5,
                verify=False
            )

            response_text = response.text.lower()

            for error in error_signatures:
                if error in response_text:
                    vulnerabilities.append({
                        "type": "SQL Injection",
                        "severity": "High",
                        "description": f"Possible SQL Injection using payload: {payload}",
                        "fix": "Use parameterized queries (prepared statements)"
                    })
                    return vulnerabilities

    except requests.exceptions.ConnectTimeout:
        vulnerabilities.append({
            "type": "SQL Injection",
            "severity": "Error",
            "description": "Connection timed out"
        })

    except requests.exceptions.RequestException as e:
        vulnerabilities.append({
            "type": "SQL Injection",
            "severity": "Error",
            "description": str(e)
        })

    if not vulnerabilities:
        vulnerabilities.append({
            "type": "SQL Injection",
            "severity": "Low",
            "description": "No SQL Injection detected",
            "fix": "No action needed"
        })

    return vulnerabilities