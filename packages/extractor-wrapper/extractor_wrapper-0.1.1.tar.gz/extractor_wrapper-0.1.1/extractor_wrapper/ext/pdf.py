# ====== Code Summary ======
# This module defines `PDFExtractor`, a subclass of `BaseExtractor`, for extracting text from PDF files
# using the `PyPDF2` library. It reads all pages from the PDF, extracts text, logs the operation, and
# handles any exceptions that occur during the extraction process.

REQUIRED_LIBS = ["PyPDF2"]

# ====== Third-party Library Imports ======
try:
    import PyPDF2

    _NOT_INSTALLED = False
except ImportError:
    _NOT_INSTALLED = True

# ====== Internal Project Imports ======
from extractor_wrapper.base_extractor import BaseExtractor


class PDFExtractor(BaseExtractor):
    """
    Extractor for PDF files using PyPDF2.

    Inherits from:
        BaseExtractor: Provides file validation and logging features.

    This extractor reads and extracts text from all pages in a PDF document.
    """

    def _ext_extract(self, file_path: str) -> str:
        """
        Extract text content from a PDF file.

        Iterates through all pages in the PDF and concatenates the extracted text.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            str: Combined text content from all pages.

        Raises:
            Exception: If any error occurs during file access or text extraction.
        """
        # Log the start of PDF text extraction
        self.logger.info(f"Extracting text from PDF: {file_path}")
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
        except Exception as e:
            # Log errors encountered during extraction
            self.logger.error(f"Error extracting PDF: {file_path}")
            raise e
        return text
