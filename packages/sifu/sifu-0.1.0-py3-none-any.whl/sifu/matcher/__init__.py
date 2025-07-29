"""
Intent matching and pattern recognition module for Sifu.

This module provides functionality for matching user queries to intents
and extracting relevant entities using various matching strategies.
"""

from typing import Dict, List, Optional, Any, Tuple, Callable, Pattern
import re
import logging
import json
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import hashlib

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from ..config import settings
from ..language import text_processor, detector

logger = logging.getLogger(__name__)

@dataclass
class Intent:
    """Represents a user intent with patterns and examples."""
    name: str
    patterns: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    description: str = ""
    confidence_threshold: float = 0.7
    response_templates: List[str] = field(default_factory=list)
    entities: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_pattern(self, pattern: str) -> None:
        """Add a pattern to this intent."""
        self.patterns.append(pattern)
    
    def add_example(self, example: str) -> None:
        """Add an example to this intent."""
        self.examples.append(example)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "patterns": self.patterns,
            "examples": self.examples,
            "description": self.description,
            "confidence_threshold": self.confidence_threshold,
            "response_templates": self.response_templates,
            "entities": self.entities
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Intent':
        """Create from dictionary."""
        return cls(
            name=data["name"],
            patterns=data.get("patterns", []),
            examples=data.get("examples", []),
            description=data.get("description", ""),
            confidence_threshold=data.get("confidence_threshold", 0.7),
            response_templates=data.get("response_templates", []),
            entities=data.get("entities", [])
        )

@dataclass
class MatchResult:
    """Represents the result of an intent match."""
    intent: str
    confidence: float
    entities: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "intent": self.intent,
            "confidence": self.confidence,
            "entities": self.entities,
            "metadata": self.metadata
        }
    
    @property
    def is_confident(self) -> bool:
        """Check if the match is confident."""
        return self.confidence >= 0.7  # Default threshold

