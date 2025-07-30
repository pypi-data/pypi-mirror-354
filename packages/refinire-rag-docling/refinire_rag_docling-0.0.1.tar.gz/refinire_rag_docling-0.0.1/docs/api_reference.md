# API Reference

Complete API documentation for the Refinire-RAG Docling Plugin.

## Core Classes

### DoclingLoader

Main class for loading and processing documents.

```python
class DoclingLoader:
    """Docling-based document loader for RAG systems."""
```

#### Constructor

```python
def __init__(self, config: ConversionConfig = None) -> None:
    """
    Initialize DoclingLoader with configuration.
    
    Args:
        config: Optional configuration object. Uses default if None.
    """
```

#### Methods

##### load()

```python
def load(self, source: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Load a single document and return RAG-compatible format.
    
    Args:
        source: Path to the document file
        
    Returns:
        List containing single document dictionary
        
    Raises:
        FileFormatNotSupportedError: If file format is not supported
        DocumentProcessingError: If document processing fails
    """
```

##### load_batch()

```python
def load_batch(self, sources: List[Union[str, Path]]) -> List[Dict[str, Any]]:
    """
    Load multiple documents in batch.
    
    Args:
        sources: List of document file paths
        
    Returns:
        List of document dictionaries
        
    Note:
        Continues processing even if individual documents fail.
        Errors are logged but do not stop batch processing.
    """
```

#### Factory Methods

##### create_with_markdown_output()

```python
@classmethod
def create_with_markdown_output(cls, chunk_size: int = 512) -> "DoclingLoader":
    """
    Factory method for creating loader with markdown output.
    
    Args:
        chunk_size: Size for text chunking
        
    Returns:
        DoclingLoader configured for markdown output
    """
```

##### create_with_text_output()

```python
@classmethod
def create_with_text_output(cls, chunk_size: int = 512) -> "DoclingLoader":
    """
    Factory method for creating loader with text output.
    
    Args:
        chunk_size: Size for text chunking
        
    Returns:
        DoclingLoader configured for text output
    """
```

### ConversionConfig

Configuration class for document processing options.

```python
@dataclass
class ConversionConfig:
    """Configuration for document conversion."""
    
    export_format: ExportFormat = ExportFormat.MARKDOWN
    chunk_size: int = 512
    ocr_enabled: bool = True
    table_structure: bool = True
    options: Dict[str, Any] = field(default_factory=dict)
```

#### Methods

##### validate()

```python
def validate(self) -> bool:
    """
    Validate configuration settings.
    
    Returns:
        True if configuration is valid
        
    Raises:
        ValueError: If chunk_size is not between 100 and 4096
    """
```

##### to_dict()

```python
def to_dict(self) -> Dict[str, Any]:
    """
    Convert configuration to dictionary format.
    
    Returns:
        Dictionary representation of configuration
    """
```

### DocumentMetadata

Metadata container for processed documents.

```python
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
```

### ProcessingResult

Container for document processing results.

```python
@dataclass
class ProcessingResult:
    """Result of document processing."""
    
    content: str
    metadata: DocumentMetadata
    processing_time: float
    chunks: List[str] = field(default_factory=list)
```

#### Methods

##### get_chunks()

```python
def get_chunks(self, chunk_size: int = 512) -> List[str]:
    """
    Split content into chunks of specified size.
    
    Args:
        chunk_size: Maximum size for each chunk
        
    Returns:
        List of text chunks
    """
```

##### to_rag_format()

```python
def to_rag_format(self) -> Dict[str, Any]:
    """
    Convert to RAG system compatible format.
    
    Returns:
        Dictionary with content, metadata, chunks, and source
    """
```

### DocumentService

Service class for document processing logic.

```python
class DocumentService:
    """Service for handling Docling document conversion."""
```

#### Constructor

```python
def __init__(self, config: ConversionConfig) -> None:
    """
    Initialize service with configuration.
    
    Args:
        config: Conversion configuration
    """
```

#### Methods

##### process_document()

```python
def process_document(self, file_path: str) -> ProcessingResult:
    """
    Process a document and return structured result.
    
    Args:
        file_path: Path to document file
        
    Returns:
        ProcessingResult with content and metadata
        
    Raises:
        FileFormatNotSupportedError: If file format is not supported
        DocumentProcessingError: If processing fails
    """
```

## Enums

### SupportedFormat

```python
class SupportedFormat(str, Enum):
    """Supported document formats."""
    
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    HTML = "html"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
```

### ExportFormat

```python
class ExportFormat(str, Enum):
    """Export format options."""
    
    MARKDOWN = "markdown"
    TEXT = "text"
    JSON = "json"
```

## Exceptions

### DoclingLoaderError

```python
class DoclingLoaderError(Exception):
    """Base exception for DoclingLoader."""
    pass
```

### FileFormatNotSupportedError

```python
class FileFormatNotSupportedError(DoclingLoaderError):
    """Raised when file format is not supported."""
    pass
```

### DocumentProcessingError

```python
class DocumentProcessingError(DoclingLoaderError):
    """Raised when document processing fails."""
    pass
```

### ConfigurationError

```python
class ConfigurationError(DoclingLoaderError):
    """Raised when configuration is invalid."""
    pass
```

## Usage Examples

### Basic Document Loading

```python
from refinire_rag_docling import DoclingLoader

loader = DoclingLoader()
documents = loader.load("document.pdf")

for doc in documents:
    print(f"Content: {doc['content'][:100]}...")
    print(f"Source: {doc['metadata']['source']}")
```

### Custom Configuration

```python
from refinire_rag_docling import DoclingLoader, ConversionConfig, ExportFormat

config = ConversionConfig(
    export_format=ExportFormat.TEXT,
    chunk_size=1024,
    ocr_enabled=False
)

loader = DoclingLoader(config)
documents = loader.load("document.pdf")
```

### Error Handling

```python
from refinire_rag_docling import (
    DoclingLoader,
    FileFormatNotSupportedError,
    DocumentProcessingError
)

loader = DoclingLoader()

try:
    documents = loader.load("document.unknown")
except FileFormatNotSupportedError:
    print("File format not supported")
except DocumentProcessingError as e:
    print(f"Processing failed: {e}")
```

### Batch Processing

```python
files = ["doc1.pdf", "doc2.docx", "doc3.xlsx"]
documents = loader.load_batch(files)

print(f"Successfully processed {len(documents)} documents")
```

## Document Output Format

Each processed document returns a dictionary with the following structure:

```python
{
    "content": str,           # Extracted text content
    "metadata": {             # Document metadata
        "source": str,        # Original file path
        "format": str,        # File format (pdf, docx, etc.)
        "file_size": int,     # File size in bytes
        "page_count": int,    # Number of pages (if applicable)
        "title": str,         # Document title (if available)
        "author": str,        # Document author (if available)
        "processing_time": float  # Processing time in seconds
    },
    "chunks": List[str]       # Text chunks (if chunking enabled)
}
```

## Performance Considerations

### Chunking

- Optimal chunk size depends on your RAG system
- Smaller chunks (256-512): Better for precise retrieval
- Larger chunks (1024-2048): Better for context preservation

### Batch Processing

- Use `load_batch()` for multiple documents
- Processes documents sequentially but handles errors gracefully
- Memory usage scales with document size and batch size

### OCR Settings

- Enable OCR only for scanned documents or images
- OCR processing is significantly slower than text extraction
- Consider disabling for pure text documents