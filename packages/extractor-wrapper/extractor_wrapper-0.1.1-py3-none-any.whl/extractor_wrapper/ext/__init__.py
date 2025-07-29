# ====== Code Summary ======
# This module dynamically imports and registers extractor classes for various file formats
# (PDF, DOC, DOCX, XLSX, PPTX, TXT, MSG). If an import fails due to missing dependencies,
# a `NotInstalledExtractor` is used as a fallback, recording the required libraries.
# It also defines `__all__` for wildcard imports and maintains lists of available and unavailable extractors.

# ====== Standard Library Imports ======
import functools

# ====== Internal Project Imports ======
from extractor_wrapper.not_installed import NotInstalledExtractor

AVAILABLE_EXTRACTORS = []
UNAVAILABLE_EXTRACTORS = []

# ==== PDF ====
from extractor_wrapper.ext.pdf import (
    PDFExtractor,
    REQUIRED_LIBS as PDF_REQUIRED_LIBS,
    _NOT_INSTALLED as PDF_NOT_INSTALLED
)

if PDF_NOT_INSTALLED:
    PDFExtractor = functools.partial(NotInstalledExtractor, required_libs=PDF_REQUIRED_LIBS)
    UNAVAILABLE_EXTRACTORS.append(("PDFExtractor", PDF_REQUIRED_LIBS))
else:
    AVAILABLE_EXTRACTORS.append("PDFExtractor")

# ==== DOC ====
from extractor_wrapper.ext.doc import (
    DOCExtractor,
    REQUIRED_LIBS as DOC_REQUIRED_LIBS,
    _NOT_INSTALLED as DOC_NOT_INSTALLED
)

if DOC_NOT_INSTALLED:
    DOCExtractor = functools.partial(NotInstalledExtractor, required_libs=DOC_REQUIRED_LIBS)
    UNAVAILABLE_EXTRACTORS.append(("DOCExtractor", DOC_REQUIRED_LIBS))
else:
    AVAILABLE_EXTRACTORS.append("DOCExtractor")

# ==== DOCX ====
from extractor_wrapper.ext.docx import (
    DOCXExtractor,
    REQUIRED_LIBS as DOCX_REQUIRED_LIBS,
    _NOT_INSTALLED as DOCX_NOT_INSTALLED
)

if DOCX_NOT_INSTALLED:
    DOCXExtractor = functools.partial(NotInstalledExtractor, required_libs=DOCX_REQUIRED_LIBS)
    UNAVAILABLE_EXTRACTORS.append(("DOCXExtractor", DOCX_REQUIRED_LIBS))
else:
    AVAILABLE_EXTRACTORS.append("DOCXExtractor")

# ==== XLSX ====
from extractor_wrapper.ext.xlsx import (
    XLSXExtractor,
    REQUIRED_LIBS as XLSX_REQUIRED_LIBS,
    _NOT_INSTALLED as XLSX_NOT_INSTALLED
)

if XLSX_NOT_INSTALLED:
    XLSXExtractor = functools.partial(NotInstalledExtractor, required_libs=XLSX_REQUIRED_LIBS)
    UNAVAILABLE_EXTRACTORS.append(("XLSXExtractor", XLSX_REQUIRED_LIBS))
else:
    AVAILABLE_EXTRACTORS.append("XLSXExtractor")

# ==== PPTX ====
from extractor_wrapper.ext.pptx import (
    PPTXExtractor,
    REQUIRED_LIBS as PPTX_REQUIRED_LIBS,
    _NOT_INSTALLED as PPTX_NOT_INSTALLED
)

if PPTX_NOT_INSTALLED:
    PPTXExtractor = functools.partial(NotInstalledExtractor, required_libs=PPTX_REQUIRED_LIBS)
    UNAVAILABLE_EXTRACTORS.append(("PPTXExtractor", PPTX_REQUIRED_LIBS))
else:
    AVAILABLE_EXTRACTORS.append("PPTXExtractor")

# ==== TXT ====
from extractor_wrapper.ext.txt import (
    TXTExtractor,
    REQUIRED_LIBS as TXT_REQUIRED_LIBS,
    _NOT_INSTALLED as TXT_NOT_INSTALLED
)

if TXT_NOT_INSTALLED:
    TXTExtractor = functools.partial(NotInstalledExtractor, required_libs=TXT_REQUIRED_LIBS)
    UNAVAILABLE_EXTRACTORS.append(("TXTExtractor", TXT_REQUIRED_LIBS))
else:
    AVAILABLE_EXTRACTORS.append("TXTExtractor")

# ==== MSG ====
from extractor_wrapper.ext.msg import (
    MSGExtractor,
    REQUIRED_LIBS as MSG_REQUIRED_LIBS,
    _NOT_INSTALLED as MSG_NOT_INSTALLED
)

if MSG_NOT_INSTALLED:
    MSGExtractor = functools.partial(NotInstalledExtractor, required_libs=MSG_REQUIRED_LIBS)
    UNAVAILABLE_EXTRACTORS.append(("MSGExtractor", MSG_REQUIRED_LIBS))
else:
    AVAILABLE_EXTRACTORS.append("MSGExtractor")

# Wildcard import support
__all__ = [
    "PDFExtractor",
    "DOCExtractor",
    "DOCXExtractor",
    "XLSXExtractor",
    "PPTXExtractor",
    "TXTExtractor",
    "MSGExtractor",
    "AVAILABLE_EXTRACTORS",
    "UNAVAILABLE_EXTRACTORS"
]
