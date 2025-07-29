# ====== Code Summary ======
# This module defines `ExtractorFactory`, a factory class that returns the appropriate extractor
# instance based on the file extension. It supports various formats (PDF, DOC, DOCX, XLSX, PPTX, TXT, MSG),
# and falls back to `UnsupportedExtractor` for unrecognized extensions. It also provides an
# `auto_extract` method for simplified content extraction.

# ====== Standard Library Imports ======
import os

# ====== Internal Project Imports ======
from extractor_wrapper.ext import (
    PDFExtractor,
    DOCExtractor,
    DOCXExtractor,
    XLSXExtractor,
    PPTXExtractor,
    TXTExtractor,
    MSGExtractor
)
from extractor_wrapper.unsupported import UnsupportedExtractor
from extractor_wrapper.base_extractor import BaseExtractor


class ExtractorFactory:
    """
    Factory for retrieving appropriate extractor instances based on file extension.

    Supports file types: .pdf, .docx, .xlsx, .doc, .pptx, .txt, .msg.
    Returns UnsupportedExtractor for all other file types.
    """

    @staticmethod
    def get_extractor(file_path: str) -> BaseExtractor:
        """
        Get the correct extractor instance based on the file extension.

        Args:
            file_path (str): The full path to the file.

        Returns:
            BaseExtractor: An instance of a subclass of BaseExtractor suitable for the file type.
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return PDFExtractor()
        elif ext == '.docx':
            return DOCXExtractor()
        elif ext == '.xlsx':
            return XLSXExtractor()
        elif ext == '.doc':
            return DOCExtractor()
        elif ext == '.pptx':
            return PPTXExtractor()
        elif ext == '.txt':
            return TXTExtractor()
        elif ext == '.msg':
            return MSGExtractor()
        else:
            return UnsupportedExtractor()

    @staticmethod
    def auto_extract(file_path: str, safe_read: bool = False) -> str:
        """
        Automatically extract content from a file using the appropriate extractor.

        Args:
            file_path (str): The full path to the file.
            safe_read (bool): If True, suppresses FileNotFoundError and returns an empty string.
        Returns:
            str: Extracted text content.
        """
        extractor: BaseExtractor = ExtractorFactory.get_extractor(file_path)
        return extractor.extract(file_path, safe_read=safe_read)
