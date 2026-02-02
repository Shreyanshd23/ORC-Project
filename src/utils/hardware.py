import torch
import platform
import logging

logger = logging.getLogger(__name__)

def get_device():
    """
    Detects the best available hardware device.
    Priority: CUDA > MPS (Apple Silicon) > CPU
    """
    if torch.cuda.is_available():
        device = "cuda"
        logger.info(f"System: {platform.system()} | Device: NVIDIA GPU (CUDA)")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = "mps"
        logger.info(f"System: {platform.system()} | Device: Apple Silicon GPU (MPS)")
    else:
        device = "cpu"
        logger.warning(f"System: {platform.system()} | Device: CPU (Fallback Mode)")
    
    return device

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    device = get_device()
    print(f"\n[Hardware Detector] Final Choice: {device.upper()}")
