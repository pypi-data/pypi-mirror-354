"""End-to-end integration tests for DoclingLoader."""

import pytest
from pathlib import Path
import tempfile
import io
from unittest.mock import patch, Mock

from refinire_rag_docling import (
    DoclingLoader, 
    ConversionConfig, 
    ExportFormat,
    SupportedFormat
)


class TestDoclingLoaderIntegration:
    """Integration tests for DoclingLoader with mocked Docling."""
    
    def create_sample_pdf_content(self) -> bytes:
        """Create a minimal PDF content for testing."""
        # This is a minimal PDF structure for testing
        pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
72 720 Td
(Hello World) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000210 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
306
%%EOF"""
        return pdf_content
    
    @patch('refinire_rag_docling.services.DocumentConverter')
    def test_load_pdf_document_markdown(self, mock_converter_class):
        """Test loading a PDF document with markdown output."""
        # Mock the DocumentConverter
        mock_converter = Mock()
        mock_converter_class.return_value = mock_converter
        
        # Mock the conversion result
        mock_result = Mock()
        mock_document = Mock()
        mock_document.export_to_markdown.return_value = "# Test Document\n\nThis is a test document."
        mock_document.pages = [1, 2]  # Mock 2 pages
        mock_result.document = mock_document
        
        mock_converter.convert.return_value = mock_result
        
        # Create temporary PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(self.create_sample_pdf_content())
            tmp_file_path = tmp_file.name
        
        try:
            # Create loader
            config = ConversionConfig(export_format=ExportFormat.MARKDOWN)
            loader = DoclingLoader(config)
            
            # Load document
            documents = loader.load(tmp_file_path)
            
            # Verify results
            assert len(documents) == 1
            doc = documents[0]
            
            assert doc["content"] == "# Test Document\n\nThis is a test document."
            assert doc["metadata"]["format"] == "pdf"
            assert doc["metadata"]["source"] == tmp_file_path
            assert "processing_time" in doc["metadata"]
            
            # Verify mock was called
            mock_converter.convert.assert_called_once_with(tmp_file_path)
            mock_document.export_to_markdown.assert_called_once()
            
        finally:
            Path(tmp_file_path).unlink()
    
    @patch('refinire_rag_docling.services.DocumentConverter')
    def test_load_docx_document_text(self, mock_converter_class):
        """Test loading a DOCX document with text output."""
        mock_converter = Mock()
        mock_converter_class.return_value = mock_converter
        
        mock_result = Mock()
        mock_document = Mock()
        mock_document.export_to_text.return_value = "This is plain text content."
        mock_result.document = mock_document
        
        mock_converter.convert.return_value = mock_result
        
        # Create temporary DOCX file (minimal content)
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
            tmp_file.write(b"PK\x03\x04")  # Minimal ZIP header for DOCX
            tmp_file_path = tmp_file.name
        
        try:
            config = ConversionConfig(export_format=ExportFormat.TEXT)
            loader = DoclingLoader(config)
            
            documents = loader.load(tmp_file_path)
            
            assert len(documents) == 1
            doc = documents[0]
            
            assert doc["content"] == "This is plain text content."
            assert doc["metadata"]["format"] == "docx"
            
            mock_document.export_to_text.assert_called_once()
            
        finally:
            Path(tmp_file_path).unlink()
    
    @patch('refinire_rag_docling.services.DocumentConverter')
    def test_load_batch_documents(self, mock_converter_class):
        """Test loading multiple documents in batch."""
        mock_converter = Mock()
        mock_converter_class.return_value = mock_converter
        
        def mock_convert(file_path):
            mock_result = Mock()
            mock_document = Mock()
            
            if file_path.endswith('.pdf'):
                mock_document.export_to_markdown.return_value = f"# PDF Content from {Path(file_path).name}"
                mock_document.pages = [1]
            else:  # DOCX
                mock_document.export_to_markdown.return_value = f"# DOCX Content from {Path(file_path).name}"
            
            mock_result.document = mock_document
            return mock_result
        
        mock_converter.convert.side_effect = mock_convert
        
        # Create temporary files
        pdf_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        docx_file = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
        
        try:
            pdf_file.write(self.create_sample_pdf_content())
            pdf_file.close()
            
            docx_file.write(b"PK\x03\x04")
            docx_file.close()
            
            loader = DoclingLoader()
            documents = loader.load_batch([pdf_file.name, docx_file.name])
            
            assert len(documents) == 2
            
            # Verify PDF document
            pdf_doc = next(doc for doc in documents if doc["metadata"]["format"] == "pdf")
            assert "PDF Content" in pdf_doc["content"]
            
            # Verify DOCX document
            docx_doc = next(doc for doc in documents if doc["metadata"]["format"] == "docx")
            assert "DOCX Content" in docx_doc["content"]
            
        finally:
            Path(pdf_file.name).unlink()
            Path(docx_file.name).unlink()
    
    def test_unsupported_file_format(self):
        """Test handling of unsupported file formats."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(b"This is a text file")
            tmp_file_path = tmp_file.name
        
        try:
            loader = DoclingLoader()
            
            # Should handle the error gracefully in batch processing
            documents = loader.load_batch([tmp_file_path])
            
            # Should return empty list due to unsupported format
            assert len(documents) == 0
            
        finally:
            Path(tmp_file_path).unlink()
    
    @patch('refinire_rag_docling.services.DocumentConverter')
    def test_chunking_large_document(self, mock_converter_class):
        """Test chunking of large documents."""
        mock_converter = Mock()
        mock_converter_class.return_value = mock_converter
        
        # Create large content
        large_content = " ".join([f"Word{i}" for i in range(200)])  # 200 words
        
        mock_result = Mock()
        mock_document = Mock()
        mock_document.export_to_markdown.return_value = large_content
        mock_document.pages = [1]
        mock_result.document = mock_document
        
        mock_converter.convert.return_value = mock_result
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(self.create_sample_pdf_content())
            tmp_file_path = tmp_file.name
        
        try:
            # Configure with small chunk size
            config = ConversionConfig(chunk_size=100)
            loader = DoclingLoader(config)
            
            documents = loader.load(tmp_file_path)
            
            assert len(documents) == 1
            doc = documents[0]
            
            # Should have chunks due to large content and small chunk size
            assert "chunks" in doc
            assert len(doc["chunks"]) > 1
            assert "chunk_count" in doc["metadata"]
            
        finally:
            Path(tmp_file_path).unlink()
    
    def test_factory_methods(self):
        """Test factory methods for creating loaders."""
        # Test markdown factory
        markdown_loader = DoclingLoader.create_with_markdown_output(chunk_size=1024)
        assert markdown_loader.config.export_format == ExportFormat.MARKDOWN
        assert markdown_loader.config.chunk_size == 1024
        
        # Test text factory
        text_loader = DoclingLoader.create_with_text_output(chunk_size=2048)
        assert text_loader.config.export_format == ExportFormat.TEXT
        assert text_loader.config.chunk_size == 2048