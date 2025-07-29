"""
Context management system for Sifu.

This module provides context management capabilities for maintaining
conversation state, user preferences, and contextual information.
"""

from typing import Dict, List, Optional, Any, Set
import time
import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

from ..config import settings

logger = logging.getLogger(__name__)

@dataclass
class ContextEntity:
    """Represents a single entity in the context."""
    type: str
    value: Any
    confidence: float = 1.0
    source: str = "system"
    last_updated: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextEntity':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class ConversationTurn:
    """Represents a single turn in a conversation."""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationTurn':
        """Create from dictionary."""
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=data.get("timestamp", time.time()),
            metadata=data.get("metadata", {})
        )

class ContextManager:
    """
    Manages conversation context and state.
    
    This class is responsible for maintaining the state of conversations,
    including history, entities, and user preferences.
    """
    
    def __init__(self, max_history: int = 20, storage_path: Optional[Path] = None):
        """
        Initialize the context manager.
        
        Args:
            max_history: Maximum number of conversation turns to keep in memory
            storage_path: Path to persist context data (optional)
        """
        self.max_history = max_history
        self.storage_path = storage_path or settings.MODEL_CACHE_DIR / "context"
        self.contexts: Dict[str, 'Context'] = {}
        self._setup_storage()
    
    def _setup_storage(self) -> None:
        """Set up storage directory."""
        if self.storage_path:
            self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def get_context(self, context_id: str) -> 'Context':
        """
        Get or create a context by ID.
        
        Args:
            context_id: Unique identifier for the context
            
        Returns:
            The context object
        """
        if context_id not in self.contexts:
            self.contexts[context_id] = Context(context_id, self)
            self._load_context(context_id)
        return self.contexts[context_id]
    
    def set_user(self, user_id: str) -> 'Context':
        """
        Set the current user context.
        
        Args:
            user_id: User ID
            
        Returns:
            The user's context
        """
        return self.get_context(f"user:{user_id}")
    
    def _load_context(self, context_id: str) -> None:
        """
        Load context from storage.
        
        Args:
            context_id: ID of the context to load
        """
        if not self.storage_path:
            return
            
        context_file = self.storage_path / f"{context_id}.json"
        if context_file.exists():
            try:
                with open(context_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.contexts[context_id].from_dict(data)
                logger.debug(f"Loaded context for {context_id}")
            except Exception as e:
                logger.error(f"Error loading context {context_id}: {e}")
    
    def save_context(self, context_id: str) -> None:
        """
        Save context to storage.
        
        Args:
            context_id: ID of the context to save
        """
        if not self.storage_path or context_id not in self.contexts:
            return
            
        context_file = self.storage_path / f"{context_id}.json"
        try:
            with open(context_file, 'w', encoding='utf-8') as f:
                json.dump(
                    self.contexts[context_id].to_dict(),
                    f,
                    ensure_ascii=False,
                    indent=2
                )
            logger.debug(f"Saved context for {context_id}")
        except Exception as e:
            logger.error(f"Error saving context {context_id}: {e}")
    
    async def close(self) -> None:
        """Clean up resources and save all contexts."""
        for context_id in list(self.contexts.keys()):
            self.save_context(context_id)
        logger.info("Context manager closed")
    
    def count_active_sessions(self) -> int:
        """Get the number of active sessions."""
        return len(self.contexts)

class Context:
    """
    Represents a conversation context.
    
    This class holds the state of a conversation, including history,
    entities, and other contextual information.
    """
    
    def __init__(self, context_id: str, manager: Optional[ContextManager] = None):
        """
        Initialize a new context.
        
        Args:
            context_id: Unique identifier for this context
            manager: Reference to the context manager (optional)
        """
        self.context_id = context_id
        self.manager = manager
        self.conversation_history: List[ConversationTurn] = []
        self.entities: Dict[str, ContextEntity] = {}
        self.metadata: Dict[str, Any] = {}
        self.created_at = time.time()
        self.updated_at = time.time()
        self._dirty = False
    
    def add_message(self, role: str, content: str, **metadata: Any) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            role: Role of the message sender ('user' or 'assistant')
            content: Message content
            **metadata: Additional metadata for the message
        """
        self.conversation_history.append(ConversationTurn(
            role=role,
            content=content,
            metadata=metadata or {}
        ))
        self.updated_at = time.time()
        self._dirty = True
        
        # Trim history if needed
        if len(self.conversation_history) > (self.manager.max_history if self.manager else 20):
            self.conversation_history.pop(0)
    
    def get_recent_messages(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get the most recent messages from the conversation.
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of message dictionaries
        """
        return [
            turn.to_dict()
            for turn in self.conversation_history[-limit:]
        ]
    
    def set_entity(self, name: str, value: Any, entity_type: str = "generic", 
                 confidence: float = 1.0, source: str = "system") -> None:
        """
        Set an entity in the context.
        
        Args:
            name: Entity name
            value: Entity value
            entity_type: Type of entity
            confidence: Confidence score (0.0 to 1.0)
            source: Source of the entity
        """
        self.entities[name] = ContextEntity(
            type=entity_type,
            value=value,
            confidence=confidence,
            source=source
        )
        self.updated_at = time.time()
        self._dirty = True
    
    def get_entity(self, name: str, default: Any = None) -> Any:
        """
        Get an entity from the context.
        
        Args:
            name: Entity name
            default: Default value if entity not found
            
        Returns:
            Entity value or default
        """
        entity = self.entities.get(name)
        return entity.value if entity else default
    
    def update_metadata(self, **kwargs: Any) -> None:
        """
        Update context metadata.
        
        Args:
            **kwargs: Key-value pairs to update
        """
        self.metadata.update(kwargs)
        self.updated_at = time.time()
        self._dirty = True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the context to a dictionary.
        
        Returns:
            Dictionary representation of the context
        """
        return {
            "context_id": self.context_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "conversation_history": [
                turn.to_dict() for turn in self.conversation_history
            ],
            "entities": {
                name: entity.to_dict()
                for name, entity in self.entities.items()
            },
            "metadata": self.metadata
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load context from a dictionary.
        
        Args:
            data: Dictionary containing context data
        """
        self.context_id = data.get("context_id", self.context_id)
        self.created_at = data.get("created_at", self.created_at)
        self.updated_at = data.get("updated_at", self.updated_at)
        
        # Load conversation history
        self.conversation_history = [
            ConversationTurn.from_dict(turn_data)
            for turn_data in data.get("conversation_history", [])
        ]
        
        # Load entities
        self.entities = {
            name: ContextEntity.from_dict(entity_data)
            for name, entity_data in data.get("entities", {}).items()
        }
        
        # Load metadata
        self.metadata = data.get("metadata", {})
        self._dirty = False
    
    def clear(self) -> None:
        """Clear the context."""
        self.conversation_history.clear()
        self.entities.clear()
        self.metadata.clear()
        self.updated_at = time.time()
        self._dirty = True
    
    def is_expired(self, ttl_seconds: int = 3600) -> bool:
        """
        Check if the context has expired.
        
        Args:
            ttl_seconds: Time-to-live in seconds
            
        Returns:
            True if expired, False otherwise
        """
        return (time.time() - self.updated_at) > ttl_seconds
    
    def __del__(self):
        """Save context on destruction if dirty."""
        if self._dirty and self.manager:
            self.manager.save_context(self.context_id)

# Create a default context manager for easy import
context_manager = ContextManager()

__all__ = ["Context", "ContextManager", "ContextEntity", "ConversationTurn", "context_manager"]
