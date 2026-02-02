import argparse
from pathlib import Path
from rapidfuzz.distance import Levenshtein

def normalize_text(text: str) -> str:
    """
    Normalize text by removing Markdown artifacts, extra whitespace.
    """
    import re
    
    # Remove Markdown headers (## )
    text = re.sub(r'#+\s+', '', text)
    # Remove bold/italic (** or *)
    text = re.sub(r'\*\*|__', '', text)
    # Remove image placeholders
    text = re.sub(r'<!-- image -->', '', text)
    
    # Normalize quotes (typographic to straight)
    text = text.replace("”", '"').replace("“", '"')
    text = text.replace("’", "'").replace("‘", "'")
    # Normalize single quotes to be consistent
    # WARNING: This is aggressive but useful for plain text validation.
    text = text.replace("'", '"')

    # Normalize ordinal dates (31 st -> 31st)
    text = re.sub(r'(\d+)\s+(st|nd|rd|th)', r'\1\2', text, flags=re.IGNORECASE)
    
    # Replace multiple newlines/spaces with single space
    text = " ".join(text.split())
    return text.strip()

def calculate_metrics(gt_text: str, pred_text: str):
    """
    Calculate Character Error Rate (CER) and Word Error Rate (WER).
    """
    # CER: Levenshtein distance on characters / length of ground truth
    char_dist = Levenshtein.distance(gt_text, pred_text)
    cer = char_dist / max(len(gt_text), 1)

    # WER: Levenshtein distance on words / length of ground truth word list
    gt_words = gt_text.split()
    pred_words = pred_text.split()
    word_dist = Levenshtein.distance(gt_words, pred_words)
    wer = word_dist / max(len(gt_words), 1)

    return {
        "CER": cer,
        "WER": wer,
        "char_distance": char_dist,
        "word_distance": word_dist,
        "gt_len_chars": len(gt_text),
        "gt_len_words": len(gt_words)
    }

def main():
    parser = argparse.ArgumentParser(description="Benchmark OCR accuracy against Ground Truth.")
    parser.add_argument("--ground-truth", "-gt", required=True, help="Path to Ground Truth text file.")
    parser.add_argument("--prediction", "-p", required=True, help="Path to OCR output file (Markdown/Text).")
    
    args = parser.parse_args()
    
    gt_path = Path(args.ground_truth)
    pred_path = Path(args.prediction)
    
    if not gt_path.exists():
        print(f"Error: Ground Truth file {gt_path} not found.")
        return
    if not pred_path.exists():
        print(f"Error: Prediction file {pred_path} not found.")
        return
        
    try:
        with open(gt_path, "r", encoding="utf-8") as f:
            gt_content = f.read()
        
        with open(pred_path, "r", encoding="utf-8") as f:
            pred_content = f.read()
            
        # 1. Strict Comparison (Checking formatting preservation)
        metrics_strict = calculate_metrics(gt_content, pred_content)
        
        # 2. Normalized Comparison (Checking content accuracy ignoring layout whitespace)
        metrics_norm = calculate_metrics(normalize_text(gt_content), normalize_text(pred_content))
        
        print("-" * 50)
        print(f"BENCHMARK REPORT: {pred_path.name}")
        print("-" * 50)
        print(f"Ground Truth Size: {metrics_strict['gt_len_chars']} chars, {metrics_strict['gt_len_words']} words")
        print("\n[STRICT METRICS] (Includes formatting differences)")
        print(f"  CER: {metrics_strict['CER']:.4%}")
        print(f"  WER: {metrics_strict['WER']:.4%}")
        
        print("\n[NORMALIZED METRICS] (Content accuracy only)")
        print(f"  CER: {metrics_norm['CER']:.4%}")
        print(f"  WER: {metrics_norm['WER']:.4%}")
        print("-" * 50)
        
        # Pass/Fail Criteria (Arbitrary threshold for now: <2% CER normalized)
        if metrics_norm['CER'] < 0.02:
             print("✅ RESULT: PASS (High Accuracy)")
        else:
             print("❌ RESULT: FAIL (Needs Improvement)")
             print("   (Check for encoding issues or layout misinterpretation)")

    except Exception as e:
        print(f"Error calculating metrics: {e}")

if __name__ == "__main__":
    main()
