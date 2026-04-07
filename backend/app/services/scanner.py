from concurrent.futures import ThreadPoolExecutor
from app.services.xss_scanner import check_xss
from app.services.headers_scanner import check_headers
from app.services.sql_scanner import scan_sql_injection
from app.utils.risk_calculator import calculate_risk

def run_scan(url):
    all_vulnerabilities = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_xss = executor.submit(check_xss, url)
        future_headers = executor.submit(check_headers, url)
        future_sql = executor.submit(scan_sql_injection, url)

        xss_result = future_xss.result()
        headers_result = future_headers.result()
        sql_results = future_sql.result()

    all_vulnerabilities.append(xss_result)
    all_vulnerabilities.append(headers_result)
    all_vulnerabilities.extend(sql_results)

    # Unpack risk
    risk_score, risk_level = calculate_risk(all_vulnerabilities)

    print("Scan result:", {
        "vulnerabilities": all_vulnerabilities,
        "risk_score": risk_score,
        "overall_severity": risk_level
    })

    return {
        "vulnerabilities": all_vulnerabilities,
        "risk_score": risk_score,
        "overall_severity": risk_level
    }