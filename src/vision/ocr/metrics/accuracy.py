from jiwer import cer, wer
from rapidfuzz.distance import Levenshtein
import re

def normalize_text(text: str) -> str:
    """
    Strong normalization to reduce layout-induced CER inflation.
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"-\n", "", text)        # fix hyphenated line breaks
    text = re.sub(r"\n+", "\n", text)      # collapse multiple newlines
    text = re.sub(r"[^\w\s]", "", text)    # remove punctuation
    text = re.sub(r"\s+", " ", text)       # normalize spaces
    return text.strip()


def compute_cer(ground_truth: str, ocr_text: str) -> float:
    ground_truth = normalize_text(ground_truth)
    ocr_text = normalize_text(ocr_text)
    return round(cer(ground_truth, ocr_text), 4)



def compute_wer(ground_truth: str, ocr_text: str) -> float:
    ground_truth = normalize_text(ground_truth)
    ocr_text = normalize_text(ocr_text)
    return round(wer(ground_truth, ocr_text), 4)



def character_accuracy(ground_truth: str, ocr_text: str) -> float:
    ground_truth = normalize_text(ground_truth)
    ocr_text = normalize_text(ocr_text)

    dist = Levenshtein.distance(ground_truth, ocr_text)
    return round(1 - dist / max(len(ground_truth), 1), 4)


def accuracy_report(ground_truth: str, ocr_text: str) -> dict:
    """
    Unified OCR accuracy report
    """
    return {
        "CER": compute_cer(ground_truth, ocr_text),
        "WER": compute_wer(ground_truth, ocr_text),
        "Char_Accuracy": character_accuracy(ground_truth, ocr_text)
    }
