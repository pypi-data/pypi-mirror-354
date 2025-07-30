"""Refinire-RAG Docling Plugin - Document loader using Docling library."""

from .loader import DoclingLoader
from .models import (
    ConversionConfig,
    SupportedFormat,
    ExportFormat,
    ProcessingResult,
    DocumentMetadata,
    DoclingLoaderError,
    FileFormatNotSupportedError,
    DocumentProcessingError,
    ConfigurationError
)
from .services import DocumentService

__version__ = "0.0.1"
__all__ = [
    "DoclingLoader",
    "ConversionConfig", 
    "SupportedFormat",
    "ExportFormat",
    "ProcessingResult",
    "DocumentMetadata",
    "DocumentService",
    "DoclingLoaderError",
    "FileFormatNotSupportedError", 
    "DocumentProcessingError",
    "ConfigurationError"
]