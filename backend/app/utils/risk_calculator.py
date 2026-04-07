def calculate_risk(vulnerabilities):
    score = 0

    for vuln in vulnerabilities:
        sev = vuln.get("severity", "").lower()
        if sev == "high":
            score += 3
        elif sev == "medium":
            score += 2
        elif sev == "low":
            score += 1
        elif sev == "error":  
            score += 2

    # Determine overall level
    if score >= 6:
        severity = "High"
    elif score >= 3:
        severity = "Medium"
    else:
        severity = "Low"

    return score, severity