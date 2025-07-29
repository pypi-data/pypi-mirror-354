# ====== Code Summary ======
# This module defines `MSGExtractor`, a subclass of `BaseExtractor`, for extracting text content
# from Outlook `.msg` files using the `extract_msg` library. It captures email metadata and body,
# logs the process, and handles file-related and extraction errors gracefully.

REQUIRED_LIBS = ["extract_msg"]

# ====== Third-party Library Imports ======
try:
    import extract_msg

    _NOT_INSTALLED = False
except ImportError:
    _NOT_INSTALLED = True

# ====== Internal Project Imports ======
from extractor_wrapper.base_extractor import BaseExtractor


class MSGExtractor(BaseExtractor):
    """
    Extractor for Microsoft Outlook MSG files.

    Inherits from:
        BaseExtractor: Provides file validation and logging features.

    This extractor parses email metadata (subject, sender, date) and the body text using extract_msg.
    """

    def _ext_extract(self, file_path: str) -> str:
        """
        Extract plain text content from an Outlook .msg file.

        Extracted content includes the subject, sender, date, and body text, formatted in plain text.

        Args:
            file_path (str): Path to the .msg file.

        Returns:
            str: Formatted string containing extracted email fields.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            Exception: For all other errors encountered during extraction.
        """
        # Log the beginning of MSG file extraction
        self.logger.info(f"Extracting text from MSG: {file_path}")
        try:
            msg = extract_msg.Message(file_path)
            msg_sender = msg.sender or ""
            msg_date = msg.date or ""
            msg_subject = msg.subject or ""
            msg_body = msg.body or ""

            result = (
                f"Subject: {msg_subject}\n"
                f"From: {msg_sender}\n"
                f"Date: {msg_date}\n\n"
                f"{msg_body}"
            )
            return result

        except FileNotFoundError:
            # Log file-not-found error specifically
            self.logger.error(f"File not found: {file_path}")
            raise

        except Exception as e:
            # Log any other exception during MSG extraction
            self.logger.error(f"Error extracting MSG: {file_path} – {str(e)}")
            raise
