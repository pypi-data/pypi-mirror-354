"""
Language processing module for Sifu.

This module provides language detection, translation, and other
language-related functionality to support multilingual interactions.
"""

from typing import Dict, List, Optional, Tuple, Union, Any
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
import json

# Try to import language detection libraries
try:
    from langdetect import detect, detect_langs, LangDetectException
except ImportError:
    detect = detect_langs = None
    LangDetectException = Exception

# Try to import translation libraries
try:
    from googletrans import Translator as GoogleTranslator
except ImportError:
    GoogleTranslator = None

try:
    import spacy
except ImportError:
    spacy = None

from ..config import settings

logger = logging.getLogger(__name__)

@dataclass
class DetectedLanguage:
    """Represents a detected language with confidence score."""
    language: str
    confidence: float = 1.0
    is_reliable: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "language": self.language,
            "confidence": self.confidence,
            "is_reliable": self.is_reliable
        }

@dataclass
class TranslationResult:
    """Represents a translation result."""
    text: str
    source_language: str
    target_language: str
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "text": self.text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "confidence": self.confidence
        }

class LanguageDetector:
    """
    Detects the language of a given text.
    
    Uses multiple strategies to detect language with confidence scoring.
    """
    
    def __init__(self):
        """Initialize the language detector."""
        self.supported_languages = set(settings.SUPPORTED_LANGUAGES)
        self._setup_detectors()
    
    def _setup_detectors(self) -> None:
        """Set up available language detectors."""
        self.detectors = []
        
        if detect is not None:
            self.detectors.append(self._detect_with_langdetect)
        
        # Add more detectors as needed
    
    def detect(self, text: str, default: str = "en") -> DetectedLanguage:
        """
        Detect the language of the given text.
        
        Args:
            text: Text to detect language for
            default: Default language code if detection fails
            
        Returns:
            DetectedLanguage object with language and confidence
        """
        if not text or not text.strip():
            return DetectedLanguage(language=default, confidence=0.0, is_reliable=False)
        
        # Try each detector until we get a reliable result
        for detector in self.detectors:
            try:
                result = detector(text)
                if result.is_reliable and result.language in self.supported_languages:
                    return result
            except Exception as e:
                logger.warning(f"Language detection failed: {e}")
        
        # Fall back to default if no reliable detection
        return DetectedLanguage(
            language=default,
            confidence=0.0,
            is_reliable=False
        )
    
    def _detect_with_langdetect(self, text: str) -> DetectedLanguage:
        """
        Detect language using the langdetect library.
        
        Args:
            text: Text to detect language for
            
        Returns:
            DetectedLanguage object
        """
        try:
            # Get all possible languages with probabilities
            languages = detect_langs(text)
            
            if not languages:
                raise ValueError("No languages detected")
            
            # Get the most likely language
            best = languages[0]
            
            # Consider it reliable if confidence is high enough
            is_reliable = best.prob >= 0.8
            
            return DetectedLanguage(
                language=best.lang,
                confidence=float(best.prob),
                is_reliable=is_reliable
            )
            
        except LangDetectException as e:
            logger.warning(f"Language detection error: {e}")
            raise ValueError(f"Language detection failed: {e}")

class Translator:
    """
    Handles text translation between languages.
    
    Uses multiple translation backends with fallback mechanisms.
    """
    
    def __init__(self):
        """Initialize the translator."""
        self.supported_languages = set(settings.SUPPORTED_LANGUAGES)
        self._setup_translators()
    
    def _setup_translators(self) -> None:
        """Set up available translation backends."""
        self.translators = []
        
        if GoogleTranslator is not None:
            self.translators.append(GoogleTranslator())
    
    async def translate(
        self,
        text: str,
        target_lang: str = "en",
        source_lang: Optional[str] = None
    ) -> TranslationResult:
        """
        Translate text to the target language.
        
        Args:
            text: Text to translate
            target_lang: Target language code (ISO 639-1)
            source_lang: Optional source language code (auto-detected if None)
            
        Returns:
            TranslationResult object
        """
        if not text or not text.strip():
            return TranslationResult(
                text=text,
                source_language=source_lang or "",
                target_language=target_lang,
                confidence=0.0
            )
        
        # If source language is not provided, try to detect it
        if not source_lang:
            detector = LanguageDetector()
            detected = detector.detect(text)
            source_lang = detected.language
        
        # If source and target are the same, no translation needed
        if source_lang == target_lang:
            return TranslationResult(
                text=text,
                source_language=source_lang,
                target_language=target_lang,
                confidence=1.0
            )
        
        # Try each translator until one succeeds
        for translator in self.translators:
            try:
                return await self._translate_with(translator, text, target_lang, source_lang)
            except Exception as e:
                logger.warning(f"Translation failed with {translator.__class__.__name__}: {e}")
        
        # If all translators fail, return the original text with low confidence
        return TranslationResult(
            text=text,
            source_language=source_lang,
            target_language=target_lang,
            confidence=0.0
        )
    
    async def _translate_with(
        self,
        translator: Any,
        text: str,
        target_lang: str,
        source_lang: str
    ) -> TranslationResult:
        """
        Translate text using a specific translator.
        
        Args:
            translator: Translator instance
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code
            
        Returns:
            TranslationResult object
        """
        if isinstance(translator, GoogleTranslator):
            # Google Translate implementation
            result = translator.translate(text, dest=target_lang, src=source_lang)
            
            return TranslationResult(
                text=result.text,
                source_language=result.src,
                target_language=result.dest,
                confidence=0.9  # Google Translate is generally reliable
            )
        
        # Add more translator implementations here
        
        raise NotImplementedError(f"Unsupported translator: {translator.__class__.__name__}")