class IntentMatcher:
    """
    Matches user queries to predefined intents using various strategies.
    
    This class combines rule-based and ML-based approaches for intent recognition.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the intent matcher.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.intents: Dict[str, Intent] = {}
        self.patterns: List[Tuple[Pattern, str, float]] = []  # (pattern, intent_name, confidence)
        self.model = None
        self.model_name = model_name
        self.embeddings: Dict[str, np.ndarray] = {}
        self._setup_model()
    
    def _setup_model(self) -> None:
        """Set up the sentence transformer model."""
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded sentence transformer model: {self.model_name}")
        except Exception as e:
            logger.warning(f"Failed to load sentence transformer model: {e}")
            self.model = None
    
    def add_intent(self, intent: Intent) -> None:
        """
        Add an intent to the matcher.
        
        Args:
            intent: Intent to add
        """
        self.intents[intent.name] = intent
        
        # Precompile patterns for faster matching
        for pattern in intent.patterns:
            try:
                # Simple pattern matching with word boundaries
                regex = re.compile(
                    r'\b' + re.escape(pattern.lower()) + r'\b',
                    re.IGNORECASE
                )
                self.patterns.append((regex, intent.name, 0.9))  # High confidence for exact matches
            except re.error as e:
                logger.warning(f"Invalid regex pattern '{pattern}': {e}")
        
        # Add examples for ML-based matching
        if self.model and intent.examples:
            self._update_embeddings(intent)
    
    def _update_embeddings(self, intent: Intent) -> None:
        """
        Update embeddings for an intent's examples.
        
        Args:
            intent: Intent to update embeddings for
        """
        if not self.model or not intent.examples:
            return
            
        try:
            # Get embeddings for all examples
            example_texts = [
                self._preprocess_text(ex) for ex in intent.examples
            ]
            embeddings = self.model.encode(
                example_texts,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            
            # Store the average embedding for this intent
            if len(embeddings) > 0:
                self.embeddings[intent.name] = np.mean(embeddings, axis=0)
                
        except Exception as e:
            logger.error(f"Error updating embeddings for intent '{intent.name}': {e}")
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for matching.
        
        Args:
            text: Text to preprocess
            
        Returns:
            Preprocessed text
        """
        return text_processor.preprocess(
            text=text,
            lowercase=True,
            remove_punct=True,
            remove_stopwords=True,
            lemmatize=True
        )
    
    def match(self, text: str, context: Optional[Dict[str, Any]] = None) -> MatchResult:
        """
        Match text against known intents.
        
        Args:
            text: Text to match
            context: Additional context
            
        Returns:
            MatchResult with the best matching intent
        """
        if not text.strip():
            return MatchResult(intent="unknown", confidence=0.0)
        
        # Try pattern matching first (fast)
        pattern_match = self._match_patterns(text)
        if pattern_match and pattern_match.confidence >= 0.9:  # High confidence in pattern matches
            return pattern_match
        
        # Try ML-based matching
        ml_match = self._match_ml(text, context)
        
        # Return the best match
        if pattern_match and ml_match:
            if pattern_match.confidence > ml_match.confidence:
                return pattern_match
            return ml_match
        elif pattern_match:
            return pattern_match
        elif ml_match:
            return ml_match
        
        # No good match found
        return MatchResult(intent="unknown", confidence=0.0)
    
    def _match_patterns(self, text: str) -> Optional[MatchResult]:
        """
        Match text against pattern-based rules.
        
        Args:
            text: Text to match
            
        Returns:
            MatchResult if a match is found, else None
        """
        text_lower = text.lower()
        
        for pattern, intent_name, confidence in self.patterns:
            if pattern.search(text_lower):
                return MatchResult(
                    intent=intent_name,
                    confidence=confidence,
                    metadata={"matched_pattern": pattern.pattern}
                )
        
        return None
    
    def _match_ml(self, text: str, context: Optional[Dict[str, Any]] = None) -> Optional[MatchResult]:
        """
        Match text using ML-based similarity.
        
        Args:
            text: Text to match
            context: Additional context
            
        Returns:
            MatchResult if a match is found, else None
        """
        if not self.model or not self.embeddings:
            return None
        
        try:
            # Preprocess and embed the input text
            processed_text = self._preprocess_text(text)
            query_embedding = self.model.encode(
                [processed_text],
                convert_to_numpy=True,
                show_progress_bar=False
            )[0]
            
            # Calculate similarity to each intent
            similarities = {}
            for intent_name, intent_embedding in self.embeddings.items():
                # Reshape to 2D arrays for cosine_similarity
                query_2d = query_embedding.reshape(1, -1)
                intent_2d = intent_embedding.reshape(1, -1)
                
                # Calculate cosine similarity
                similarity = cosine_similarity(query_2d, intent_2d)[0][0]
                similarities[intent_name] = similarity
            
            # Get the best match
            if similarities:
                best_intent = max(similarities.items(), key=lambda x: x[1])
                intent_name, confidence = best_intent
                
                # Apply confidence threshold from intent
                intent = self.intents.get(intent_name)
                min_confidence = intent.confidence_threshold if intent else 0.7
                
                if confidence >= min_confidence:
                    return MatchResult(
                        intent=intent_name,
                        confidence=float(confidence),
                        metadata={
                            "method": "ml",
                            "similarity": float(confidence)
                        }
                    )
                    
        except Exception as e:
            logger.error(f"Error in ML-based matching: {e}")
        
        return None
    
    def load_intents_from_file(self, file_path: Path) -> None:
        """
        Load intents from a JSON file.
        
        Args:
            file_path: Path to the JSON file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                for item in data:
                    self.add_intent(Intent.from_dict(item))
            elif isinstance(data, dict):
                for intent_data in data.get("intents", []):
                    self.add_intent(Intent.from_dict(intent_data))
                    
            logger.info(f"Loaded {len(self.intents)} intents from {file_path}")
            
        except Exception as e:
            logger.error(f"Error loading intents from {file_path}: {e}")
            raise
    
    def get_intent(self, intent_name: str) -> Optional[Intent]:
        """
        Get an intent by name.
        
        Args:
            intent_name: Name of the intent to get
            
        Returns:
            The Intent object, or None if not found
        """
        return self.intents.get(intent_name)
    
    def list_intents(self) -> List[str]:
        """
        Get a list of all intent names.
        
        Returns:
            List of intent names
        """
        return list(self.intents.keys())
    
    def clear(self) -> None:
        """Clear all intents and patterns."""
        self.intents.clear()
        self.patterns.clear()
        self.embeddings.clear()

# Create a default instance for easy use
intent_matcher = IntentMatcher()

__all__ = [
    "Intent",
    "MatchResult",
    "IntentMatcher",
    "intent_matcher"
]
