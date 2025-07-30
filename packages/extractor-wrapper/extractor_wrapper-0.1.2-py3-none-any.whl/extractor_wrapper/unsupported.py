# ====== Code Summary ======
# This module defines `UnsupportedExtractor`, a subclass of `BaseExtractor`, which is used for handling
# unsupported file types. It logs an error and raises a ValueError when an extraction is attempted.

# ====== Internal Project Imports ======
from extractor_wrapper.base_extractor import BaseExtractor


class UnsupportedExtractor(BaseExtractor):
    """
    Extractor for unsupported file types.

    Inherits from:
        BaseExtractor: Provides logging and file existence validation.

    This class is used when an attempt is made to extract text from a file with an unsupported type.
    """

    def _ext_extract(self, file_path: str):
        """
        Handles extraction attempts for unsupported file types.

        Logs an error and raises a ValueError indicating the file type is unsupported.

        Args:
            file_path (str): The path to the file for which extraction was attempted.

        Raises:
            ValueError: Indicates that the file type is not supported.
        """
        # Logging the unsupported file type before raising an error
        self.logger.error(f"Unsupported file type: {file_path}")
        raise ValueError(f"Unsupported file type: {file_path}")
