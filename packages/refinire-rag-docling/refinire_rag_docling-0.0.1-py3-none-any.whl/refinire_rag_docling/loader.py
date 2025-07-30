"""DoclingLoader implementation for refinire-rag integration."""

from typing import List, Dict, Any, Union
from pathlib import Path

from .models import ConversionConfig, ProcessingResult, ExportFormat
from .services import DocumentService


class DoclingLoader:
    """Docling-based document loader for RAG systems."""
    
    def __init__(self, config: ConversionConfig = None):
        """Initialize DoclingLoader with configuration."""
        self.config = config or ConversionConfig()
        self.service = DocumentService(self.config)
    
    def load(self, source: Union[str, Path]) -> List[Dict[str, Any]]:
        """Load a single document and return RAG-compatible format."""
        file_path = str(source)
        
        # Process document
        result = self.service.process_document(file_path)
        
        # Convert to RAG format
        rag_document = self._convert_to_rag_document(result)
        
        return [rag_document]
    
    def load_batch(self, sources: List[Union[str, Path]]) -> List[Dict[str, Any]]:
        """Load multiple documents in batch."""
        documents = []
        
        for source in sources:
            try:
                doc_list = self.load(source)
                documents.extend(doc_list)
            except Exception as e:
                # Log error but continue processing other documents
                print(f"Warning: Failed to process {source}: {e}")
                continue
        
        return documents
    
    def _convert_to_rag_document(self, result: ProcessingResult) -> Dict[str, Any]:
        """Convert ProcessingResult to RAG-compatible document format."""
        # Basic document structure expected by RAG systems
        document = {
            "content": result.content,
            "metadata": {
                "source": result.metadata.file_path,
                "file_size": result.metadata.file_size,
                "format": result.metadata.format.value,
                "processing_time": result.processing_time
            }
        }
        
        # Add optional metadata if available
        if result.metadata.page_count:
            document["metadata"]["page_count"] = result.metadata.page_count
        
        if result.metadata.title:
            document["metadata"]["title"] = result.metadata.title
        
        if result.metadata.author:
            document["metadata"]["author"] = result.metadata.author
        
        # Add chunks if content needs to be split
        if self.config.chunk_size and self.config.chunk_size < len(result.content):
            chunks = result.get_chunks(self.config.chunk_size)
            document["chunks"] = chunks
            document["metadata"]["chunk_count"] = len(chunks)
        
        return document
    
    @classmethod
    def create_with_markdown_output(cls, chunk_size: int = 512) -> "DoclingLoader":
        """Factory method for creating loader with markdown output."""
        config = ConversionConfig(
            export_format=ExportFormat.MARKDOWN,
            chunk_size=chunk_size
        )
        return cls(config)
    
    @classmethod 
    def create_with_text_output(cls, chunk_size: int = 512) -> "DoclingLoader":
        """Factory method for creating loader with text output."""
        config = ConversionConfig(
            export_format=ExportFormat.TEXT,
            chunk_size=chunk_size
        )
        return cls(config)