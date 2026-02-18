import re


# -----------------------------
# Extract company info
# -----------------------------
def extract_metadata(text):

    cin = None
    company = None
    year = None

    cin_match = re.search(r"[A-Z]{1}\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}", text)
    if cin_match:
        cin = cin_match.group()

    company_match = re.search(r"([A-Z][A-Za-z\s]+Limited)", text)
    if company_match:
        company = company_match.group().strip()

    year_match = re.search(r"20\d{2}[-–]?\d{2}", text)
    if year_match:
        year = year_match.group()

    return {
        "cin": cin,
        "company_name": company,
        "year": year
    }


# -----------------------------
# Detect table title
# -----------------------------
def detect_title(markdown, idx):
    if not markdown:
        return f"table_{idx}"

    lines = markdown.split("\n")

    for i, line in enumerate(lines):
        if "|" in line:
            if i > 0:
                return lines[i - 1].strip()

    return f"table_{idx}"


# -----------------------------
# Normalize headers
# -----------------------------
def normalize_header(h):
    h = h.lower()

    if "particular" in h:
        return "particular"
    if "note" in h:
        return "note"
    if "mar" in h or "202" in h:
        if "25" in h:
            return "2024_25"
        if "24" in h:
            return "2023_24"

    return h.strip()


# -----------------------------
# Parse table → structured rows
# -----------------------------
def parse_table(table):

    rows = table.get("rows", [])
    if len(rows) < 2:
        return None

    header = rows[0]
    header = [normalize_header(h) for h in header]

    parsed_rows = []

    for row in rows[1:]:
        entry = {}

        for i in range(min(len(row), len(header))):
            key = header[i]
            value = row[i].strip()

            if key:
                entry[key] = value

        if len(entry) > 1:
            parsed_rows.append(entry)

    return parsed_rows


# -----------------------------
# Detect section type
# -----------------------------
def classify_table(title):

    t = title.lower()

    if "balance sheet" in t:
        return "balance_sheet"
    if "profit" in t or "loss" in t:
        return "profit_loss"
    if "cash flow" in t:
        return "cash_flow"

    return "other"


# -----------------------------
# MAIN BUILDER
# -----------------------------
def build_gt_like_json(result):

    text = result.get("text", "")
    tables = result.get("tables", [])
    markdown = result.get("markdown", "")

    metadata = extract_metadata(text)

    structured_tables = []

    for i, table in enumerate(tables):

        parsed = parse_table(table)
        if not parsed:
            continue

        title = detect_title(markdown, i)

        structured_tables.append({
            "title": title,
            "type": classify_table(title),
            "rows": parsed
        })

    return {
        **metadata,
        "tables": structured_tables
    }
