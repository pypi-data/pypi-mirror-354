"""
Sifu API Module

This module provides a FastAPI-based web service for interacting with Sifu's
core functionality, including natural language processing, knowledge management,
and learning capabilities.
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
import logging
import time
import uuid

from ..app import Sifu
from ..config import settings
from ..knowledge import KnowledgeEntry
from ..matcher import MatchResult

logger = logging.getLogger(__name__)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class SifuAPI:
    """
    FastAPI application for the Sifu service.
    
    This class sets up the API endpoints and handles request/response
    processing for the Sifu service.
    """
    
    def __init__(self, sifu: Sifu):
        """
        Initialize the Sifu API.
        
        Args:
            sifu: Sifu application instance
        """
        self.sifu = sifu
        self.app = self._create_app()
        self._setup_routes()
    
    def _create_app(self) -> FastAPI:
        """Create and configure the FastAPI application."""
        app = FastAPI(
            title="Sifu API",
            description="API for Sifu - Enhanced Knowledge System for ELLMa",
            version="0.1.0",
            docs_url="/docs",
            redoc_url="/redoc",
        )
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add request logging middleware
        @app.middleware("http")
        async def log_requests(request: Request, call_next):
            request_id = str(uuid.uuid4())
            logger.info(f"Request: {request.method} {request.url} - ID: {request_id}")
            
            start_time = time.time()
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            
            logger.info(
                f"Response: {request.method} {request.url} - "
                f"Status: {response.status_code} - "
                f"Process time: {process_time:.2f}ms - "
                f"ID: {request_id}"
            )
            
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
            return response
        
        # Add exception handler
        @app.exception_handler(Exception)
        async def global_exception_handler(request: Request, exc: Exception):
            logger.error(f"Unhandled exception: {exc}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error",
                    "error": str(exc)
                }
            )
        
        return app
    
    def _setup_routes(self) -> None:
        """Set up API routes."""
        # Health check
        @self.app.get("/health", tags=["System"])
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "version": "0.1.0"}
        
        # Query processing
        @self.app.post("/query", response_model=Dict[str, Any], tags=["Core"])
        async def process_query(
            request: Dict[str, Any],
            token: str = Depends(oauth2_scheme)
        ) -> Dict[str, Any]:
            """
            Process a natural language query and return a response.
            
            Args:
                request: Dictionary containing 'text' key with the query
                
            Returns:
                Dictionary with response and metadata
            """
            query = request.get("text", "").strip()
            if not query:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Query text is required"
                )
            
            # Get user context if available
            context = request.get("context", {})
            user_id = context.get("user_id")
            
            # Process the query
            response = await self.sifu.process_query(query, context, user_id)
            
            return response
        
        # Knowledge management
        @self.app.post("/knowledge", response_model=Dict[str, Any], tags=["Knowledge"])
        async def add_knowledge(
            entry: Dict[str, Any],
            token: str = Depends(oauth2_scheme)
        ) -> Dict[str, Any]:
            """
            Add a new knowledge entry.
            
            Args:
                entry: Dictionary containing knowledge entry data
                
            Returns:
                Dictionary with the created entry
            """
            try:
                # Create a new knowledge entry
                knowledge_entry = await self.sifu.knowledge_base.add_entry(
                    content=entry.get("content", ""),
                    metadata=entry.get("metadata", {}),
                    tags=entry.get("tags", []),
                    language=entry.get("language", "en"),
                    source=entry.get("source", "api"),
                    confidence=entry.get("confidence", 1.0)
                )
                
                return {"status": "success", "id": knowledge_entry.id}
                
            except Exception as e:
                logger.error(f"Error adding knowledge: {e}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
        
        # Intent matching
        @self.app.post("/match", response_model=MatchResult, tags=["NLP"])
        async def match_intent(
            request: Dict[str, Any],
            token: str = Depends(oauth2_scheme)
        ) -> MatchResult:
            """
            Match text to an intent.
            
            Args:
                request: Dictionary containing 'text' key with the query
                
            Returns:
                MatchResult with the matched intent
            """
            text = request.get("text", "").strip()
            if not text:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Text is required"
                )
            
            context = request.get("context", {})
            
            # Get the intent matcher
            matcher = self.sifu.intent_matcher
            
            # Match the intent
            result = matcher.match(text, context)
            
            return result
        
        # Learning feedback
        @self.app.post("/feedback", response_model=Dict[str, Any], tags=["Learning"])
        async def provide_feedback(
            feedback: Dict[str, Any],
            token: str = Depends(oauth2_scheme)
        ) -> Dict[str, Any]:
            """
            Provide feedback on a response to improve the system.
            
            Args:
                feedback: Dictionary containing feedback data
                    - query: Original query
                    - response: System's response
                    - rating: Rating (-1, 0, 1)
                    - better_response: Optional better response
                    - context: Additional context
                    
            Returns:
                Dictionary with status
            """
            try:
                # Record the feedback
                await self.sifu.learning_engine.record_interaction(
                    query=feedback.get("query", ""),
                    response=feedback.get("response", {}),
                    feedback={
                        "rating": feedback.get("rating", 0),
                        "better_response": feedback.get("better_response"),
                        "context": feedback.get("context", {})
                    }
                )
                
                return {"status": "success", "message": "Feedback recorded"}
                
            except Exception as e:
                logger.error(f"Error processing feedback: {e}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
        
        # System status
        @self.app.get("/status", response_model=Dict[str, Any], tags=["System"])
        async def get_status() -> Dict[str, Any]:
            """Get system status and statistics."""
            return self.sifu.get_status()
        
        # Authentication (simple implementation)
        @self.app.post("/token")
        async def login(form_data: OAuth2PasswordRequestForm = Depends()):
            """
            Get an access token for API authentication.
            
            This is a simple implementation. In production, you would
            validate against a user database and use proper password hashing.
            """
            # Simple authentication for demo purposes
            if form_data.username == "admin" and form_data.password == "password":
                return {"access_token": "dummy_token", "token_type": "bearer"}
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Create a default API instance
api = SifuAPI(Sifu())

# Make the FastAPI app available for uvicorn
app = api.app

__all__ = ["SifuAPI", "api", "app"]
