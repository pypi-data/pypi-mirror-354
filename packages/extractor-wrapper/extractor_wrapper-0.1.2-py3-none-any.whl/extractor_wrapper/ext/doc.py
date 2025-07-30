# ====== Code Summary ======
# This module defines the `DOCExtractor` class, a subclass of `BaseExtractor`, which extracts text
# from `.doc` files using the `antiword` utility. It resolves and manages paths to the antiword
# executable and sets up the environment for subprocess execution.

REQUIRED_LIBS = ["antiword"]

# ====== Standard Library Imports ======
try:
    import os
    import pathlib
    import subprocess
    _NOT_INSTALLED = False
except ImportError:
    _NOT_INSTALLED = True

# ====== Internal Project Imports ======
from extractor_wrapper.base_extractor import BaseExtractor


class DOCExtractor(BaseExtractor):
    """
    Extractor for Microsoft DOC files using the antiword utility.

    Inherits from:
        BaseExtractor: Provides file validation and logging capabilities.

    This extractor uses a subprocess call to execute the antiword program and capture its output.
    """

    # Paths to antiword directory and executable
    __antiword_path: pathlib.Path | None = None
    __antiword_executable_path: pathlib.Path | None = None

    @classmethod
    def get_antiword_executable_path(cls) -> pathlib.Path:
        """
        Resolve the path to the antiword executable.

        Returns:
            pathlib.Path: Absolute path to the antiword executable.
        """
        if cls.__antiword_executable_path is None:
            cls.__antiword_executable_path = (
                    pathlib.Path(__file__).resolve().parent.parent / "dependencies" / "antiword" / "antiword.exe"
            )
        return cls.__antiword_executable_path

    @classmethod
    def get_antiword_path(cls) -> pathlib.Path:
        """
        Resolve the base path to the antiword directory.

        Returns:
            pathlib.Path: Absolute path to the antiword directory.
        """
        if cls.__antiword_path is None:
            cls.__antiword_path = (
                    pathlib.Path(__file__).resolve().parent.parent / "dependencies" / "antiword"
            )
        return cls.__antiword_path

    def extract_text_with_antiword(self, file_path: str) -> str:
        """
        Extract text content from a DOC file using the antiword tool via subprocess.

        The method constructs the command to run antiword, sets up environment variables,
        and decodes the output.

        Args:
            file_path (str): Path to the .doc file to extract.

        Returns:
            str: Extracted text from the DOC file.

        Raises:
            subprocess.CalledProcessError: If antiword execution fails.
        """
        try:
            self.logger.info(f"Extracting text using antiword for file: {file_path}")

            antiword_executable_path = DOCExtractor.get_antiword_executable_path()
            antiword_path = DOCExtractor.get_antiword_path()

            cmd = [str(antiword_executable_path), "-t", file_path]

            env = os.environ.copy()
            env["HOME"] = str(antiword_path)
            env["ANTIWORDHOME"] = str(antiword_path)

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                env=env
            )

            text = result.stdout.decode("utf-8", errors="ignore")
            return text

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode("utf-8", errors="ignore")
            self.logger.error(f"Error executing antiword on {file_path}: {error_message}")
            raise e

    def _ext_extract(self, file_path: str) -> str:
        """
        Main method for extracting text from a DOC file using antiword.

        Args:
            file_path (str): Path to the .doc file to extract.

        Returns:
            str: Extracted text content.

        Raises:
            Exception: If extraction fails for any reason.
        """
        try:
            text = self.extract_text_with_antiword(file_path)
            return text
        except Exception as e:
            self.logger.error(f"Error processing DOC file: {file_path}")
            raise e
