"""
refinire-rag: RAG (Retrieval-Augmented Generation) functionality for Refinire

This package provides modular RAG capabilities with use cases implemented as
Refinire Step subclasses and single-responsibility backend modules.
"""

__version__ = "0.0.2"

# Core models
from .models.document import Document
from .models.config import LoadingConfig, LoadingResult

# Loaders
from .loaders.base import Loader, MetadataGenerator, PathBasedMetadataGenerator
from .loaders.universal import UniversalLoader
from .loaders.specialized import (
    SpecializedLoader,
    TextLoader,
    MarkdownLoader,
    PDFLoader,
    HTMLLoader,
    CSVLoader,
    JSONLoader
)
from .loaders.document_store_loader import DocumentStoreLoader

# Storage
from .storage import (
    DocumentStore, SearchResult, StorageStats, SQLiteDocumentStore,
    VectorStore, VectorSearchResult, VectorEntry, VectorStoreStats,
    InMemoryVectorStore, PickleVectorStore
)

# Processing
from .processing import DocumentProcessor, DocumentPipeline, DocumentProcessorConfig

# Chunking
from .chunking import Chunker, ChunkingConfig, TokenBasedChunker, SentenceAwareChunker

# Embedding
from .embedding import (
    Embedder, 
    EmbeddingConfig, 
    EmbeddingResult,
    OpenAIEmbedder,
    OpenAIEmbeddingConfig,
    TFIDFEmbedder,
    TFIDFEmbeddingConfig
)

# Use Cases
from .use_cases import CorpusManager, CorpusManagerConfig

# Exceptions
from .exceptions import (
    RefinireRAGError,
    LoaderError,
    EmbeddingError,
    StorageError
)

# Plugin detection utilities
def check_plugin_availability():
    """Check which optional plugins are available"""
    # Check which optional plugins are available
    # プラグインの利用可能性をチェック
    
    plugins = {}
    
    # Docling plugin for enhanced document parsing
    try:
        import refinire_rag_docling
        plugins['docling'] = True
    except ImportError:
        plugins['docling'] = False
    
    # ChromaDB plugin for vector storage
    try:
        import refinire_rag_chroma
        plugins['chroma'] = True
    except ImportError:
        plugins['chroma'] = False
    
    # BM25s plugin for lexical search
    try:
        import refinire_rag_bm25s
        plugins['bm25s'] = True
    except ImportError:
        plugins['bm25s'] = False
    
    return plugins

def get_available_plugins():
    """Get list of available plugin names"""
    # 利用可能なプラグイン名のリストを取得
    return [name for name, available in check_plugin_availability().items() if available]

__all__ = [
    # Version
    "__version__",
    
    # Core models
    "Document",
    "LoadingConfig", 
    "LoadingResult",
    
    # Loaders
    "Loader",
    "MetadataGenerator",
    "PathBasedMetadataGenerator",
    "UniversalLoader",
    "SpecializedLoader",
    "TextLoader",
    "MarkdownLoader", 
    "PDFLoader",
    "HTMLLoader",
    "CSVLoader",
    "JSONLoader",
    "DocumentStoreLoader",
    
    # Storage
    "DocumentStore",
    "SearchResult",
    "StorageStats", 
    "SQLiteDocumentStore",
    "VectorStore",
    "VectorSearchResult",
    "VectorEntry",
    "VectorStoreStats",
    "InMemoryVectorStore",
    "PickleVectorStore",
    
    # Processing
    "DocumentProcessor",
    "DocumentPipeline", 
    "DocumentProcessorConfig",
    
    # Chunking
    "Chunker",
    "ChunkingConfig",
    "TokenBasedChunker",
    "SentenceAwareChunker",
    
    # Embedding
    "Embedder",
    "EmbeddingConfig", 
    "EmbeddingResult",
    "OpenAIEmbedder",
    "OpenAIEmbeddingConfig",
    "TFIDFEmbedder",
    "TFIDFEmbeddingConfig",
    
    # Use Cases
    "CorpusManager",
    "CorpusManagerConfig",
    
    # Exceptions
    "RefinireRAGError",
    "LoaderError",
    "EmbeddingError",
    "StorageError",
    
    # Plugin utilities
    "check_plugin_availability",
    "get_available_plugins",
]