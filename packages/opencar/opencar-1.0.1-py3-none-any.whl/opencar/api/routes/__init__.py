"""API routes for OpenCar."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime
import uuid

from opencar.config.settings import get_settings
from opencar.perception.models.detector import ObjectDetector
from opencar.integrations.openai_client import OpenAIClient

# Initialize routers
perception_router = APIRouter(prefix="/perception", tags=["perception"])
health_router = APIRouter(prefix="/health", tags=["health"])
admin_router = APIRouter(prefix="/admin", tags=["admin"])

# Global state for initialized models
_detector: Optional[ObjectDetector] = None
_openai_client: Optional[OpenAIClient] = None


async def get_detector() -> ObjectDetector:
    """Get initialized object detector."""
    global _detector
    if _detector is None:
        _detector = ObjectDetector()
        await _detector.initialize()
    return _detector


async def get_openai_client() -> OpenAIClient:
    """Get initialized OpenAI client."""
    global _openai_client
    if _openai_client is None:
        settings = get_settings()
        _openai_client = OpenAIClient(api_key="test-key", model=settings.openai_model)
    return _openai_client


@perception_router.post("/detect")
async def detect_objects(
    file: UploadFile = File(...),
    confidence_threshold: float = 0.5,
    detector: ObjectDetector = Depends(get_detector)
) -> Dict[str, Any]:
    """Detect objects in uploaded image."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Perform detection
        detections = await detector.detect(image_data, confidence_threshold)
        
        return {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "detections": detections,
            "image_info": {
                "filename": file.filename,
                "size": len(image_data),
                "content_type": file.content_type
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Detection failed: {str(e)}"
        )


@perception_router.post("/analyze")
async def analyze_scene(
    file: UploadFile = File(...),
    analysis_type: str = "comprehensive",
    openai_client: OpenAIClient = Depends(get_openai_client)
) -> Dict[str, Any]:
    """Analyze scene using AI."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        image_data = await file.read()
        
        # Perform AI analysis
        analysis = await openai_client.analyze_image(image_data, analysis_type)
        
        return {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "analysis": analysis,
            "analysis_type": analysis_type,
            "image_info": {
                "filename": file.filename,
                "size": len(image_data),
                "content_type": file.content_type
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@health_router.get("/live")
async def liveness_check() -> Dict[str, Any]:
    """Liveness probe for Kubernetes."""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }


@health_router.get("/ready")
async def readiness_check(
    detector: ObjectDetector = Depends(get_detector)
) -> Dict[str, Any]:
    """Readiness probe for Kubernetes."""
    try:
        # Check if models are loaded
        is_ready = await detector.health_check()
        
        return {
            "status": "ready" if is_ready else "not_ready",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                "detector": is_ready
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )


@health_router.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get application metrics."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": {
            "total_requests": 0,  # Would be tracked in production
            "active_connections": 0,
            "model_status": "loaded",
            "memory_usage": "low",
            "cpu_usage": "normal"
        }
    }


@admin_router.post("/models/reload")
async def reload_models() -> Dict[str, Any]:
    """Reload ML models."""
    global _detector
    try:
        if _detector:
            await _detector.reload()
        
        return {
            "status": "success",
            "message": "Models reloaded successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reload models: {str(e)}"
        )


@admin_router.get("/config")
async def get_config() -> Dict[str, Any]:
    """Get current configuration."""
    settings = get_settings()
    return {
        "debug": settings.debug,
        "log_level": settings.log_level,
        "api_host": settings.api_host,
        "api_port": settings.api_port,
        "device": settings.device,
        "batch_size": settings.batch_size,
        "model_path": str(settings.model_path),
        "openai_model": settings.openai_model
    }


# Main router that includes all sub-routers
main_router = APIRouter()
main_router.include_router(perception_router)
main_router.include_router(health_router)
main_router.include_router(admin_router) 