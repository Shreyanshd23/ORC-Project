from typing import List, Dict


def bbox_iou(boxA, boxB):
    """
    Compute Intersection over Union between two boxes.
    box format: [x, y, width, height]
    """

    ax1, ay1, aw, ah = boxA
    bx1, by1, bw, bh = boxB

    ax2, ay2 = ax1 + aw, ay1 + ah
    bx2, by2 = bx1 + bw, by1 + bh

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_w = max(0, inter_x2 - inter_x1)
    inter_h = max(0, inter_y2 - inter_y1)

    inter_area = inter_w * inter_h
    areaA = aw * ah
    areaB = bw * bh

    union = areaA + areaB - inter_area

    return inter_area / union if union else 0


def evaluate_layout(
    gt_blocks: List[Dict],
    pred_blocks: List[Dict],
    iou_threshold: float = 0.5
):
    """
    Match predicted layout blocks to GT using IoU.
    Evaluate category classification accuracy.
    """

    matched = 0
    correct_class = 0

    for gt in gt_blocks:

        best_iou = 0
        best_pred = None

        for pred in pred_blocks:
            iou = bbox_iou(gt["bbox"], pred["bbox"])
            if iou > best_iou:
                best_iou = iou
                best_pred = pred

        if best_iou >= iou_threshold and best_pred:
            matched += 1
            if best_pred["category"] == gt["category"]:
                correct_class += 1

    total = len(gt_blocks)

    return {
        "layout_total_blocks": total,
        "layout_matched_blocks": matched,
        "layout_classification_accuracy":
            round(correct_class / total, 4) if total else 0
    }
   
