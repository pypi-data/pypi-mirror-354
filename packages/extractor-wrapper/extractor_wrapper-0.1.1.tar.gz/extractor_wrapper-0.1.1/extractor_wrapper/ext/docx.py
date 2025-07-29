# ====== Code Summary ======
# This module defines `DOCXExtractor`, a subclass of `BaseExtractor`, for extracting text from `.docx` files
# using the `python-docx` library. It logs the extraction process and handles any exceptions by logging errors.

REQUIRED_LIBS = ["python-docx"]

# ====== Third-party Library Imports ======
try:
    from docx import Document

    _NOT_INSTALLED = False
except ImportError:
    _NOT_INSTALLED = True

# ====== Internal Project Imports ======
from extractor_wrapper.base_extractor import BaseExtractor


class DOCXExtractor(BaseExtractor):
    """
    Extractor for DOCX (Microsoft Word Open XML) files.

    Inherits from:
        BaseExtractor: Provides file validation and logging capabilities.

    This extractor uses the `python-docx` library to load and extract text from paragraphs.
    """

    def _ext_extract(self, file_path: str) -> str:
        """
        Extract text content from a DOCX file.

        Args:
            file_path (str): Path to the .docx file to extract.

        Returns:
            str: Extracted text joined from all paragraphs.

        Raises:
            Exception: If extraction fails for any reason.
        """
        # Logging the start of the DOCX extraction process
        self.logger.info(f"Extracting text from DOCX: {file_path}")
        try:
            doc = Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)
        except Exception as e:
            # Logging any errors encountered during DOCX extraction
            self.logger.error(f"Error extracting DOCX: {file_path}")
            raise e
