"""
Base classes for retrieval components

Defines the core interfaces for QueryComponent and its implementations:
Retriever, Reranker, and Reader components used in QueryEngine.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Type
import numpy as np

from ..models.document import Document


@dataclass
class SearchResult:
    """Search result from retrieval"""
    document_id: str
    document: Document
    score: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class QueryResult:
    """Final query result with answer"""
    query: str
    normalized_query: Optional[str] = None
    answer: str = ""
    sources: List[SearchResult] = None
    confidence: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.sources is None:
            self.sources = []
        if self.metadata is None:
            self.metadata = {}


class QueryComponentConfig:
    """Base configuration for query components"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


@dataclass
class RetrieverConfig(QueryComponentConfig):
    """Configuration for retrievers"""
    top_k: int = 10
    similarity_threshold: float = 0.0
    enable_filtering: bool = True


@dataclass  
class RerankerConfig(QueryComponentConfig):
    """Configuration for rerankers"""
    top_k: int = 5
    rerank_model: str = "cross-encoder"
    score_threshold: float = 0.0


@dataclass
class ReaderConfig(QueryComponentConfig):
    """Configuration for readers"""
    max_context_length: int = 2000
    llm_model: str = "gpt-4o-mini"
    temperature: float = 0.1
    max_tokens: int = 500


class QueryComponent(ABC):
    """Base class for query processing components
    
    Similar to DocumentProcessor but for query processing workflow.
    Provides unified interface for Retriever, Reranker, and Reader.
    """
    
    def __init__(self, config: Optional[QueryComponentConfig] = None):
        self.config = config or QueryComponentConfig()
        
        # Processing statistics
        self.processing_stats = {
            "queries_processed": 0,
            "processing_time": 0.0,
            "errors_encountered": 0
        }
    
    @classmethod
    @abstractmethod
    def get_config_class(cls) -> Type[QueryComponentConfig]:
        """Get the configuration class for this component"""
        pass
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return self.processing_stats.copy()


class Retriever(QueryComponent):
    """Base class for document retrievers
    
    Unified interface for all document retrieval implementations including
    vector search, keyword search, and hybrid approaches.
    
    すべての文書検索実装（ベクトル検索、キーワード検索、ハイブリッドアプローチ）
    の統一インターフェース。
    """
    
    @classmethod
    @abstractmethod
    def get_config_class(cls) -> Type[RetrieverConfig]:
        """Get the configuration class for this retriever"""
        pass
    
    @abstractmethod
    def retrieve(self, 
                 query: str, 
                 limit: Optional[int] = None,
                 metadata_filter: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Retrieve relevant documents for query
        
        Args:
            query: Search query text
                  検索クエリテキスト
            limit: Maximum number of results to return (uses config.top_k if None)
                  返す結果の最大数（Noneの場合はconfig.top_kを使用）
            metadata_filter: Optional metadata filters for constraining search
                           検索を制約するオプションのメタデータフィルタ
                           Example: {"department": "AI", "year": 2024, "status": "active"}
            
        Returns:
            List[SearchResult]: List of search results with scores, sorted by relevance
                               関連度でソートされたスコア付き検索結果のリスト
        """
        pass


class IndexableMixin:
    """Mixin for document indexing capabilities
    
    Provides document indexing and management functionality that can be
    mixed into Retriever implementations to create searchable stores.
    
    検索可能なストアを作成するためにRetriever実装にミックスインできる
    文書インデックスと管理機能を提供します。
    """
    
    @abstractmethod
    def index_document(self, document: Document) -> None:
        """Index a single document for search
        
        Args:
            document: Document to index
                     インデックスする文書
        """
        pass
    
    @abstractmethod
    def index_documents(self, documents: List[Document]) -> None:
        """Index multiple documents efficiently
        
        Args:
            documents: List of documents to index
                      インデックスする文書のリスト
        """
        pass
    
    @abstractmethod
    def remove_document(self, document_id: str) -> bool:
        """Remove document from index
        
        Args:
            document_id: ID of document to remove
                        削除する文書のID
                        
        Returns:
            bool: True if document was found and removed, False otherwise
                 文書が見つかって削除された場合True、そうでなければFalse
        """
        pass
    
    @abstractmethod
    def update_document(self, document: Document) -> bool:
        """Update an existing document in the index
        
        Args:
            document: Updated document (must have existing ID)
                     更新する文書（既存のIDを持つ必要がある）
                     
        Returns:
            bool: True if document was found and updated, False otherwise
                 文書が見つかって更新された場合True、そうでなければFalse
        """
        pass
    
    @abstractmethod
    def clear_index(self) -> None:
        """Remove all documents from the index
        
        インデックスからすべての文書を削除
        """
        pass
    
    @abstractmethod
    def get_document_count(self) -> int:
        """Get the number of documents in the index
        
        Returns:
            int: Number of indexed documents
                インデックスされた文書数
        """
        pass
    
    def index_document_batch(self, documents: List[Document], batch_size: int = 100) -> None:
        """Index documents in batches for better performance
        
        Args:
            documents: Documents to index
                      インデックスする文書
            batch_size: Number of documents per batch
                       バッチあたりの文書数
        """
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            self.index_documents(batch)


class Reranker(QueryComponent):
    """Base class for result rerankers"""
    
    @classmethod
    @abstractmethod
    def get_config_class(cls) -> Type[RerankerConfig]:
        """Get the configuration class for this reranker"""
        pass
    
    @abstractmethod
    def rerank(self, query: str, results: List[SearchResult]) -> List[SearchResult]:
        """Rerank search results based on relevance
        
        Args:
            query: Original query
            results: Initial search results
            
        Returns:
            Reranked search results
        """
        pass


class Reader(QueryComponent):
    """Base class for answer readers/generators"""
    
    @classmethod
    @abstractmethod
    def get_config_class(cls) -> Type[ReaderConfig]:
        """Get the configuration class for this reader"""
        pass
    
    @abstractmethod
    def read(self, query: str, contexts: List[SearchResult]) -> str:
        """Generate answer from query and context documents
        
        Args:
            query: User query
            contexts: Relevant context documents
            
        Returns:
            Generated answer
        """
        pass