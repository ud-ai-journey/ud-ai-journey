from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime

# Local imports
from api.models.optimization import (
    TitleOptimizationRequest,
    TitleOptimizationResponse,
    BatchOptimizationRequest,
    BatchOptimizationResponse
)
from core.ai.model_factory import ModelFactory, get_model_factory

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.post("/optimize", response_model=TitleOptimizationResponse)
async def optimize_title(
    request: TitleOptimizationRequest,
    model_factory: ModelFactory = Depends(get_model_factory)
):
    """
    Optimize a YouTube title using AI
    
    This endpoint takes a YouTube title and related information and returns
    an optimized version with alternatives and analysis.
    """
    try:
        # Get the appropriate AI service based on the model name
        model_name = request.model.lower().split()[0] if request.model else "gemini"
        ai_service = model_factory.get_service(model_name)
        
        # Call the AI service to optimize the title
        result = await ai_service.optimize_title(
            original_title=request.original_title,
            description=request.description,
            category=request.category,
            target_emotion=request.target_emotion,
            content_type=request.content_type,
            model_name=model_name,
            optimization_strength=request.optimization_strength,
            advanced_analysis=request.advanced_analysis
        )
        
        # Add metadata to the response
        result["metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "model_used": model_name,
            "request_id": str(request.request_id)
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error optimizing title: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to optimize title: {str(e)}"
        )

@router.post("/batch-optimize", response_model=BatchOptimizationResponse)
async def batch_optimize_titles(
    request: BatchOptimizationRequest,
    background_tasks: BackgroundTasks,
    model_factory: ModelFactory = Depends(get_model_factory)
):
    """
    Optimize multiple YouTube titles in batch
    
    This endpoint takes a list of YouTube titles and returns optimized versions.
    For large batches, processing happens in the background.
    """
    try:
        # Get the appropriate AI service
        model_name = request.model.lower().split()[0] if request.model else "gemini"
        ai_service = model_factory.get_service(model_name)
        
        # For small batches (≤5), process synchronously
        if len(request.titles) <= 5:
            optimized_titles = []
            
            for title in request.titles:
                result = await ai_service.optimize_title(
                    original_title=title,
                    description=request.description or "Batch optimization",
                    category=request.category,
                    target_emotion=request.target_emotion,
                    content_type=request.content_type,
                    model_name=model_name,
                    optimization_strength=request.optimization_strength,
                    advanced_analysis=False  # Simplified for batch processing
                )
                
                optimized_titles.append({
                    "original": title,
                    "optimized": result["improved_title"],
                    "seo_score": result.get("seo_score", 75)
                })
            
            return {
                "optimized_titles": optimized_titles,
                "status": "completed",
                "batch_id": str(request.batch_id)
            }
        
        # For larger batches, process in background
        else:
            # Create a job and return the ID
            batch_id = str(request.batch_id)
            
            # Add background task
            background_tasks.add_task(
                process_batch_optimization,
                batch_id,
                request,
                ai_service
            )
            
            return {
                "optimized_titles": [],
                "status": "processing",
                "batch_id": batch_id,
                "message": f"Processing {len(request.titles)} titles in the background. Check status with /batch-status/{batch_id}"
            }
            
    except Exception as e:
        logger.error(f"Error in batch optimization: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process batch: {str(e)}"
        )

@router.get("/batch-status/{batch_id}")
async def get_batch_status(batch_id: str):
    """Get the status of a batch optimization job"""
    # In a real implementation, this would check a database or cache
    # For now, return a mock response
    return {
        "batch_id": batch_id,
        "status": "completed",
        "progress": 100,
        "total_titles": 10,
        "processed_titles": 10,
        "completed_at": datetime.now().isoformat()
    }

async def process_batch_optimization(
    batch_id: str,
    request: BatchOptimizationRequest,
    ai_service: Any
):
    """Process batch optimization in the background"""
    try:
        # In a real implementation, this would update a database with progress
        logger.info(f"Processing batch {batch_id} with {len(request.titles)} titles")
        
        # Process each title
        for title in request.titles:
            # Add delay to avoid rate limits
            await asyncio.sleep(1)
            
            # Optimize title
            await ai_service.optimize_title(
                original_title=title,
                description=request.description or "Batch optimization",
                category=request.category,
                target_emotion=request.target_emotion,
                content_type=request.content_type
            )
            
            # Update progress in database
            logger.info(f"Processed title: {title}")
        
        # Mark batch as complete
        logger.info(f"Batch {batch_id} processing completed")
        
    except Exception as e:
        logger.error(f"Error processing batch {batch_id}: {str(e)}")
        # Update batch status to failed
