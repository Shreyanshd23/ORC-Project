from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable


class BaseOCREngine(ABC):
    """
    Abstract base class for all OCR engines.

    This defines a common, flexible interface so that:
    - Engines can provide progress feedback
    - Engines can handle corrupted PDFs gracefully
    - The CLI can remain engine-agnostic
    """

    def __init__(self, **kwargs):
        """
        Base constructor.

        Accepts arbitrary keyword arguments so that
        different engines (Docling, Tesseract, TrOCR)
        can define their own configuration parameters
        without breaking the interface.
        """
        pass

    @abstractmethod
    def process_pdf(
        self,
        pdf_path: str,
        output_dir: Optional[str] = None,
        progress_cb: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """
        Process a PDF file and return OCR results.

        Must return a dictionary with at least:

        {
            "text": str,        # Plain extracted text
            "markdown": str,    # Markdown representation (if available)
            "pages": int,       # Number of pages processed
            "time_sec": float   # Total processing time in seconds
        }

        Implementations should:
        - Validate input PDFs
        - Handle corrupted files gracefully
        - Use progress_cb to emit user-visible status updates
        """
        raise NotImplementedError
