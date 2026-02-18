# Layout Accuracy Evaluation

A lightweight Python utility for evaluating layout understanding models by comparing predicted layout blocks against ground truth annotations using Intersection over Union (IoU) matching.

## Overview

This module provides functions to compute layout accuracy metrics by matching predicted document layout elements (text blocks, images, tables, etc.) with ground truth annotations. It uses IoU-based matching followed by category classification evaluation.

## Functions

### `bbox_iou(boxA, boxB)`

Computes the Intersection over Union (IoU) between two bounding boxes.

**Parameters:**
- `boxA`, `boxB` (*list*): Bounding boxes in format `[x, y, width, height]` where:
  - `x, y`: Top-left coordinates
  - `width, height`: Box dimensions

**Returns:**
- *float*: IoU value between 0 and 1 (0 if no overlap)

### `evaluate_layout(gt_blocks, pred_blocks, iou_threshold=0.5)`

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

## Usage Example

```python
# Ground truth blocks
gt_blocks = [
    {"bbox": [10, 20, 100, 50], "category": "text"},
    {"bbox": [150, 30, 200, 80], "category": "image"}
]

# Predicted blocks
pred_blocks = [
    {"bbox": [12, 22, 98, 48], "category": "text"},
    {"bbox": [155, 35, 195, 75], "category": "table"}
]

# Evaluate
results = evaluate_layout(gt_blocks, pred_blocks, iou_threshold=0.5)
print(results)
# Output: {'layout_total_blocks': 2, 'layout_matched_blocks': 2, 'layout_classification_accuracy': 0.5}

```

# Metrics Explained

    Matched Blocks: Count of ground truth blocks that have a predicted block with IoU ≥ threshold

    Classification Accuracy: Among matched blocks, proportion where the predicted category matches the ground truth category

    Note: If multiple predictions overlap a ground truth block, only the highest IoU prediction is considered

    box coordinates are assumed to be in absolute pixel values or normalized coordinates (as long as consistent)

    The matching algorithm is greedy: each ground truth block matches with its highest IoU prediction

    Multiple ground truth blocks can match to the same prediction (no one-to-one enforcement)
