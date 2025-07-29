# ====== Code Summary ======
# This module defines `NotInstalledExtractor`, a fallback extractor used when required dependencies
# for a specific file type are missing. It inherits from `BaseExtractor` and overrides the `_ext_extract`
# method to raise an `ImportError` with details about the missing libraries. It also logs the error.

# ====== Internal Project Imports ======
from extractor_wrapper.base_extractor import BaseExtractor


class NotInstalledExtractor(BaseExtractor):
    """
    Fallback extractor for missing dependencies.

    Inherits from:
        BaseExtractor: Provides logging and base structure for extraction.

    This extractor raises an ImportError with a message about the required libraries that are not installed.
    """

    def __init__(
            self,
            required_libs: list[str],
            custom_error_message: str = "",
            *args,
            **kwargs
    ):
        """
        Initialize the NotInstalledExtractor with required libraries and an optional custom error message.

        Args:
            required_libs (list[str]): Names of the libraries that are missing.
            custom_error_message (str, optional): Additional message to include in the error.
        """
        super().__init__(*args, **kwargs)
        self.required_libs: list[str] = required_libs
        self.custom_error_message: str = custom_error_message

    def _ext_extract(self, file_path: str):
        """
        Raise an ImportError indicating which libraries are required but not installed.

        Args:
            file_path (str): The path to the file that was attempted to be extracted.

        Raises:
            ImportError: Always raised to indicate missing dependencies.
        """
        msg = (
            f"Cannot extract '{file_path}'. Extractor packages are not installed ! "
            f"Required libraries not installed: {', '.join(self.required_libs)}"
        )
        if self.custom_error_message:
            msg += f". {self.custom_error_message}"

        self.logger.error(msg)
        raise ImportError(msg)
