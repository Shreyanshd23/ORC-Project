import pandas as pd
import json
import numpy as np
from pathlib import Path
import os

print("=" * 70)
print("FIN TAB NET - MINIMAL WORKING VERSION")
print("=" * 70)

# Delete old file if exists
output_path = "data/benchmarks/fintabnet/gt_json/FinTabNet_OTSL_val.json"
if os.path.exists(output_path):
    os.remove(output_path)
    print(f"🗑️  Deleted old file")

# Read parquet files
print("\n📖 Reading parquet files...")
files = [
    "data/benchmarks/fintabnet/raw_parquet/val-00000-of-00002-86a95c240ca8897d.parquet",
    "data/benchmarks/fintabnet/raw_parquet/val-00001-of-00002-e636f429131c7408.parquet"
]

df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
print(f"✅ Total rows: {len(df):,}")
print(f"📊 Original columns: {list(df.columns)}")

# Select ONLY the columns we need for benchmarking
# Based on the README, for table structure recognition we need:
required_columns = ['otsl', 'html', 'html_restored', 'cols', 'rows', 'filename', 'imgid']

# Keep only required columns (or all except problematic ones)
print(f"\n🔧 Selecting columns for benchmarking...")
if all(col in df.columns for col in required_columns):
    df = df[required_columns]
    print(f"✅ Using minimal columns: {list(df.columns)}")
else:
    # Fallback: Remove only problematic columns
    print(f"⚠️  Some required columns missing, removing only problematic ones...")
    if 'image' in df.columns:
        df = df.drop(columns=['image'])
        print(f"  Removed 'image' column")

print(f"📊 Final columns: {list(df.columns)}")
print(f"📐 DataFrame shape: {df.shape}")

# Convert any remaining numpy types
print(f"\n🔄 Converting numpy types to Python types...")

def clean_value(val):
    """Convert numpy types to Python native types"""
    if isinstance(val, np.ndarray):
        return val.tolist()
    elif isinstance(val, np.generic):  # numpy scalar
        return val.item()
    elif isinstance(val, dict):
        return {k: clean_value(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [clean_value(item) for item in val]
    else:
        return val

# Convert each column
for col in df.columns:
    print(f"  Processing column: {col}")
    try:
        # Check if column needs cleaning
        sample = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
        if sample is not None:
            if isinstance(sample, (np.ndarray, np.generic)) or (
                isinstance(sample, list) and sample and isinstance(sample[0], np.ndarray)
            ):
                df[col] = df[col].apply(clean_value)
    except Exception as e:
        print(f"    ⚠️  Warning: Could not process {col}: {e}")

# Save to JSON
print(f"\n💾 Saving to {output_path}...")
Path(output_path).parent.mkdir(parents=True, exist_ok=True)

# Use pandas to_json which handles basic types well
df.to_json(output_path, orient='records')
print(f"✅ File saved using pandas.to_json()")

# Verify
size_mb = os.path.getsize(output_path) / (1024*1024)
print(f"📏 File size: {size_mb:.2f} MB")

# Quick test
print(f"\n🔍 Quick verification...")
try:
    with open(output_path, 'r') as f:
        data = json.load(f)
    print(f"  ✅ Successfully loaded JSON")
    print(f"  📊 Records: {len(data):,}")
    print(f"  🔑 First record keys: {list(data[0].keys())}")
    
    # Show OTSL sample (the main thing we need)
    if 'otsl' in data[0]:
        otsl_sample = data[0]['otsl']
        print(f"\n  📝 OTSL sample (first 100 chars):")
        if isinstance(otsl_sample, str):
            print(f"    {otsl_sample[:100]}...")
        else:
            print(f"    Type: {type(otsl_sample).__name__}")
    
except Exception as e:
    print(f"  ❌ Verification failed: {e}")

print("\n" + "=" * 70)
print("🎉 FIN TAB NET PROCESSING COMPLETE!")
print("=" * 70)