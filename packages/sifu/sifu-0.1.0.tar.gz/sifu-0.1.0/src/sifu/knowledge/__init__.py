"""
Knowledge management system for Sifu.

This module provides the core knowledge management capabilities,
including storage, retrieval, and reasoning over knowledge.
"""

from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass, field, asdict
import json
import uuid
import time
from pathlib import Path
import logging

from ..config import settings

logger = logging.getLogger(__name__)

@dataclass
class KnowledgeEntry:
    """Represents a single piece of knowledge in the system."""
    id: str
    content: str
    metadata: Dict[str, Any]
    created_at: float
    updated_at: float
    confidence: float = 1.0
    source: str = "user"
    tags: List[str] = field(default_factory=list)
    language: str = "en"
    
    @classmethod
    def create(
        cls,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        language: str = "en",
        source: str = "user",
        confidence: float = 1.0
    ) -> 'KnowledgeEntry':
        """Create a new knowledge entry with current timestamps."""
        now = time.time()
        return cls(
            id=str(uuid.uuid4()),
            content=content,
            metadata=metadata or {},
            tags=tags or [],
            language=language,
            source=source,
            confidence=confidence,
            created_at=now,
            updated_at=now
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the entry to a dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeEntry':
        """Create an entry from a dictionary."""
        return cls(**data)

class KnowledgeBase:
    """
    Core knowledge management system for Sifu.
    
    Handles storage, retrieval, and reasoning over knowledge entries.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the knowledge base.
        
        Args:
            storage_path: Path to store the knowledge base. If None, uses in-memory storage.
        """
        self.storage_path = storage_path or settings.MODEL_CACHE_DIR / "knowledge"
        self.entries: Dict[str, KnowledgeEntry] = {}
        self._index = None  # Will be initialized on first use
        self._setup_storage()
    
    def _setup_storage(self) -> None:
        """Set up the storage directory and load existing knowledge."""
        if self.storage_path:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            self._load_knowledge()
    
    def _load_knowledge(self) -> None:
        """Load knowledge from storage."""
        if not self.storage_path or not self.storage_path.exists():
            return
            
        for file_path in self.storage_path.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    entry = KnowledgeEntry.from_dict(data)
                    self.entries[entry.id] = entry
            except Exception as e:
                logger.error(f"Error loading knowledge from {file_path}: {e}")
    
    def _save_entry(self, entry: KnowledgeEntry) -> None:
        """Save a single entry to storage."""
        if not self.storage_path:
            return
            
        try:
            file_path = self.storage_path / f"{entry.id}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(entry.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving knowledge entry {entry.id}: {e}")
    
    async def add_entry(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        language: str = "en",
        source: str = "user",
        confidence: float = 1.0
    ) -> KnowledgeEntry:
        """
        Add a new knowledge entry.
        
        Args:
            content: The main content of the knowledge
            metadata: Additional metadata
            tags: List of tags for categorization
            language: Language code (ISO 639-1)
            source: Source of the knowledge
            confidence: Confidence score (0.0 to 1.0)
            
        Returns:
            The created knowledge entry
        """
        entry = KnowledgeEntry.create(
            content=content,
            metadata=metadata or {},
            tags=tags or [],
            language=language,
            source=source,
            confidence=confidence
        )
        
        self.entries[entry.id] = entry
        self._save_entry(entry)
        
        # Update search index
        await self._update_index(entry)
        
        logger.info(f"Added new knowledge entry: {entry.id}")
        return entry
    
    async def update_entry(
        self,
        entry_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        confidence: Optional[float] = None
    ) -> Optional[KnowledgeEntry]:
        """
        Update an existing knowledge entry.
        
        Args:
            entry_id: ID of the entry to update
            content: New content (if updating)
            metadata: New metadata (will be merged with existing)
            tags: New tags (will replace existing)
            confidence: New confidence score
            
        Returns:
            The updated entry, or None if not found
        """
        if entry_id not in self.entries:
            return None
            
        entry = self.entries[entry_id]
        
        if content is not None:
            entry.content = content
        
        if metadata is not None:
            entry.metadata.update(metadata)
            
        if tags is not None:
            entry.tags = tags
            
        if confidence is not None:
            entry.confidence = max(0.0, min(1.0, confidence))
        
        entry.updated_at = time.time()
        self._save_entry(entry)
        
        # Update search index
        await self._update_index(entry)
        
        logger.info(f"Updated knowledge entry: {entry_id}")
        return entry
    
    async def delete_entry(self, entry_id: str) -> bool:
        """
        Delete a knowledge entry.
        
        Args:
            entry_id: ID of the entry to delete
            
        Returns:
            True if deleted, False if not found
        """
        if entry_id not in self.entries:
            return False
            
        # Remove from storage
        if self.storage_path:
            file_path = self.storage_path / f"{entry_id}.json"
            if file_path.exists():
                try:
                    file_path.unlink()
                except Exception as e:
                    logger.error(f"Error deleting knowledge file {file_path}: {e}")
        
        # Remove from memory
        del self.entries[entry_id]
        
        # Update search index
        await self._remove_from_index(entry_id)
        
        logger.info(f"Deleted knowledge entry: {entry_id}")
        return True
    
    async def search(
        self,
        query: str,
        limit: int = 10,
        min_confidence: float = 0.5,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for knowledge entries matching the query.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            min_confidence: Minimum confidence score (0.0 to 1.0)
            language: Filter by language code
            tags: Filter by tags
            
        Returns:
            List of matching entries with scores
        """
        # Initialize index if needed
        if self._index is None:
            await self._initialize_index()
        
        # Simple implementation - would use vector search in production
        results = []
        for entry in self.entries.values():
            # Apply filters
            if entry.confidence < min_confidence:
                continue
                
            if language and entry.language != language:
                continue
                
            if tags and not any(tag in entry.tags for tag in tags):
                continue
            
            # Simple text matching (would use embeddings in production)
            score = self._calculate_similarity(query, entry.content)
            if score >= min_confidence:
                result = entry.to_dict()
                result["score"] = score
                results.append(result)
        
        # Sort by score (descending)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:limit]
    
    def _calculate_similarity(self, query: str, content: str) -> float:
        """
        Calculate similarity between query and content.
        
        This is a simple implementation. In production, you would use
        sentence embeddings or other NLP techniques.
        """
        # Simple word overlap
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        if not query_words or not content_words:
            return 0.0
            
        intersection = len(query_words & content_words)
        union = len(query_words | content_words)
        
        return intersection / union if union > 0 else 0.0
    
    async def _initialize_index(self) -> None:
        """Initialize the search index."""
        # In a real implementation, this would set up a vector database
        # like FAISS, Annoy, or similar for efficient similarity search
        self._index = {}
        
        # Simple in-memory index for demo purposes
        for entry in self.entries.values():
            self._index[entry.id] = entry
    
    async def _update_index(self, entry: KnowledgeEntry) -> None:
        """Update the search index with a new or updated entry."""
        if self._index is None:
            await self._initialize_index()
        
        self._index[entry.id] = entry
    
    async def _remove_from_index(self, entry_id: str) -> None:
        """Remove an entry from the search index."""
        if self._index is not None and entry_id in self._index:
            del self._index[entry_id]
    
    def count_entries(self) -> int:
        """Get the total number of knowledge entries."""
        return len(self.entries)
    
    def get_supported_languages(self) -> List[str]:
        """Get a list of supported languages in the knowledge base."""
        languages = set()
        for entry in self.entries.values():
            languages.add(entry.language)
        return sorted(languages)
    
    async def find_similar(
        self,
        query: str,
        threshold: float = 0.6,
        limit: int = 5
    ) -> Optional[Dict[str, Any]]:
        """
        Find the most similar knowledge entry to the query.
        
        Args:
            query: The query to match against
            threshold: Minimum similarity score (0.0 to 1.0)
            limit: Maximum number of results to return
            
        Returns:
            The most similar entry with score, or None if none found above threshold
        """
        results = await self.search(query, limit=limit, min_confidence=threshold)
        return results[0] if results else None
    
    async def close(self) -> None:
        """Clean up resources."""
        self._index = None
        logger.info("Knowledge base closed")

# Create a default instance for easy import
knowledge_base = KnowledgeBase()

__all__ = ["KnowledgeBase", "KnowledgeEntry", "knowledge_base"]
