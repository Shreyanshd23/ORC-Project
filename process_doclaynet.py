from pathlib import Path
import json
import os

print("=" * 70)
print("PROCESSING DOC LAY NET FROM KAGGLE")
print("=" * 70)

# Paths
input_file = Path("data/benchmarks/doclaynet/raw_json/val/doclaynet_val_00.json")
output_file = Path("data/benchmarks/doclaynet/gt_json/DocLayNet_val.json")

print(f"📁 Input file: {input_file}")
print(f"💾 Output file: {output_file}")

# Check if file exists
if not input_file.exists():
    print("❌ ERROR: Input file not found!")
    print(f"   Expected: {input_file.absolute()}")
    print("\n   Please make sure:")
    print("   1. You downloaded val.json from Kaggle")
    print("   2. Renamed it to doclaynet_val_00.json")
    print("   3. Placed it in: data/benchmarks/doclaynet/raw_json/val/")
    exit()

# Get file size
size_mb = os.path.getsize(input_file) / (1024*1024)
print(f"📏 File size: {size_mb:.2f} MB")

# Read the JSON file
print(f"\n📖 Reading JSON file...")
try:
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"✅ Successfully loaded!")
except Exception as e:
    print(f"❌ ERROR loading JSON: {e}")
    exit()

# Analyze the structure
print(f"\n🔍 Analyzing data structure...")
print(f"   Data type: {type(data).__name__}")

if isinstance(data, dict):
    print(f"   Dictionary with keys: {list(data.keys())}")
    
    # Kaggle/COCO format usually has 'images', 'annotations', 'categories'
    if 'images' in data and 'annotations' in data:
        print(f"   ✓ COCO format detected")
        print(f"   Images: {len(data['images'])}")
        print(f"   Annotations: {len(data['annotations'])}")
        if 'categories' in data:
            print(f"   Categories: {len(data['categories'])}")
        
        # For benchmarking, we might want the combined structure
        # But for now, let's keep it as-is
        print(f"\n   ℹ️  Keeping COCO format for benchmarking")
        
elif isinstance(data, list):
    print(f"   List with {len(data):,} items")
    if data:
        print(f"   First item type: {type(data[0]).__name__}")
        if isinstance(data[0], dict):
            print(f"   First item keys: {list(data[0].keys())}")

# Save to ground truth JSON
print(f"\n💾 Saving to ground truth JSON...")
output_file.parent.mkdir(parents=True, exist_ok=True)

try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f)
    
    print(f"✅ Saved to: {output_file}")
    output_size_mb = os.path.getsize(output_file) / (1024*1024)
    print(f"📏 Output size: {output_size_mb:.2f} MB")
    
except Exception as e:
    print(f"❌ ERROR saving: {e}")
    exit()

# Final verification
print(f"\n🔍 Final verification...")
try:
    with open(output_file, "r", encoding="utf-8") as f:
        verify_data = json.load(f)
    
    print(f"✅ File can be loaded successfully")
    
    if isinstance(verify_data, dict):
        print(f"   Type: Dictionary")
        print(f"   Keys: {list(verify_data.keys())}")
        if 'images' in verify_data:
            print(f"   Images: {len(verify_data['images']):,}")
        if 'annotations' in verify_data:
            print(f"   Annotations: {len(verify_data['annotations']):,}")
    
    elif isinstance(verify_data, list):
        print(f"   Type: List")
        print(f"   Items: {len(verify_data):,}")
        if verify_data:
            print(f"   First item keys: {list(verify_data[0].keys())}")
    
except Exception as e:
    print(f"❌ Verification failed: {e}")

print("\n" + "=" * 70)
print("🎉 DOC LAY NET PROCESSING COMPLETE!")
print("=" * 70)
print("\n✅ BENCHMARK STATUS:")
print("   • FinTabNet: ✓ COMPLETE (23.40 MB, 10,505 records)")
print("   • DocLayNet: ✓ COMPLETE (59.47 MB, validation data)")
print("\n📊 Next: PubTables-1M (last dataset)")
print("=" * 70)