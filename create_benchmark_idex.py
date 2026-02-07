# create_benchmark_index.py
import json
from pathlib import Path
from datetime import datetime

benchmark_config = {
    "name": "T0.3 OCR Reliability Benchmarks",
    "version": "1.0",
    "created": datetime.now().isoformat(),
    "description": "Benchmarks for validating OCR reliability before processing real-world reports",
    "benchmarks": {
        "fintabnet": {
            "type": "table_structure",
            "split": "validation",
            "ground_truth": "data/benchmarks/fintabnet/gt_json/FinTabNet_OTSL_val.json",
            "description": "Financial tables for table structure recognition testing",
            "metrics": ["table_detection_accuracy", "cell_recognition_accuracy"]
        },
        "doclaynet": {
            "type": "document_layout",
            "split": "validation", 
            "ground_truth": "data/benchmarks/doclaynet/gt_json/DocLayNet_val.json",
            "description": "Complex document layouts for layout analysis testing",
            "metrics": ["layout_parsing_accuracy", "region_detection_f1"]
        },
        "icdar2013": {
            "type": "text_recognition",
            "split": "validation",
            "ground_truth": "data/benchmarks/icdar2013/gt_json/ICDAR2013_val.json",
            "description": "Clean text documents for OCR baseline testing",
            "metrics": ["character_recognition_rate", "word_accuracy"]
        }
    },
    "evaluation_script": "evaluate_ocr_reliability.py",
    "requirements": [
        "All ground truth files must be valid JSON",
        "Each benchmark should have > 1000 samples",
        "Evaluation metrics must be reproducible"
    ]
}

# Save config
config_path = Path("data/benchmarks/benchmark_config.json")
config_path.parent.mkdir(parents=True, exist_ok=True)

with open(config_path, "w") as f:
    json.dump(benchmark_config, f, indent=2)

print(f"✅ Created benchmark config: {config_path}")
print(f"\n📋 Configuration:")
print(f"   • Benchmarks: {len(benchmark_config['benchmarks'])}")
for name, config in benchmark_config["benchmarks"].items():
    print(f"   • {name}: {config['description']}")