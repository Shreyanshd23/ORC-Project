def validate_compliance(gt_json: dict, ocr_text: str):

    results = []
    text_lower = ocr_text.lower()

    required_sections = [
        "balance sheet",
        "statement of profit and loss",
        "cash flow",
        "auditor"
    ]

    for section in required_sections:
        results.append({
            "rule": f"{section.title()} Present",
            "status": "PASS" if section in text_lower else "FAIL"
        })

    if "tables" in gt_json:
        for table in gt_json.get("tables", []):
            title = str(table.get("title", "")).lower()
            if title:
                results.append({
                    "rule": f"Table Detected: {title}",
                    "status": "PASS" if title in text_lower else "FAIL"
                })

    return results