from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseOCREngine(ABC):

    @abstractmethod
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Must return:
        {
            "text": str,
            "markdown": str,
            "pages": int,
            "time_sec": float
        }
        """
        pass
