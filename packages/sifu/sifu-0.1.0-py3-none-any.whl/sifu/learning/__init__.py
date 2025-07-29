"""
Learning and adaptation system for Sifu.

This module provides the core learning capabilities that allow Sifu to
improve its responses over time based on user interactions and feedback.
"""

from typing import Dict, List, Optional, Any, Tuple, Set
import time
import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import random

from ..config import settings
from ..knowledge import KnowledgeBase, KnowledgeEntry
from ..context import Context, ContextManager

logger = logging.getLogger(__name__)

class LearningEngine:
    """
    Core learning engine that handles continuous improvement
    based on user interactions and feedback.
    """
    
    def __init__(
        self,
        knowledge_base: Optional[KnowledgeBase] = None,
        context_manager: Optional[ContextManager] = None,
        storage_path: Optional[Path] = None
    ):
        """
        Initialize the learning engine.
        
        Args:
            knowledge_base: Knowledge base instance
            context_manager: Context manager instance
            storage_path: Path to store learning data
        """
        self.knowledge_base = knowledge_base or KnowledgeBase()
        self.context_manager = context_manager or ContextManager()
        self.storage_path = storage_path or settings.MODEL_CACHE_DIR / "learning"
        self._setup_storage()
        
        # Learning parameters
        self.confidence_threshold = 0.7
        self.min_feedback_count = 3
        self.decay_factor = 0.95  # How quickly confidence decays without reinforcement
        
        # Load learning state
        self._load_state()
    
    def _setup_storage(self) -> None:
        """Set up storage directories."""
        if self.storage_path:
            self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def _load_state(self) -> None:
        """Load learning state from disk."""
        self.state_file = self.storage_path / "learning_state.json"
        self.state = {
            "last_learned": 0,
            "total_interactions": 0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "learning_rate": 0.1,
            "decay_factor": 0.95,
            "last_updated": time.time()
        }
        
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    self.state.update(json.load(f))
            except Exception as e:
                logger.error(f"Error loading learning state: {e}")
    
    def _save_state(self) -> None:
        """Save learning state to disk."""
        if not self.storage_path:
            return
            
        try:
            self.state["last_updated"] = time.time()
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving learning state: {e}")
    
    async def record_interaction(
        self,
        query: str,
        response: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        feedback: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record an interaction for learning purposes.
        
        Args:
            query: User's query
            response: System's response
            context: Additional context
            feedback: Optional feedback on the response
        """
        self.state["total_interactions"] += 1
        
        # Extract useful information
        intent = response.get("metadata", {}).get("intent")
        confidence = response.get("metadata", {}).get("confidence", 0.0)
        
        # If we have feedback, use it to improve
        if feedback:
            await self.process_feedback(query, response, feedback, context)
        
        # If confidence was low, consider this for active learning
        elif confidence < self.confidence_threshold:
            await self._handle_low_confidence(query, response, context)
        
        # Periodically save state
        if self.state["total_interactions"] % 10 == 0:
            self._save_state()
    
    async def process_feedback(
        self,
        query: str,
        response: Dict[str, Any],
        feedback: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Process user feedback to improve future responses.
        
        Args:
            query: Original user query
            response: System's response
            feedback: User feedback
            context: Additional context
        """
        rating = feedback.get("rating", 0)  # -1, 0, 1
        better_response = feedback.get("better_response")
        
        # Update feedback counts
        if rating > 0:
            self.state["positive_feedback"] += 1
        elif rating < 0:
            self.state["negative_feedback"] += 1
        
        # If we have a better response, learn from it
        if better_response:
            await self._learn_from_better_response(
                query=query,
                original_response=response,
                better_response=better_response,
                context=context
            )
        
        # Adjust learning parameters based on feedback
        self._adjust_learning_parameters(rating)
        
        logger.info(f"Processed feedback for query: {query[:50]}...")
    
    async def _learn_from_better_response(
        self,
        query: str,
        original_response: Dict[str, Any],
        better_response: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Learn from a user-provided better response.
        
        Args:
            query: Original user query
            original_response: System's original response
            better_response: User-provided better response
            context: Additional context
        """
        # Extract intent and metadata from original response
        metadata = original_response.get("metadata", {})
        intent = metadata.get("intent")
        
        # Create or update knowledge entry
        await self.knowledge_base.add_entry(
            content=query,
            metadata={
                "response": better_response,
                "intent": intent,
                "source": "user_feedback",
                **metadata
            },
            confidence=1.0,  # High confidence in user-provided corrections
            source="user_feedback"
        )
        
        logger.info(f"Learned better response for query: {query[:50]}...")
    
    async def _handle_low_confidence(
        self,
        query: str,
        response: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Handle cases where the system has low confidence in its response.
        
        Args:
            query: User's query
            response: System's response
            context: Additional context
        """
        # In a real implementation, this would trigger active learning
        # For now, just log it
        logger.info(f"Low confidence response for query: {query[:100]}...")
        
        # We could also store these for later review
        self._store_uncertain_example(query, response, context)
    
    def _store_uncertain_example(
        self,
        query: str,
        response: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Store uncertain examples for later review or active learning.
        
        Args:
            query: User's query
            response: System's response
            context: Additional context
        """
        if not self.storage_path:
            return
            
        try:
            # Create a unique filename based on query and timestamp
            timestamp = int(time.time())
            query_hash = hashlib.md5(query.encode()).hexdigest()[:8]
            filename = f"uncertain_{timestamp}_{query_hash}.json"
            
            # Prepare data to store
            data = {
                "query": query,
                "response": response,
                "context": context or {},
                "timestamp": timestamp,
                "query_hash": query_hash
            }
            
            # Save to file
            with open(self.storage_path / filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Error storing uncertain example: {e}")
    
    def _adjust_learning_parameters(self, feedback_rating: int) -> None:
        """
        Adjust learning parameters based on feedback.
        
        Args:
            feedback_rating: User's feedback rating (-1, 0, 1)
        """
        # Simple adjustment - in a real system, this would be more sophisticated
        if feedback_rating > 0:
            # Positive feedback - increase learning rate slightly
            self.state["learning_rate"] = min(
                0.5,  # Max learning rate
                self.state["learning_rate"] * 1.1  # 10% increase
            )
        elif feedback_rating < 0:
            # Negative feedback - decrease learning rate
            self.state["learning_rate"] = max(
                0.01,  # Min learning rate
                self.state["learning_rate"] * 0.9  # 10% decrease
            )
    
    async def decay_confidence(self) -> None:
        """
        Periodically decay confidence in knowledge entries
        to ensure the system stays up-to-date.
        """
        logger.info("Starting confidence decay process...")
        
        # In a real implementation, we would iterate through knowledge entries
        # and decay their confidence scores
        
        logger.info("Confidence decay process completed.")
    
    async def train_models(self) -> None:
        """
        Train or fine-tune models based on collected data.
        """
        logger.info("Starting model training...")
        
        # In a real implementation, this would train or fine-tune
        # the intent classification and response generation models
        
        logger.info("Model training completed.")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get learning statistics.
        
        Returns:
            Dictionary of learning statistics
        """
        return {
            "total_interactions": self.state["total_interactions"],
            "positive_feedback": self.state["positive_feedback"],
            "negative_feedback": self.state["negative_feedback"],
            "learning_rate": self.state["learning_rate"],
            "last_updated": datetime.fromtimestamp(self.state["last_updated"]).isoformat()
        }
    
    async def close(self) -> None:
        """Clean up resources."""
        self._save_state()
        logger.info("Learning engine closed")

# Create a default instance for easy import
learning_engine = LearningEngine()

__all__ = ["LearningEngine", "learning_engine"]
