"""Service layer for document processing using Docling."""

import time
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from docling.document_converter import DocumentConverter
except ImportError:
    # Mock DocumentConverter for testing when docling is not available
    class DocumentConverter:
        def convert(self, file_path: str):
            raise NotImplementedError("Docling not available")

from .models import (
    ProcessingResult, 
    DocumentMetadata, 
    ConversionConfig,
    SupportedFormat,
    ExportFormat,
    DocumentProcessingError,
    FileFormatNotSupportedError
)


class DocumentService:
    """Service for handling Docling document conversion."""
    
    def __init__(self, config: ConversionConfig):
        self.config = config
        self.converter = DocumentConverter()
    
    def process_document(self, file_path: str) -> ProcessingResult:
        """Process a document and return structured result."""
        start_time = time.time()
        
        try:
            # Validate file format
            self._validate_file_format(file_path)
            
            # Convert document using Docling
            docling_result = self.converter.convert(file_path)
            
            # Extract content based on export format
            content = self._extract_content(docling_result)
            
            # Extract metadata
            metadata = self._extract_metadata(file_path, docling_result)
            
            processing_time = time.time() - start_time
            
            return ProcessingResult(
                content=content,
                metadata=metadata,
                processing_time=processing_time
            )
            
        except Exception as e:
            raise DocumentProcessingError(f"Failed to process document {file_path}: {str(e)}")
    
    def _validate_file_format(self, file_path: str) -> None:
        """Validate if file format is supported."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = path.suffix.lower().lstrip('.')
        try:
            SupportedFormat(suffix)
        except ValueError:
            raise FileFormatNotSupportedError(f"Unsupported file format: {suffix}")
    
    def _extract_content(self, docling_result) -> str:
        """Extract content from Docling result based on export format."""
        if self.config.export_format == ExportFormat.MARKDOWN:
            return docling_result.document.export_to_markdown()
        elif self.config.export_format == ExportFormat.TEXT:
            return docling_result.document.export_to_text()
        elif self.config.export_format == ExportFormat.JSON:
            return str(docling_result.document.export_to_dict())
        else:
            return docling_result.document.export_to_markdown()
    
    def _extract_metadata(self, file_path: str, docling_result) -> DocumentMetadata:
        """Extract metadata from file and Docling result."""
        path = Path(file_path)
        file_stats = path.stat()
        
        # Get format from file extension
        suffix = path.suffix.lower().lstrip('.')
        format_enum = SupportedFormat(suffix)
        
        # Extract document-specific metadata
        doc_metadata = self._get_document_metadata(docling_result)
        
        return DocumentMetadata(
            file_path=str(path.absolute()),
            file_size=file_stats.st_size,
            format=format_enum,
            page_count=doc_metadata.get('page_count'),
            title=doc_metadata.get('title'),
            author=doc_metadata.get('author'),
            creation_date=doc_metadata.get('creation_date'),
            language=doc_metadata.get('language')
        )
    
    def _get_document_metadata(self, docling_result) -> Dict[str, Any]:
        """Extract document-specific metadata from Docling result."""
        metadata = {}
        
        try:
            # Try to extract common metadata
            doc = docling_result.document
            
            # Page count for paginated documents
            if hasattr(doc, 'pages') and doc.pages:
                metadata['page_count'] = len(doc.pages)
            
            # Title extraction (if available)
            if hasattr(doc, 'title') and doc.title:
                metadata['title'] = doc.title
            
            # Other metadata can be extracted here based on Docling's actual structure
            
        except Exception:
            # If metadata extraction fails, continue with empty metadata
            pass
        
        return metadata