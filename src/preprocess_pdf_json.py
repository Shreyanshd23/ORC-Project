import json
import pandas as pd
from pathlib import Path

# =====================
# CONFIG
# =====================
PARQUET_FILE = r"C:\Users\dewan\AI-FRC\train-00000.parquet"
OUTPUT_DIR = Path(r"C:\Users\dewan\AI-FRC\data\benchmarks")
NUM_SAMPLES = 3

print("📖 Loading parquet...")
df = pd.read_parquet(PARQUET_FILE)
print(f"✅ Loaded {len(df):,} rows")
print("🧱 Columns:", df.columns.tolist())

# Required columns (from README)
required = ["pdf_bytes", "ocr_json", "basename", "page"]
for col in required:
    if col not in df.columns:
        raise ValueError(f"❌ Missing required column: {col}")

subset = df.head(NUM_SAMPLES)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\n🚀 Creating PDF + JSON pairs...\n")

for i, row in subset.iterrows():
    doc_id = f"{row['basename']}_p{row['page']}"

    # --------------------
    # PDF
    # --------------------
    pdf_path = OUTPUT_DIR / f"{doc_id}.pdf"
    if row["pdf_bytes"] is None:
        print(f"⚠️ Skipping {doc_id} (no pdf_bytes)")
        continue

    with open(pdf_path, "wb") as f:
        f.write(row["pdf_bytes"])

    # --------------------
    # OCR JSON (GT)
    # --------------------
    ocr_data = json.loads(row["ocr_json"])

    gt = {
        "id": doc_id,
        "source": "PubMed-OCR",
        "page": int(row["page"]),
        "ocr": ocr_data
    }

    json_path = OUTPUT_DIR / f"{doc_id}_gt.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(gt, f, indent=2, ensure_ascii=False)

    print(f"✅ {doc_id}: PDF + OCR JSON created")

print("\n🎉 DONE")
print(f"📁 Output directory: {OUTPUT_DIR.resolve()}")
