"""Basic usage examples for refinire-rag-docling plugin."""

from pathlib import Path
from refinire_rag_docling import (
    DoclingLoader,
    ConversionConfig,
    ExportFormat,
    SupportedFormat
)


def example_basic_usage():
    """Basic usage example with default configuration."""
    print("=== Basic Usage Example ===")
    
    # Create loader with default configuration
    loader = DoclingLoader()
    
    # Load a single document (replace with actual file path)
    # documents = loader.load("path/to/your/document.pdf")
    
    print("Loader created with default configuration")
    print(f"Export format: {loader.config.export_format}")
    print(f"Chunk size: {loader.config.chunk_size}")
    print(f"OCR enabled: {loader.config.ocr_enabled}")


def example_custom_configuration():
    """Example with custom configuration."""
    print("\n=== Custom Configuration Example ===")
    
    # Create custom configuration
    config = ConversionConfig(
        export_format=ExportFormat.TEXT,
        chunk_size=1024,
        ocr_enabled=True,
        table_structure=True
    )
    
    # Create loader with custom config
    loader = DoclingLoader(config)
    
    print("Loader created with custom configuration")
    print(f"Export format: {config.export_format}")
    print(f"Chunk size: {config.chunk_size}")


def example_factory_methods():
    """Example using factory methods."""
    print("\n=== Factory Methods Example ===")
    
    # Create loader for markdown output
    markdown_loader = DoclingLoader.create_with_markdown_output(chunk_size=512)
    print(f"Markdown loader - Export format: {markdown_loader.config.export_format}")
    
    # Create loader for text output
    text_loader = DoclingLoader.create_with_text_output(chunk_size=2048)
    print(f"Text loader - Export format: {text_loader.config.export_format}")


def example_batch_processing():
    """Example of batch processing multiple documents."""
    print("\n=== Batch Processing Example ===")
    
    loader = DoclingLoader()
    
    # Example file paths (replace with actual files)
    file_paths = [
        "examples/sample1.pdf",
        "examples/sample2.docx", 
        "examples/sample3.xlsx"
    ]
    
    print("Batch processing configuration:")
    print(f"Files to process: {len(file_paths)}")
    
    # Note: Actual batch processing would require real files
    # documents = loader.load_batch(file_paths)
    # print(f"Processed documents: {len(documents)}")


def example_supported_formats():
    """Display supported file formats."""
    print("\n=== Supported Formats ===")
    
    print("Supported file formats:")
    for format_type in SupportedFormat:
        print(f"  - {format_type.value.upper()}")
    
    print("\nAvailable export formats:")
    for export_format in ExportFormat:
        print(f"  - {export_format.value}")


def example_error_handling():
    """Example of error handling."""
    print("\n=== Error Handling Example ===")
    
    loader = DoclingLoader()
    
    # Example of handling unsupported formats
    try:
        # This would raise FileFormatNotSupportedError for .txt files
        # documents = loader.load("unsupported_file.txt")
        print("File format validation will catch unsupported formats")
    except Exception as e:
        print(f"Error caught: {type(e).__name__}")
    
    # Example of batch processing with error tolerance
    problematic_files = [
        "nonexistent.pdf",
        "unsupported.txt",
        "valid_document.pdf"
    ]
    
    print("Batch processing handles individual file errors gracefully")
    # documents = loader.load_batch(problematic_files)
    # Only valid documents would be processed


def main():
    """Run all examples."""
    print("Refinire-RAG Docling Plugin Examples")
    print("=" * 50)
    
    example_basic_usage()
    example_custom_configuration()
    example_factory_methods()
    example_batch_processing()
    example_supported_formats()
    example_error_handling()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nTo test with actual files:")
    print("1. Place sample documents in the examples/ directory")
    print("2. Update file paths in the examples")
    print("3. Run: python examples/basic_usage.py")


if __name__ == "__main__":
    main()