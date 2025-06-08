import os
import logging
import asyncio
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import time
import uuid
import redis
from datetime import datetime, timedelta

# Local imports
from api.models.optimization import (
    TitleOptimizationRequest,
    TitleOptimizationResponse,
    BatchOptimizationRequest,
    BatchOptimizationResponse
)
from api.routers import optimization, analytics, users, youtube
from api.services.cache import RedisCache
from api.services.database import Database
from core.ai.gemini_service import GeminiService
from core.ai.openai_service import OpenAIService
from core.ai.anthropic_service import AnthropicService
from core.ai.model_factory import ModelFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Title Optimizer API",
    description="API for optimizing YouTube titles using AI",
    version="2.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    # Initialize Redis cache if available
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        cache = RedisCache(redis_url)
    else:
        cache = None
        logger.warning("Redis URL not provided. Running without cache.")
    
    # Initialize database connection
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        database = Database(db_url)
    else:
        database = None
        logger.warning("Database URL not provided. Running without database.")
    
    # Initialize AI services
    model_factory = ModelFactory(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
except Exception as e:
    logger.error(f"Error initializing services: {str(e)}")
    raise

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Get client IP
    client_ip = request.client.host
    
    # Skip rate limiting for certain paths
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)
    
    # Check if Redis is available for rate limiting
    if cache:
        # Rate limit: 60 requests per minute per IP
        rate_limit_key = f"rate_limit:{client_ip}"
        current_count = cache.redis.get(rate_limit_key)
        
        if current_count and int(current_count) >= 60:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Please try again later."}
            )
        
        # Increment counter and set expiry
        pipe = cache.redis.pipeline()
        pipe.incr(rate_limit_key)
        pipe.expire(rate_limit_key, 60)  # 60 seconds
        pipe.execute()
    
    # Continue processing the request
    return await call_next(request)

# Include routers
app.include_router(optimization.router, prefix="/api/v1", tags=["optimization"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(youtube.router, prefix="/api/v1", tags=["youtube"])

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": app.version,
        "services": {
            "cache": "available" if cache else "unavailable",
            "database": "available" if database else "unavailable",
            "ai_models": model_factory.available_models()
        }
    }

# Fallback error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
