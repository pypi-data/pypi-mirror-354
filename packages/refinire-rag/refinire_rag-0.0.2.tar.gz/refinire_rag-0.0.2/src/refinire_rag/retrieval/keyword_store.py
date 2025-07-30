"""
Keyword-based document store with search capabilities
キーワードベース文書ストア（検索機能付き）

Provides full-text search capabilities using keyword-based algorithms
like BM25, TF-IDF, or other lexical search methods.

BM25、TF-IDF、その他の語彙検索手法などのキーワードベースアルゴリズムを
使用した全文検索機能を提供します。
"""

import logging
import time
from typing import List, Optional, Dict, Any, Type
from abc import abstractmethod

from .base import Retriever, RetrieverConfig, SearchResult, IndexableMixin
from ..models.document import Document

logger = logging.getLogger(__name__)


class KeywordStoreConfig(RetrieverConfig):
    """Configuration for KeywordStore retriever"""
    
    def __init__(self,
                 top_k: int = 10,
                 similarity_threshold: float = 0.0,
                 enable_filtering: bool = True,
                 algorithm: str = "bm25",
                 batch_size: int = 100,
                 index_path: Optional[str] = None,
                 **kwargs):
        """
        Initialize KeywordStore configuration
        
        Args:
            top_k: Maximum number of results to return
                  返す結果の最大数
            similarity_threshold: Minimum relevance score for results
                                結果の最小関連度スコア
            enable_filtering: Whether to enable metadata filtering
                            メタデータフィルタリングを有効にするか
            algorithm: Keyword search algorithm ("bm25", "tfidf", etc.)
                      キーワード検索アルゴリズム
            batch_size: Batch size for bulk operations
                       一括操作のバッチサイズ
            index_path: Path to save/load keyword index
                       キーワードインデックスの保存/読み込みパス
        """
        super().__init__(top_k=top_k,
                        similarity_threshold=similarity_threshold,
                        enable_filtering=enable_filtering)
        self.algorithm = algorithm
        self.batch_size = batch_size
        self.index_path = index_path
        
        # Set additional attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)


