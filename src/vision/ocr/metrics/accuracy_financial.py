import re
from typing import Any, Dict, List


# ------------------------------------------------
# BASIC HELPERS
# ------------------------------------------------
def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def normalize_number(n: str) -> str:
    return re.sub(r"[^\d.]", "", n)


def extract_numbers(text: str) -> List[str]:
    return [normalize_number(x) for x in re.findall(r"\d[\d,\.]*", text)]


# ------------------------------------------------
# NUMERIC MATCH SCORE
# ------------------------------------------------
def numeric_overlap(gt: str, pred: str):

    gt_nums = extract_numbers(gt)
    pred_nums = extract_numbers(pred)

    matched = sum(1 for n in gt_nums if n in pred_nums)
    total = len(gt_nums)

    return matched / total if total else 0


# ------------------------------------------------
# TABLE PARSER FROM MARKDOWN
# ------------------------------------------------
def parse_markdown_table(md: str):

    rows = []

    for line in md.splitlines():
        if "|" in line:
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if cells:
                rows.append(cells)

    return rows


# ------------------------------------------------
# STRUCTURE SCORE
# ------------------------------------------------
def structure_score(gt_rows, pred_rows):

    if not gt_rows or not pred_rows:
        return 0

    return min(len(pred_rows), len(gt_rows)) / max(len(pred_rows), len(gt_rows))


# ------------------------------------------------
# ROW MATCH SCORE
# ------------------------------------------------
def row_score(gt_rows, pred_rows):

    if not gt_rows:
        return 0

    matched = 0

    for gt in gt_rows:
        gt_line = " ".join(gt)

        for pr in pred_rows:
            pr_line = " ".join(pr)
            if normalize(gt_line) in normalize(pr_line):
                matched += 1
                break

    return matched / len(gt_rows)


# ------------------------------------------------
# COLUMN SCORE
# ------------------------------------------------
def column_score(gt_rows, pred_rows):

    if not gt_rows or not pred_rows:
        return 0

    gt_cols = max(len(r) for r in gt_rows)
    pr_cols = max(len(r) for r in pred_rows)

    return min(gt_cols, pr_cols) / max(gt_cols, pr_cols)


# ======================================================
# AUTO ADAPTIVE FINANCIAL METRIC
# ======================================================
def financial_accuracy_report(gt_json: Any, ocr_output: str) -> Dict:

    # =====================================================
    # WORD-LEVEL DATASET
    # =====================================================
    if isinstance(gt_json, list):

        gt_text = " ".join(
            item["text"]
            for item in gt_json
            if "text" in item
        )

        num_score = numeric_overlap(gt_text, ocr_output)

        return {
            "mode": "word_level",
            "numeric_score": round(num_score,4),
            "structure_score": None,
            "row_score": None,
            "column_score": None,
            "financial_overall_score": round(num_score,4)
        }


    # =====================================================
    # STRUCTURED TABLE FORMAT
    # =====================================================
    if isinstance(gt_json, dict) and "tables" in gt_json:

        table = gt_json["tables"][0]

        # ---------- HTML FORMAT ----------
        if "html" in table:

            gt_rows = parse_markdown_table(table["html"])
            pred_rows = parse_markdown_table(ocr_output)

            gt_text = table["html"]

        # ---------- CELL FORMAT ----------
        elif "cells" in table:

            gt_rows = []
            current = []

            for c in table["cells"]:
                current.append(str(c.get("value","")))
                if c.get("end_row"):
                    gt_rows.append(current)
                    current = []

            pred_rows = parse_markdown_table(ocr_output)
            gt_text = " ".join(sum(gt_rows,[]))

        else:
            return {"mode":"unknown_table_format","financial_overall_score":0}

        # ---------- SCORES ----------
        num = numeric_overlap(gt_text, ocr_output)
        struct = structure_score(gt_rows, pred_rows)
        row = row_score(gt_rows, pred_rows)
        col = column_score(gt_rows, pred_rows)

        final = (
            num*0.4 +
            struct*0.2 +
            row*0.2 +
            col*0.2
        )

        return {
            "mode":"table_evaluation",
            "numeric_score": round(num,4),
            "structure_score": round(struct,4),
            "row_score": round(row,4),
            "column_score": round(col,4),
            "financial_overall_score": round(final,4)
        }


    # =====================================================
    # ROOT HTML FORMAT
    # =====================================================
    if isinstance(gt_json, dict) and "html" in gt_json:

        num = numeric_overlap(gt_json["html"], ocr_output)

        return {
            "mode":"root_html",
            "financial_overall_score": round(num,4)
        }


    # =====================================================
    # UNKNOWN FORMAT
    # =====================================================
    return {
        "mode":"unsupported_format",
        "financial_overall_score":0
    }
