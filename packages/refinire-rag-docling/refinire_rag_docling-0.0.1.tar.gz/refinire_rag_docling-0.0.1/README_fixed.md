# Refinire-RAG Docling Plugin

A powerful document processing plugin for refinire-rag that leverages IBM's Docling library to read and process various document formats including PDF, DOCX, XLSX, HTML, and images.

## Features

=Â- **Multi-format Support**: PDF, DOCX, XLSX, HTML, PNG, JPG, JPEG  
=Ñ **Advanced PDF Processing**: Page layout analysis, reading order, table structure, code, formulas  
>ì **Unified Output**: Consistent document representation across all formats  
ª- **Flexible Export**: Markdown, plain text, and JSON output formats  
=- **Local Processing**: Secure document processing without external API calls  
= **OCR Support**: Built-in OCR for scanned documents and images  
¡ **Batch Processing**: Efficient handling of multiple documents  
>é **Chunking**: Automatic text chunking for RAG applications

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd refinire-rag-docling

# Install with uv (recommended)
uv add refinire-rag-docling

# Or install with pip
pip install refinire-rag-docling
```

## Quick Start

### Basic Usage

```python
from refinire_rag_docling import DoclingLoader

# Create loader with default settings
loader = DoclingLoader()

# Load a single document
documents = loader.load("path/to/document.pdf")

# Access processed content
for doc in documents:
    print(doc["content"])
    print(doc["metadata"])
```

### Custom Configuration

```python
from refinire_rag_docling import DoclingLoader, ConversionConfig, ExportFormat

# Configure processing options
config = ConversionConfig(
    export_format=ExportFormat.MARKDOWN,
    chunk_size=1024,
    ocr_enabled=True,
    table_structure=True
)

loader = DoclingLoader(config)
documents = loader.load("document.pdf")
```

### Factory Methods

```python
# Quick setup for markdown output
loader = DoclingLoader.create_with_markdown_output(chunk_size=512)

# Quick setup for text output
loader = DoclingLoader.create_with_text_output(chunk_size=2048)
```

### Batch Processing

```python
file_paths = ["doc1.pdf", "doc2.docx", "doc3.xlsx"]
documents = loader.load_batch(file_paths)

print(f"Processed {len(documents)} documents")
```

## Supported Formats

| Format | Extension | Features |
|--------|-----------|----------|
| PDF | `.pdf` | Layout analysis, OCR, table extraction |
| Word | `.docx` | Text, formatting, metadata |
| Excel | `.xlsx` | Spreadsheet data, multiple sheets |
| HTML | `.html` | Web content, structure |
| Images | `.png`, `.jpg`, `.jpeg` | OCR text extraction |

## Configuration Options

### ConversionConfig

```python
config = ConversionConfig(
    export_format=ExportFormat.MARKDOWN,  # MARKDOWN, TEXT, JSON
    chunk_size=512,                       # 100-4096 characters
    ocr_enabled=True,                     # Enable OCR for images
    table_structure=True,                 # Preserve table structure
    options={}                            # Additional options
)
```

### Export Formats

- **MARKDOWN**: Rich text with formatting, tables, and structure
- **TEXT**: Plain text content only
- **JSON**: Structured data with metadata

## Document Structure

Each processed document returns a dictionary with:

```python
{
    "content": "Extracted text content...",
    "metadata": {
        "source": "/path/to/file",
        "format": "pdf",
        "file_size": 1024,
        "page_count": 5,
        "processing_time": 2.3
    },
    "chunks": ["chunk1", "chunk2", ...],  # If chunking enabled
}
```

## Development

### Setup Development Environment

```bash
# Clone and setup
git clone <repository-url>
cd refinire-rag-docling

# Install dependencies
uv add --dev pytest pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

### Project Structure

```
refinire-rag-docling/
--- src/
-   --- refinire_rag_docling/
-       --- __init__.py
-       --- loader.py          # Main DoclingLoader class
-       --- models.py          # Data models and types
-       --- services.py        # Document processing logic
--- tests/
-   --- unit/                  # Unit tests
-   --- e2e/                   # Integration tests
--- examples/                  # Usage examples
--- docs/                      # Documentation
--- pyproject.toml
```

### Running Tests

```bash
# All tests
pytest tests/

# Unit tests only
pytest tests/unit/

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## Error Handling

The plugin includes comprehensive error handling:

```python
from refinire_rag_docling import (
    DoclingLoaderError,
    FileFormatNotSupportedError,
    DocumentProcessingError,
    ConfigurationError
)

try:
    documents = loader.load("document.pdf")
except FileFormatNotSupportedError:
    print("Unsupported file format")
except DocumentProcessingError as e:
    print(f"Processing failed: {e}")
```

## Performance Tips

1. **Batch Processing**: Use `load_batch()` for multiple files
2. **Chunk Size**: Optimize chunk size for your RAG system
3. **OCR Settings**: Disable OCR for text-based documents
4. **Format Selection**: Choose appropriate export format

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Dependencies

- [Docling](https://github.com/docling-project/docling): Document processing engine
- Python 3.10+

## Acknowledgments

- IBM DS4SD team for the Docling library
- The refinire-rag ecosystem

## Support

- =Ö [Documentation](./docs/)
- =- [Issue Tracker](https://github.com/your-repo/issues)
- =¬ [Discussions](https://github.com/your-repo/discussions)