"""Pydantic schemas for OpenCar API."""

from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class DetectionStatus(str, Enum):
    """Detection status enumeration."""
    SUCCESS = "success"
    FAILED = "failed"
    PROCESSING = "processing"


class ObjectClass(str, Enum):
    """Object class enumeration."""
    PERSON = "person"
    CAR = "car"
    TRUCK = "truck"
    BICYCLE = "bicycle"
    MOTORCYCLE = "motorcycle"
    TRAFFIC_LIGHT = "traffic_light"
    STOP_SIGN = "stop_sign"
    UNKNOWN = "unknown"


class BoundingBox(BaseModel):
    """Bounding box for detected object."""
    model_config = {"protected_namespaces": ()}
    
    x1: float = Field(..., description="Left coordinate")
    y1: float = Field(..., description="Top coordinate")
    x2: float = Field(..., description="Right coordinate")
    y2: float = Field(..., description="Bottom coordinate")
    
    @field_validator('x1', 'x2', 'y1', 'y2')
    @classmethod
    def validate_coordinates(cls, v):
        if v < 0:
            raise ValueError("Coordinates must be non-negative")
        return v

    @field_validator('x2')
    @classmethod
    def validate_x2(cls, v, info):
        if 'x1' in info.data and v <= info.data['x1']:
            raise ValueError("x2 must be greater than x1")
        return v

    @field_validator('y2')
    @classmethod
    def validate_y2(cls, v, info):
        if 'y1' in info.data and v <= info.data['y1']:
            raise ValueError("y2 must be greater than y1")
        return v


class Detection(BaseModel):
    """Single object detection."""
    model_config = {"protected_namespaces": ()}
    
    class_name: str = Field(..., description="Detected object class")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence")
    bbox: BoundingBox = Field(..., description="Bounding box coordinates")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Additional attributes")


class DetectionRequest(BaseModel):
    """Request for object detection."""
    model_config = {"protected_namespaces": ()}
    
    confidence_threshold: float = Field(0.5, ge=0.0, le=1.0, description="Minimum confidence threshold")
    max_detections: int = Field(100, ge=1, le=1000, description="Maximum number of detections")
    classes: Optional[List[str]] = Field(None, description="Filter by specific classes")


class DetectionResponse(BaseModel):
    """Response from object detection."""
    model_config = {"protected_namespaces": ()}
    
    request_id: str = Field(..., description="Unique request identifier")
    timestamp: datetime = Field(..., description="Processing timestamp")
    status: DetectionStatus = Field(DetectionStatus.SUCCESS, description="Detection status")
    detections: List[Detection] = Field(..., description="List of detected objects")
    image_info: Dict[str, Any] = Field(..., description="Image metadata")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")


class AnalysisType(str, Enum):
    """Analysis type enumeration."""
    COMPREHENSIVE = "comprehensive"
    TRAFFIC = "traffic"
    SAFETY = "safety"
    WEATHER = "weather"
    NAVIGATION = "navigation"


class AnalysisRequest(BaseModel):
    """Request for scene analysis."""
    model_config = {"protected_namespaces": ()}
    
    analysis_type: AnalysisType = Field(AnalysisType.COMPREHENSIVE, description="Type of analysis")
    include_detections: bool = Field(True, description="Include object detections")
    language: str = Field("en", description="Response language")


class AnalysisResponse(BaseModel):
    """Response from scene analysis."""
    model_config = {"protected_namespaces": ()}
    
    request_id: str = Field(..., description="Unique request identifier")
    timestamp: datetime = Field(..., description="Processing timestamp")
    analysis_type: AnalysisType = Field(..., description="Type of analysis performed")
    analysis: Dict[str, Any] = Field(..., description="Analysis results")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Analysis confidence")
    image_info: Dict[str, Any] = Field(..., description="Image metadata")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")


