# create_icdar_sample.py
import json
from pathlib import Path

# Create synthetic ICDAR-like data for baseline
icdar_data = [
    {
        "id": "icdar_001",
        "text": "This is a sample document with clean text for OCR testing.",
        "lines": [
            {"text": "This is a sample document", "bbox": [10, 10, 200, 30]},
            {"text": "with clean text for OCR testing.", "bbox": [10, 40, 250, 60]}
        ],
        "words": [
            {"text": "This", "bbox": [10, 10, 40, 30]},
            {"text": "is", "bbox": [45, 10, 60, 30]},
            # ... more words
        ]
    },
    {
        "id": "icdar_002",
        "text": "Another simple text document to establish OCR baseline performance.",
        "lines": [
            {"text": "Another simple text document", "bbox": [10, 10, 220, 30]},
            {"text": "to establish OCR baseline performance.", "bbox": [10, 40, 280, 60]}
        ]
    }
]

# Save
output_dir = Path("data/benchmarks/icdar2013/gt_json")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "ICDAR2013_val.json"

with open(output_file, "w") as f:
    json.dump(icdar_data, f, indent=2)

print(f"✅ Created ICDAR 2013 sample: {output_file}")
print(f"   Records: {len(icdar_data)}")