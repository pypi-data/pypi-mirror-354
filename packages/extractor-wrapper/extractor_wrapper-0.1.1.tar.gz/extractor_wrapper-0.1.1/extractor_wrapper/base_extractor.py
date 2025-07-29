# ====== Code Summary ======
# This module defines an abstract base class `BaseExtractor` for text extraction tasks.
# It integrates a file existence decorator that optionally suppresses errors via a `safe_read` flag.
# Subclasses must implement `_ext_extract`, which is invoked only if the target file exists.
# The class also includes logging to track extraction attempts, errors, and file checks.

# ====== Standard Library Imports ======
import os
from abc import ABC, abstractmethod
from functools import wraps

# ====== Third-party Library Imports ======
from loggerplusplus import LoggerClass


class BaseExtractor(ABC, LoggerClass):
    """
    Abstract base class for text extractors. Handles logging and safe file existence verification.

    Subclasses must implement the `_ext_extract` method, which defines how the text
    should be extracted from a given file.

    Inherits:
        ABC: Provides abstract base class features.
        LoggerClass: Provides `self.logger` for logging operations.
    """

    @staticmethod
    def file_exists_decorator(func):
        """
        Decorator to ensure a file exists before executing the decorated method.

        If the file does not exist:
        - Logs an error.
        - If `safe_read` is True, returns an empty string instead of raising an error.

        Args:
            func (Callable): The method to wrap.

        Returns:
            Callable: The wrapped method with file existence verification.
        """

        @wraps(func)
        def wrapper(self, file_path: str, safe_read: bool = False, *args, **kwargs):
            if not os.path.isfile(file_path):
                # File not found; safe_read controls behavior
                if safe_read:
                    self.logger.error(
                        f"File not found (safe_read enabled, skipping extract): {file_path}"
                    )
                    return ""
                else:
                    self.logger.error(f"File not found: {file_path}")
                    raise FileNotFoundError(f"File not found: {file_path}")

            # File exists, proceed with original function
            self.logger.debug(f"File exists: {file_path}")
            return func(self, file_path, safe_read, *args, **kwargs)

        return wrapper

    @file_exists_decorator
    def extract(self, file_path: str, safe_read: bool = False) -> str:
        """
        Extract text from a specified file using the subclass's extraction logic.

        Applies a file existence check using a decorator before delegating to `_ext_extract`.

        Args:
            file_path (str): The path to the file to extract text from.
            safe_read (bool, optional): If True, suppresses FileNotFoundError and returns an empty string.

        Returns:
            str: The extracted text content, or an empty string if file not found and safe_read is True.
        """
        return self._ext_extract(file_path=file_path)

    @abstractmethod
    def _ext_extract(self, file_path: str) -> str:
        """
        Abstract method that subclasses must implement to define custom extraction logic.

        This method is only called after verifying the file exists.

        Args:
            file_path (str): The path to the file for extracting text.

        Returns:
            str: The text extracted from the file.
        """
        raise NotImplementedError("The _ext_extract method must be implemented by subclasses.")
