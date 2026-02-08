from jiwer import cer, wer
from rapidfuzz.distance import Levenshtein
import re
from typing import Dict


# -----------------------------
# Normalization
# -----------------------------
def normalize_text(text: str) -> str:
    """
    Strong normalization to reduce layout-induced CER/WER inflation.
    Intended for OCR benchmarking, not semantic comparison.
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"-\n", "", text)        # fix hyphenated line breaks
    text = re.sub(r"\n+", "\n", text)      # collapse multiple newlines
    text = re.sub(r"[^\w\s]", "", text)    # remove punctuation
    text = re.sub(r"\s+", " ", text)       # normalize spaces
    return text.strip()


# -----------------------------
# Metrics
# -----------------------------
def compute_cer(ground_truth: str, ocr_text: str) -> float:
    """
    Character Error Rate (CER)
    """
    gt = normalize_text(ground_truth)
    pred = normalize_text(ocr_text)

    if not gt:
        return 0.0

    return round(cer(gt, pred), 4)


def compute_wer(ground_truth: str, ocr_text: str) -> float:
    """
    Word Error Rate (WER)
    """
    gt = normalize_text(ground_truth)
    pred = normalize_text(ocr_text)

    if not gt:
        return 0.0

    return round(wer(gt, pred), 4)


def character_accuracy(ground_truth: str, ocr_text: str) -> float:
    """
    Character-level accuracy (1 - normalized Levenshtein distance)
    """
    gt = normalize_text(ground_truth)
    pred = normalize_text(ocr_text)

    if not gt:
        return 0.0

    dist = Levenshtein.distance(gt, pred)
    return round(1 - dist / max(len(gt), 1), 4)


# -----------------------------
# Unified report
# -----------------------------
def accuracy_report(ground_truth: str, ocr_text: str) -> Dict[str, float]:
    """
    Unified OCR accuracy report.
    """
    return {
        "CER": compute_cer(ground_truth, ocr_text),
        "WER": compute_wer(ground_truth, ocr_text),
        "Char_Accuracy": character_accuracy(ground_truth, ocr_text),
    }
