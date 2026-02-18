import easyocr
import numpy as np
import re
from metrics.accuracy import accuracy_report

reader = easyocr.Reader(['en'], gpu=False)


def run_easyocr(image):
    image_np = np.array(image)
    results = reader.readtext(image_np)

    text = " ".join([res[1] for res in results])
    return text


def preprocess_text(text: str):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def evaluate_text(gt_text: str, pred_text: str):
    return accuracy_report(
        preprocess_text(gt_text),
        preprocess_text(pred_text)
    )
