"""
Main Sifu application class.
"""
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from .context import ContextManager
from .knowledge import KnowledgeBase
from .learning import LearningEngine
from .matcher import IntentMatcher
from .language import LanguageProcessor
from .api import SifuAPI
from .config import settings

logger = logging.getLogger(__name__)

class Sifu:
    """Main Sifu application class."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Sifu application.
        
        Args:
            config: Optional configuration overrides
        """
        self.config = config or {}
        self._setup_logging()
        
        # Initialize core components
        self.knowledge_base = KnowledgeBase()
        self.context_manager = ContextManager()
        self.language_processor = LanguageProcessor()
        self.intent_matcher = IntentMatcher()
        self.learning_engine = LearningEngine()
        
        # Initialize API
        self.api = SifuAPI(self)
        
        logger.info("Sifu application initialized")
    
    def _setup_logging(self) -> None:
        """Configure logging based on settings."""
        log_level = self.config.get("LOG_LEVEL", settings.LOG_LEVEL)
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    async def process_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user query and generate a response.
        
        Args:
            query: The user's query text
            context: Additional context for the query
            user_id: Optional user ID for personalization
            
        Returns:
            Dictionary containing response and metadata
        """
        # Initialize response structure
        response = {
            "text": "",
            "context": {},
            "metadata": {
                "intent": None,
                "confidence": 0.0,
                "sources": [],
                "language": settings.DEFAULT_LANGUAGE,
                "suggested_responses": []
            }
        }
        
        try:
            # Update context with user info
            if user_id:
                self.context_manager.set_user(user_id)
            
            # Detect language
            lang_info = self.language_processor.detect_language(query)
            response["metadata"]["language"] = lang_info["language"]
            
            # Process query
            intent = self.intent_matcher.match(query, context)
            response["metadata"]["intent"] = intent["intent"]
            response["metadata"]["confidence"] = intent["confidence"]
            
            # Generate response based on intent
            if intent["confidence"] > 0.7:  # High confidence match
                response["text"] = self._generate_high_confidence_response(intent, context)
            else:  # Lower confidence, use fallback strategies
                response.update(self._handle_low_confidence(query, intent, context))
            
            # Update learning
            self.learning_engine.record_interaction(
                query=query,
                response=response,
                context=context
            )
            
            # Generate follow-up suggestions
            response["metadata"]["suggested_responses"] = self._generate_suggestions(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            return {
                "text": "I'm sorry, I encountered an error processing your request.",
                "error": str(e),
                "context": context or {}
            }
    
    def _generate_high_confidence_response(
        self,
        intent: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Generate response for high-confidence intent matches."""
        # This would be implemented based on the specific intent
        return f"I understand you're asking about {intent['intent']}. This is a placeholder response."
    
    def _handle_low_confidence(
        self,
        query: str,
        intent: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle queries with low confidence scores."""
        # Try to find similar queries in knowledge base
        similar = self.knowledge_base.find_similar(query, threshold=0.6)
        if similar:
            return {
                "text": f"I'm not entirely sure, but you might be asking about: {similar['question']}",
                "metadata": {
                    "suggested_responses": [
                        {"text": f"Yes, tell me more about {similar['question']}", "type": "confirmation"},
                        {"text": "No, that's not what I meant", "type": "rejection"}
                    ]
                }
            }
        
        # Fallback to general response
        return {
            "text": "I'm not sure I understand. Could you provide more details or rephrase your question?",
            "metadata": {
                "suggested_responses": [
                    {"text": "Can you rephrase that?", "type": "clarification"},
                    {"text": "Never mind", "type": "dismissal"}
                ]
            }
        }
    
    def _generate_suggestions(self, response: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate suggested follow-up responses."""
        # This would be implemented based on the current context and response
        return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the Sifu instance."""
        return {
            "status": "running",
            "version": __import__("sifu").__version__,
            "knowledge_base": {
                "entries": self.knowledge_base.count_entries(),
                "languages": self.knowledge_base.get_supported_languages()
            },
            "context": {
                "active_sessions": self.context_manager.count_active_sessions()
            }
        }
    
    async def close(self) -> None:
        """Clean up resources."""
        await self.knowledge_base.close()
        await self.context_manager.close()
        await self.learning_engine.close()
        logger.info("Sifu application shutdown complete")
