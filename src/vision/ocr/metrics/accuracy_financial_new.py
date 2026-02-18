import re
from typing import Any, Dict, List


# ============================================================
# Normalization
# ============================================================

def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def normalize_number(n: str) -> str:
    return re.sub(r"[^\d\.-]", "", n)


# ============================================================
# Recursive Extraction
# ============================================================

def extract_all_numbers(obj: Any) -> List[str]:
    numbers = []

    if isinstance(obj, dict):
        for v in obj.values():
            numbers.extend(extract_all_numbers(v))

    elif isinstance(obj, list):
        for item in obj:
            numbers.extend(extract_all_numbers(item))

    elif isinstance(obj, str):
        found = re.findall(r"-?\d[\d,\.]*", obj)
        numbers.extend(found)

    elif isinstance(obj, (int, float)):
        numbers.append(str(obj))

    return numbers


def extract_all_text(obj: Any) -> List[str]:
    texts = []

    if isinstance(obj, dict):
        for v in obj.values():
            texts.extend(extract_all_text(v))

    elif isinstance(obj, list):
        for item in obj:
            texts.extend(extract_all_text(item))

    elif isinstance(obj, str):
        t = obj.strip()
        if t:
            texts.append(t)

    return texts


# ============================================================
# Financial Accuracy
# ============================================================

def financial_accuracy_report(gt_json: Dict[str, Any], ocr_text: str) -> Dict[str, Any]:

    normalized_ocr = normalize_text(ocr_text)
    normalized_ocr_numbers = normalize_number(ocr_text)

    # --------------------------------------------------------
    # Numeric Accuracy
    # --------------------------------------------------------

    gt_numbers = extract_all_numbers(gt_json)
    gt_numbers = [normalize_number(n) for n in gt_numbers if normalize_number(n)]

    total_numbers = len(gt_numbers)
    matched_numbers = sum(
        1 for n in gt_numbers if n and n in normalized_ocr_numbers
    )

    numeric_accuracy = matched_numbers / total_numbers if total_numbers else 0


    # --------------------------------------------------------
    # Line Item Accuracy
    # --------------------------------------------------------

    gt_texts = extract_all_text(gt_json)
    gt_texts = [normalize_text(t) for t in gt_texts if len(t.strip()) > 3]

    total_items = len(gt_texts)
    matched_items = sum(
        1 for t in gt_texts if t in normalized_ocr
    )

    line_item_accuracy = matched_items / total_items if total_items else 0


    # --------------------------------------------------------
    # Section Accuracy
    # --------------------------------------------------------

    required_sections = [
        "balance sheet",
        "statement of profit and loss",
        "cash flow",
        "auditor"
    ]

    matched_sections = sum(
        1 for sec in required_sections if sec in normalized_ocr
    )

    section_accuracy = matched_sections / len(required_sections)


    # --------------------------------------------------------
    # Disclosure Accuracy
    # --------------------------------------------------------

    disclosure_keywords = [
        "true and fair",
        "for the year ended",
        "earnings per equity share",
        "as at march"
    ]

    matched_disclosures = sum(
        1 for d in disclosure_keywords if d in normalized_ocr
    )

    disclosure_accuracy = matched_disclosures / len(disclosure_keywords)


    # --------------------------------------------------------
    # Final Score (Weighted)
    # --------------------------------------------------------

    final_score = (
        numeric_accuracy * 0.4 +
        line_item_accuracy * 0.2 +
        section_accuracy * 0.2 +
        disclosure_accuracy * 0.2
    )

    return {
        "numeric_accuracy": round(numeric_accuracy, 4),
        "line_item_accuracy": round(line_item_accuracy, 4),
        "section_accuracy": round(section_accuracy, 4),
        "disclosure_accuracy": round(disclosure_accuracy, 4),
        "financial_overall_score": round(final_score, 4)
    }
 