class TextProcessor:
    """
    Handles text preprocessing and normalization.
    """
    
    def __init__(self):
        """Initialize the text processor."""
        self._setup_processors()
    
    def _setup_processors(self) -> None:
        """Set up text processing pipelines."""
        # Initialize spaCy models if available
        self.nlp = {}
        
        if spacy is not None:
            try:
                # Try to load models for supported languages
                for lang in settings.SUPPORTED_LANGUAGES:
                    try:
                        self.nlp[lang] = spacy.load(f"{lang}_core_news_sm")
                    except OSError:
                        # Model not found, skip this language
                        continue
            except Exception as e:
                logger.warning(f"Failed to load spaCy models: {e}")
    
    def preprocess(
        self,
        text: str,
        language: str = "en",
        lowercase: bool = True,
        remove_punct: bool = True,
        remove_stopwords: bool = False,
        lemmatize: bool = False
    ) -> str:
        """
        Preprocess text with various options.
        
        Args:
            text: Input text
            language: Language code
            lowercase: Whether to convert to lowercase
            remove_punct: Whether to remove punctuation
            remove_stopwords: Whether to remove stop words
            lemmatize: Whether to lemmatize words
            
        Returns:
            Processed text
        """
        if not text:
            return ""
        
        # Apply basic preprocessing
        processed = text.strip()
        
        # Apply language-specific processing if available
        if language in self.nlp and (remove_punct or remove_stopwords or lemmatize):
            doc = self.nlp[language](processed)
            tokens = []
            
            for token in doc:
                # Skip unwanted tokens
                if remove_punct and token.is_punct:
                    continue
                if remove_stopwords and token.is_stop:
                    continue
                
                # Get the processed token text
                if lemmatize and token.lemma_:
                    token_text = token.lemma_
                else:
                    token_text = token.text
                
                tokens.append(token_text)
            
            processed = " ".join(tokens)
        
        # Apply case normalization
        if lowercase:
            processed = processed.lower()
        
        # Normalize whitespace
        processed = re.sub(r'\s+', ' ', processed).strip()
        
        return processed

# Create default instances for easy import
detector = LanguageDetector()
translator = Translator()
text_processor = TextProcessor()

def detect_language(text: str, default: str = "en") -> Dict[str, Any]:
    """
    Detect the language of the given text.
    
    Args:
        text: Text to detect language for
        default: Default language code if detection fails
        
    Returns:
        Dictionary with language information
    """
    return detector.detect(text, default).to_dict()

async def translate_text(
    text: str,
    target_lang: str = "en",
    source_lang: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate text to the target language.
    
    Args:
        text: Text to translate
        target_lang: Target language code (ISO 639-1)
        source_lang: Optional source language code (auto-detected if None)
        
    Returns:
        Dictionary with translation results
    """
    result = await translator.translate(text, target_lang, source_lang)
    return result.to_dict()

def preprocess_text(
    text: str,
    language: str = "en",
    lowercase: bool = True,
    remove_punct: bool = True,
    remove_stopwords: bool = False,
    lemmatize: bool = False
) -> str:
    """
    Preprocess text with various options.
    
    Args:
        text: Input text
        language: Language code
        lowercase: Whether to convert to lowercase
        remove_punct: Whether to remove punctuation
        remove_stopwords: Whether to remove stop words
        lemmatize: Whether to lemmatize words
        
    Returns:
        Processed text
    """
    return text_processor.preprocess(
        text=text,
        language=language,
        lowercase=lowercase,
        remove_punct=remove_punct,
        remove_stopwords=remove_stopwords,
        lemmatize=lemmatize
    )

__all__ = [
    "LanguageDetector",
    "Translator",
    "TextProcessor",
    "detector",
    "translator",
    "text_processor",
    "detect_language",
    "translate_text",
    "preprocess_text"
]
