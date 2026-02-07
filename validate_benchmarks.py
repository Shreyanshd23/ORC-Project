import json
from pathlib import Path
import os

print("=" * 80)
print("T0.3 BENCHMARK VALIDATION")
print("=" * 80)

benchmarks = {
    "fintabnet": {
        "gt_path": "data/benchmarks/fintabnet/gt_json/FinTabNet_OTSL_val.json",
        "description": "Table-heavy financial documents",
        "expected_min_records": 10000,
        "expected_keys": ['otsl', 'html', 'html_restored', 'cols', 'rows', 'filename', 'imgid']
    },
    "doclaynet": {
        "gt_path": "data/benchmarks/doclaynet/gt_json/DocLayNet_val.json", 
        "description": "Complex layout documents",
        "expected_min_records": 1000,
        "expected_keys": None  # Will check based on format
    }
    # icdar2013 will be added later
}

print("🔍 Validating benchmark datasets...")
print()

all_valid = True

for benchmark_name, config in benchmarks.items():
    gt_path = Path(config["gt_path"])
    
    print(f"📊 {benchmark_name.upper()} - {config['description']}")
    print(f"   Ground truth path: {gt_path}")
    
    # Check if file exists
    if not gt_path.exists():
        print(f"   ❌ MISSING: File not found!")
        all_valid = False
        print()
        continue
    
    # Check file size
    size_mb = os.path.getsize(gt_path) / (1024*1024)
    print(f"   📏 File size: {size_mb:.2f} MB")
    
    # Try to load JSON
    try:
        with open(gt_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"   ✅ JSON loaded successfully")
        
        # Check data type and count
        if isinstance(data, list):
            record_count = len(data)
            print(f"   📊 Records: {record_count:,}")
            
            if record_count < config["expected_min_records"]:
                print(f"   ⚠️  WARNING: Low record count (expected > {config['expected_min_records']:,})")
            
            if data and config["expected_keys"]:
                first_record = data[0]
                actual_keys = list(first_record.keys())
                print(f"   🔑 Keys in first record: {actual_keys}")
                
                # Check if expected keys are present
                missing_keys = [k for k in config["expected_keys"] if k not in actual_keys]
                if missing_keys:
                    print(f"   ⚠️  WARNING: Missing expected keys: {missing_keys}")
        
        elif isinstance(data, dict):
            print(f"   📊 Dictionary format")
            print(f"   🔑 Keys: {list(data.keys())}")
            
            # Check for COCO format
            if 'images' in data and 'annotations' in data:
                print(f"   🖼️  COCO format detected")
                print(f"     Images: {len(data['images']):,}")
                print(f"     Annotations: {len(data['annotations']):,}")
                if 'categories' in data:
                    print(f"     Categories: {len(data['categories']):,}")
        
        # Quick sample
        if isinstance(data, list) and data:
            sample = data[0]
            print(f"   📝 Sample preview:")
            for key, value in list(sample.items())[:3]:  # Show first 3 items
                if isinstance(value, str) and len(value) > 50:
                    print(f"     {key}: {value[:50]}...")
                elif isinstance(value, list):
                    print(f"     {key}: List[{len(value)} items]")
                elif isinstance(value, dict):
                    print(f"     {key}: Dict[{len(value)} keys]")
                else:
                    print(f"     {key}: {type(value).__name__}")
        
    except Exception as e:
        print(f"   ❌ ERROR loading JSON: {e}")
        all_valid = False
    
    print()

print("=" * 80)
print("VALIDATION SUMMARY:")
print("=" * 80)

if all_valid:
    print("✅ ALL BENCHMARKS VALID AND READY!")
    
else:
    print("❌ SOME BENCHMARKS NEED ATTENTION")
    print("\n🔧 Required fixes:")
    print("   • Ensure all ground truth files exist")
    print("   • Fix any JSON loading errors")
    print("   • Verify minimum record counts")

print("=" * 80)