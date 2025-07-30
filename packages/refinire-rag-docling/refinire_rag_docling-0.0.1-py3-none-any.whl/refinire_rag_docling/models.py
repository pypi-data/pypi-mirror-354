"""Data models for refinire-rag-docling plugin."""

from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum


class SupportedFormat(str, Enum):
    """Supported document formats."""
    PDF = "pdf"
    DOCX = "docx" 
    XLSX = "xlsx"
    HTML = "html"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"


class ExportFormat(str, Enum):
    """Export format options."""
    MARKDOWN = "markdown"
    TEXT = "text"
    JSON = "json"


@dataclass
class ConversionConfig:
    """Configuration for document conversion."""
    export_format: ExportFormat = ExportFormat.MARKDOWN
    chunk_size: int = 512
    ocr_enabled: bool = True
    table_structure: bool = True
    options: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not (100 <= self.chunk_size <= 4096):
            raise ValueError("chunk_size must be between 100 and 4096")
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            'export_format': self.export_format.value,
            'chunk_size': self.chunk_size,
            'ocr_enabled': self.ocr_enabled,
            'table_structure': self.table_structure,
            'options': self.options
        }


@dataclass
class DocumentMetadata:
    """Document metadata extracted during processing."""
    file_path: str
    file_size: int
    format: SupportedFormat
    page_count: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    creation_date: Optional[str] = None
    language: Optional[str] = None
    
    def __post_init__(self):
        """Validate metadata after initialization."""
        if not Path(self.file_path).exists():
            raise ValueError(f"File does not exist: {self.file_path}")


@dataclass
class ProcessingResult:
    """Result of document processing."""
    content: str
    metadata: DocumentMetadata
    processing_time: float
    chunks: List[str] = field(default_factory=list)
    
    def get_chunks(self, chunk_size: int = 512) -> List[str]:
        """Split content into chunks of specified size."""
        if not self.chunks:
            words = self.content.split()
            chunks = []
            current_chunk = []
            current_size = 0
            
            for word in words:
                word_size = len(word) + 1  # +1 for space
                if current_size + word_size > chunk_size and current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [word]
                    current_size = word_size
                else:
                    current_chunk.append(word)
                    current_size += word_size
            
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            
            self.chunks = chunks
        
        return self.chunks
    
    def to_rag_format(self) -> Dict[str, Any]:
        """Convert to RAG system compatible format."""
        return {
            "content": self.content,
            "metadata": {
                "file_path": self.metadata.file_path,
                "file_size": self.metadata.file_size,
                "format": self.metadata.format.value,
                "page_count": self.metadata.page_count,
                "title": self.metadata.title,
                "author": self.metadata.author,
                "creation_date": self.metadata.creation_date,
                "language": self.metadata.language
            },
            "chunks": self.get_chunks(),
            "source": self.metadata.file_path
        }


class DoclingLoaderError(Exception):
    """Base exception for DoclingLoader."""
    pass


class FileFormatNotSupportedError(DoclingLoaderError):
    """Raised when file format is not supported."""
    pass


class DocumentProcessingError(DoclingLoaderError):
    """Raised when document processing fails."""
    pass


class ConfigurationError(DoclingLoaderError):
    """Raised when configuration is invalid."""
    pass