# Document Layout and Content Evaluation Suite

A comprehensive evaluation toolkit for document understanding systems, providing metrics for layout accuracy, compliance validation, and financial content extraction quality.

## Overview

This suite consists of three complementary modules for evaluating different aspects of document processing:

1. **Layout Accuracy** (`layout_accuracy.py`): Evaluates spatial understanding using bounding box IoU matching
2. **Compliance Rules** (`compliance_rules.py`): Validates presence of required financial sections and tables
3. **Financial Accuracy** (`accuracy_financial.py`): Measures numeric and structural accuracy of extracted financial data

---

# Module 1: Layout Accuracy Evaluation

## `layout_accuracy.py`

Lightweight utility for evaluating layout understanding models by comparing predicted layout blocks against ground truth annotations using Intersection over Union (IoU) matching.

### Functions

#### `bbox_iou(boxA, boxB)`

Computes the Intersection over Union (IoU) between two bounding boxes.

**Parameters:**
- `boxA`, `boxB` (*list*): Bounding boxes in format `[x, y, width, height]` where:
  - `x, y`: Top-left coordinates
  - `width, height`: Box dimensions

**Returns:**
- *float*: IoU value between 0 and 1 (0 if no overlap)

#### `evaluate_layout(gt_blocks, pred_blocks, iou_threshold=0.5)`

Matches predicted layout blocks to ground truth using IoU and evaluates classification accuracy.

**Parameters:**
- `gt_blocks` (*List[Dict]*): Ground truth blocks, each containing:
  - `bbox`: Bounding box coordinates `[x, y, width, height]`
  - `category`: Block category/class label
- `pred_blocks` (*List[Dict]*): Predicted blocks with same structure as above
- `iou_threshold` (*float*, optional): Minimum IoU to consider a match. Default: 0.5

**Returns:**
- *Dict*: Evaluation metrics containing:
  - `layout_total_blocks`: Total number of ground truth blocks
  - `layout_matched_blocks`: Number of ground truth blocks matched with predictions
  - `layout_classification_accuracy`: Accuracy of category classification for matched blocks

### Usage Example

```python
from layout_accuracy import evaluate_layout

gt_blocks = [
    {"bbox": [10, 20, 100, 50], "category": "text"},
    {"bbox": [150, 30, 200, 80], "category": "image"}
]

pred_blocks = [
    {"bbox": [12, 22, 98, 48], "category": "text"},
    {"bbox": [155, 35, 195, 75], "category": "table"}
]

results = evaluate_layout(gt_blocks, pred_blocks, iou_threshold=0.5)
print(results)
# Output: {'layout_total_blocks': 2, 'layout_matched_blocks': 2, 'layout_classification_accuracy': 0.5}
```