class KeywordStore(Retriever, IndexableMixin):
    """Keyword-based document store with search capabilities
    
    Abstract base class for keyword-based search implementations.
    Subclasses should implement specific algorithms like BM25, TF-IDF, etc.
    
    キーワードベース検索実装の抽象基底クラス。
    サブクラスはBM25、TF-IDFなどの特定のアルゴリズムを実装する必要があります。
    """
    
    def __init__(self, config: Optional[KeywordStoreConfig] = None):
        """
        Initialize KeywordStore
        
        Args:
            config: KeywordStore configuration
                   KeywordStore設定
        """
        super().__init__(config or KeywordStoreConfig())
        self.documents: Dict[str, Document] = {}
        self.index_built = False
        
        logger.info(f"Initialized KeywordStore with {self.config.algorithm} algorithm")
    
    @classmethod
    def get_config_class(cls) -> Type[KeywordStoreConfig]:
        """Get configuration class for this retriever"""
        return KeywordStoreConfig
    
    @abstractmethod
    def _build_index(self) -> None:
        """Build keyword search index from documents"""
        pass
    
    @abstractmethod
    def _search_index(self, query: str, limit: int) -> List[tuple]:
        """
        Search the keyword index
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of (document_id, score) tuples
        """
        pass
    
    @abstractmethod
    def _clear_index(self) -> None:
        """Clear the keyword index"""
        pass
    
    def retrieve(self, 
                 query: str, 
                 limit: Optional[int] = None,
                 metadata_filter: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """
        Retrieve relevant documents using keyword search
        
        Args:
            query: Search query text
                  検索クエリテキスト
            limit: Maximum number of results (uses config.top_k if None)
                  結果の最大数（Noneの場合はconfig.top_kを使用）
            metadata_filter: Metadata filters for constraining search
                           検索を制約するメタデータフィルタ
                           
        Returns:
            List[SearchResult]: Search results sorted by relevance
                               関連度でソートされた検索結果
        """
        start_time = time.time()
        limit = limit or self.config.top_k
        
        try:
            logger.debug(f"Keyword search for query: '{query}' (limit={limit})")
            
            # Ensure index is built
            if not self.index_built:
                self._build_index()
                self.index_built = True
            
            # Perform keyword search
            search_results_raw = self._search_index(query, limit * 2)  # Get more for filtering
            
            # Convert to SearchResult objects with filtering
            search_results = []
            for doc_id, score in search_results_raw:
                if doc_id not in self.documents:
                    continue
                
                doc = self.documents[doc_id]
                
                # Apply similarity threshold filtering
                if self.config.enable_filtering and score < self.config.similarity_threshold:
                    continue
                
                # Apply metadata filtering
                if self.config.enable_filtering and metadata_filter:
                    if not self._matches_metadata_filter(doc.metadata, metadata_filter):
                        continue
                
                search_result = SearchResult(
                    document_id=doc_id,
                    document=doc,
                    score=score,
                    metadata={
                        "retrieval_method": "keyword_search",
                        "algorithm": self.config.algorithm,
                        "query_length": len(query),
                        "keyword_store": type(self).__name__
                    }
                )
                search_results.append(search_result)
                
                # Stop when we have enough results
                if len(search_results) >= limit:
                    break
            
            # Update statistics
            processing_time = time.time() - start_time
            self.processing_stats["queries_processed"] += 1
            self.processing_stats["processing_time"] += processing_time
            
            logger.debug(f"Keyword search completed: {len(search_results)} results in {processing_time:.3f}s")
            return search_results
            
        except Exception as e:
            self.processing_stats["errors_encountered"] += 1
            logger.error(f"Keyword search failed: {e}")
            return []
    
    def index_document(self, document: Document) -> None:
        """
        Index a single document for keyword search
        
        Args:
            document: Document to index
                     インデックスする文書
        """
        try:
            self.documents[document.id] = document
            # Mark index as needing rebuild
            self.index_built = False
            
            logger.debug(f"Added document to keyword index: {document.id}")
            
        except Exception as e:
            logger.error(f"Failed to index document {document.id}: {e}")
            raise
    
    def index_documents(self, documents: List[Document]) -> None:
        """
        Index multiple documents efficiently
        
        Args:
            documents: List of documents to index
                      インデックスする文書のリスト
        """
        try:
            for doc in documents:
                self.documents[doc.id] = doc
            
            # Mark index as needing rebuild
            self.index_built = False
            
            logger.info(f"Added {len(documents)} documents to keyword index")
            
        except Exception as e:
            logger.error(f"Failed to index documents: {e}")
            raise
    
    def remove_document(self, document_id: str) -> bool:
        """
        Remove document from keyword index
        
        Args:
            document_id: ID of document to remove
                        削除する文書のID
                        
        Returns:
            bool: True if document was found and removed
                 文書が見つかって削除された場合True
        """
        try:
            if document_id in self.documents:
                del self.documents[document_id]
                # Mark index as needing rebuild
                self.index_built = False
                logger.debug(f"Removed document from keyword index: {document_id}")
                return True
            else:
                logger.warning(f"Document not found in keyword index: {document_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to remove document {document_id}: {e}")
            return False
    
    def update_document(self, document: Document) -> bool:
        """
        Update an existing document in the keyword index
        
        Args:
            document: Updated document
                     更新する文書
                     
        Returns:
            bool: True if document was found and updated
                 文書が見つかって更新された場合True
        """
        try:
            if document.id in self.documents:
                self.documents[document.id] = document
                # Mark index as needing rebuild
                self.index_built = False
                logger.debug(f"Updated document in keyword index: {document.id}")
                return True
            else:
                logger.warning(f"Document not found for update: {document.id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update document {document.id}: {e}")
            return False
    
    def clear_index(self) -> None:
        """
        Remove all documents from the keyword index
        """
        try:
            self.documents.clear()
            self._clear_index()
            self.index_built = False
            logger.info("Cleared keyword index")
            
        except Exception as e:
            logger.error(f"Failed to clear keyword index: {e}")
            raise
    
    def get_document_count(self) -> int:
        """
        Get the number of documents in the keyword index
        
        Returns:
            int: Number of indexed documents
        """
        return len(self.documents)
    
    def _matches_metadata_filter(self, metadata: Dict[str, Any], metadata_filter: Dict[str, Any]) -> bool:
        """
        Check if document metadata matches the filter
        
        Args:
            metadata: Document metadata
            metadata_filter: Filter conditions
            
        Returns:
            bool: True if metadata matches filter
        """
        for key, value in metadata_filter.items():
            if key not in metadata:
                return False
            
            if isinstance(value, list):
                # OR condition: metadata value must be in the list
                if metadata[key] not in value:
                    return False
            elif isinstance(value, dict):
                # Range or complex condition (could be extended)
                if "$gte" in value and metadata[key] < value["$gte"]:
                    return False
                if "$lte" in value and metadata[key] > value["$lte"]:
                    return False
                if "$ne" in value and metadata[key] == value["$ne"]:
                    return False
            else:
                # Exact match
                if metadata[key] != value:
                    return False
        
        return True
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics with KeywordStore-specific metrics"""
        stats = super().get_processing_stats()
        
        # Add KeywordStore-specific stats
        stats.update({
            "retriever_type": "KeywordStore",
            "algorithm": self.config.algorithm,
            "similarity_threshold": self.config.similarity_threshold,
            "top_k": self.config.top_k,
            "document_count": self.get_document_count(),
            "index_built": self.index_built
        })
        
        return stats


class TFIDFKeywordStore(KeywordStore):
    """TF-IDF based keyword search implementation
    
    Simple implementation using scikit-learn's TfidfVectorizer.
    """
    
    def __init__(self, config: Optional[KeywordStoreConfig] = None):
        super().__init__(config)
        self.vectorizer = None
        self.tfidf_matrix = None
        
    def _build_index(self) -> None:
        """Build TF-IDF index from documents"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            if not self.documents:
                return
            
            # Extract document texts
            doc_ids = list(self.documents.keys())
            doc_texts = [self.documents[doc_id].content for doc_id in doc_ids]
            
            # Build TF-IDF matrix
            self.vectorizer = TfidfVectorizer(
                max_features=10000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(doc_texts)
            self.doc_ids = doc_ids
            
            logger.info(f"Built TF-IDF index for {len(doc_texts)} documents")
            
        except ImportError:
            logger.error("scikit-learn required for TF-IDF implementation")
            raise
        except Exception as e:
            logger.error(f"Failed to build TF-IDF index: {e}")
            raise
    
    def _search_index(self, query: str, limit: int) -> List[tuple]:
        """Search TF-IDF index"""
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            
            if self.vectorizer is None or self.tfidf_matrix is None:
                return []
            
            # Vectorize query
            query_vec = self.vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            
            # Get top results
            top_indices = similarities.argsort()[::-1][:limit]
            
            results = []
            for idx in top_indices:
                doc_id = self.doc_ids[idx]
                score = float(similarities[idx])
                if score > 0:  # Only include non-zero similarities
                    results.append((doc_id, score))
            
            return results
            
        except Exception as e:
            logger.error(f"TF-IDF search failed: {e}")
            return []
    
    def _clear_index(self) -> None:
        """Clear TF-IDF index"""
        self.vectorizer = None
        self.tfidf_matrix = None
        self.doc_ids = []