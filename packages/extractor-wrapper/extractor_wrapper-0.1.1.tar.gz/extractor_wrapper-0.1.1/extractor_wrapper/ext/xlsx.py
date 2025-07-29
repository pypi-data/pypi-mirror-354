# ====== Code Summary ======
# This module defines `XLSXExtractor`, a subclass of `BaseExtractor`, used for extracting content
# from `.xlsx` spreadsheet files using pandas. It suppresses user warnings globally and reads
# the entire Excel file into a DataFrame, converting it to a formatted string output.

REQUIRED_LIBS = ["pandas", "openpyxl"]

# ====== Standard Library Imports ======
import warnings

# Suppress user warnings, e.g., from pandas Excel engine
warnings.filterwarnings("ignore", category=UserWarning)

# ====== Third-party Library Imports ======
try:
    import pandas as pd

    _NOT_INSTALLED = False
except ImportError:
    _NOT_INSTALLED = True

# ====== Internal Project Imports ======
from extractor_wrapper.base_extractor import BaseExtractor


class XLSXExtractor(BaseExtractor):
    """
    Extractor for Microsoft Excel XLSX files.

    Inherits from:
        BaseExtractor: Provides file validation and logging capabilities.

    This extractor reads spreadsheet data into a pandas DataFrame and returns it as a formatted string.
    """

    def _ext_extract(self, file_path: str) -> str:
        """
        Extract content from an Excel XLSX file and convert it to a string representation.

        Args:
            file_path (str): Path to the .xlsx file.

        Returns:
            str: Text representation of the spreadsheet data.

        Raises:
            Exception: If reading or converting the file fails.
        """
        # Logging is handled by the base class for file checks and method call
        df = pd.read_excel(file_path)
        return df.to_string()
