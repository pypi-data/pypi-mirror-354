# ====== Code Summary ======
# This module defines `TXTExtractor`, a subclass of `BaseExtractor`, which is responsible for extracting
# raw text from plain `.txt` files using built-in Python I/O functions. It reads the entire content
# of the file and raises appropriate exceptions for file access errors.

REQUIRED_LIBS = []

try:
    _NOT_INSTALLED = False
except ImportError:
    _NOT_INSTALLED = True

# ====== Internal Project Imports ======
from extractor_wrapper.base_extractor import BaseExtractor


class TXTExtractor(BaseExtractor):
    """
    Extractor for plain text (.txt) files using built-in I/O functions.

    Inherits from:
        BaseExtractor: Provides file existence validation and logging features.
    """

    def _ext_extract(self, file_path: str) -> str:
        """
        Extract raw text content from a .txt file.

        Args:
            file_path (str): Path to the text file.

        Returns:
            str: Full text content of the file.

        Raises:
            FileNotFoundError: If the specified file is not found.
            IOError: If an error occurs while reading the file.
        """
        # No need to log here — base class handles file existence and logging
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