class HealthStatus(str, Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class HealthCheck(BaseModel):
    """Health check response."""
    model_config = {"protected_namespaces": ()}
    
    status: HealthStatus = Field(..., description="Overall health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    checks: Dict[str, bool] = Field(..., description="Individual component checks")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional health details")


class SystemMetrics(BaseModel):
    """System metrics response."""
    model_config = {"protected_namespaces": ()}
    
    timestamp: datetime = Field(..., description="Metrics timestamp")
    cpu_usage: float = Field(..., ge=0.0, le=100.0, description="CPU usage percentage")
    memory_usage: float = Field(..., ge=0.0, le=100.0, description="Memory usage percentage")
    disk_usage: float = Field(..., ge=0.0, le=100.0, description="Disk usage percentage")
    gpu_usage: Optional[float] = Field(None, ge=0.0, le=100.0, description="GPU usage percentage")
    total_requests: int = Field(..., ge=0, description="Total requests processed")
    active_connections: int = Field(..., ge=0, description="Active connections")
    model_status: str = Field(..., description="ML model status")


class ConfigResponse(BaseModel):
    """Configuration response."""
    model_config = {"protected_namespaces": ()}
    
    debug: bool = Field(..., description="Debug mode enabled")
    log_level: str = Field(..., description="Current log level")
    api_host: str = Field(..., description="API host")
    api_port: int = Field(..., description="API port")
    device: str = Field(..., description="Computing device")
    batch_size: int = Field(..., description="Model batch size")
    model_path: str = Field(..., description="Model path")
    openai_model: str = Field(..., description="OpenAI model name")


class ErrorResponse(BaseModel):
    """Error response."""
    model_config = {"protected_namespaces": ()}
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    request_id: Optional[str] = Field(None, description="Request identifier")
    timestamp: datetime = Field(..., description="Error timestamp")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class BatchDetectionRequest(BaseModel):
    """Request for batch object detection."""
    model_config = {"protected_namespaces": ()}
    
    confidence_threshold: float = Field(0.5, ge=0.0, le=1.0, description="Minimum confidence threshold")
    max_detections: int = Field(100, ge=1, le=1000, description="Maximum number of detections per image")
    classes: Optional[List[str]] = Field(None, description="Filter by specific classes")
    return_images: bool = Field(False, description="Return processed images")


class BatchDetectionResponse(BaseModel):
    """Response from batch object detection."""
    model_config = {"protected_namespaces": ()}
    
    request_id: str = Field(..., description="Unique request identifier")
    timestamp: datetime = Field(..., description="Processing timestamp")
    status: DetectionStatus = Field(..., description="Overall processing status")
    results: List[DetectionResponse] = Field(..., description="Detection results for each image")
    total_processed: int = Field(..., description="Total images processed")
    processing_time_ms: float = Field(..., description="Total processing time in milliseconds")


class ModelStatus(str, Enum):
    """Model status enumeration."""
    LOADED = "loaded"
    LOADING = "loading"
    UNLOADED = "unloaded"
    ERROR = "error"


class ModelInfo(BaseModel):
    """Model information."""
    model_config = {"protected_namespaces": ()}
    
    name: str = Field(..., description="Model name")
    version: str = Field(..., description="Model version")
    status: ModelStatus = Field(..., description="Model status")
    size_mb: float = Field(..., description="Model size in MB")
    load_time_ms: float = Field(..., description="Model load time in milliseconds")
    last_updated: datetime = Field(..., description="Last update timestamp")


class ModelsResponse(BaseModel):
    """Models status response."""
    model_config = {"protected_namespaces": ()}
    
    timestamp: datetime = Field(..., description="Response timestamp")
    models: List[ModelInfo] = Field(..., description="List of models")
    total_models: int = Field(..., description="Total number of models")


class PerformanceMetrics(BaseModel):
    """Performance metrics for inference."""
    model_config = {"protected_namespaces": ()}
    
    average_inference_time_ms: float = Field(..., description="Average inference time")
    throughput_fps: float = Field(..., description="Throughput in frames per second")
    total_inferences: int = Field(..., description="Total number of inferences")
    p95_latency_ms: float = Field(..., description="95th percentile latency")
    p99_latency_ms: float = Field(..., description="99th percentile latency")


class StreamingResponse(BaseModel):
    """Streaming response chunk."""
    model_config = {"protected_namespaces": ()}
    
    chunk_id: str = Field(..., description="Chunk identifier")
    content: str = Field(..., description="Chunk content")
    is_final: bool = Field(False, description="Whether this is the final chunk")
    timestamp: datetime = Field(..., description="Chunk timestamp")


# Export all schemas
__all__ = [
    "DetectionStatus",
    "ObjectClass",
    "BoundingBox",
    "Detection",
    "DetectionRequest",
    "DetectionResponse",
    "AnalysisType",
    "AnalysisRequest",
    "AnalysisResponse",
    "HealthStatus",
    "HealthCheck",
    "SystemMetrics",
    "ConfigResponse",
    "ErrorResponse",
    "BatchDetectionRequest",
    "BatchDetectionResponse",
    "ModelStatus",
    "ModelInfo",
    "ModelsResponse",
    "PerformanceMetrics",
    "StreamingResponse",
] 