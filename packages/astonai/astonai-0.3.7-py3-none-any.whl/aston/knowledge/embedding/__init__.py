"""
Embedding functionality for code chunks.

This package provides utilities for generating vector embeddings from code chunks,
as well as storing and searching for similar code snippets.
"""

from aston.knowledge.embedding.embedding_service import EmbeddingService, EmbeddingServiceConfig
from aston.knowledge.embedding.vector_store import VectorStoreInterface, SearchResult 