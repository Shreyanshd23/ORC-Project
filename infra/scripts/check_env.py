import sys
from pathlib import Path

# Add src to path so we can import hardware
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    import fastapi
    import uvicorn
    import torch
    import paddle
    from paddleocr import PaddleOCR
    from docling.document_converter import DocumentConverter
    from src.utils.hardware import get_device
    
    print("✅ All core libraries imported successfully!")
    
    device = get_device()
    print(f"✅ Hardware Detection: {device.upper()}")
    
    print("\nEnvironment Validation: PASSED")
    
except ImportError as e:
    print(f"❌ Dependency Missing: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    sys.exit(1)
