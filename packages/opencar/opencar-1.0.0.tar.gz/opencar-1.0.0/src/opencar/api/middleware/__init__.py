"""API middleware for OpenCar."""

import time
import uuid
from typing import Callable, Dict, Any, Optional
from datetime import datetime

from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log details."""
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("user-agent", "unknown"),
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                "Request completed",
                request_id=request_id,
                status_code=response.status_code,
                process_time_ms=round(process_time * 1000, 2),
            )
            
            # Add headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                "Request failed",
                request_id=request_id,
                error=str(e),
                process_time_ms=round(process_time * 1000, 2),
            )
            raise


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting metrics."""

    def __init__(self, app):
        super().__init__(app)
        self.metrics = {
            "total_requests": 0,
            "requests_by_method": {},
            "requests_by_status": {},
            "response_times": [],
            "errors": 0,
        }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and collect metrics."""
        start_time = time.time()
        
        # Increment request counter
        self.metrics["total_requests"] += 1
        method = request.method
        self.metrics["requests_by_method"][method] = self.metrics["requests_by_method"].get(method, 0) + 1
        
        try:
            response = await call_next(request)
            
            # Record response metrics
            status_code = response.status_code
            self.metrics["requests_by_status"][status_code] = self.metrics["requests_by_status"].get(status_code, 0) + 1
            
            # Record response time
            response_time = (time.time() - start_time) * 1000
            self.metrics["response_times"].append(response_time)
            
            # Keep only last 1000 response times to prevent memory issues
            if len(self.metrics["response_times"]) > 1000:
                self.metrics["response_times"] = self.metrics["response_times"][-1000:]
            
            return response
            
        except Exception as e:
            self.metrics["errors"] += 1
            raise

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        response_times = self.metrics["response_times"]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        return {
            "total_requests": self.metrics["total_requests"],
            "requests_by_method": self.metrics["requests_by_method"],
            "requests_by_status": self.metrics["requests_by_status"],
            "errors": self.metrics["errors"],
            "average_response_time_ms": round(avg_response_time, 2),
            "timestamp": datetime.utcnow().isoformat(),
        }


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding security headers."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to response."""
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware."""

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.client_requests = {}  # In production, use Redis
        self.window_size = 60  # 1 minute

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check rate limits and process request."""
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old entries
        self._clean_old_entries(current_time)
        
        # Check rate limit
        if client_ip in self.client_requests:
            requests_in_window = [
                req_time for req_time in self.client_requests[client_ip]
                if current_time - req_time < self.window_size
            ]
            
            if len(requests_in_window) >= self.requests_per_minute:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later.",
                    headers={"Retry-After": "60"}
                )
                
            self.client_requests[client_ip].append(current_time)
        else:
            self.client_requests[client_ip] = [current_time]
        
        return await call_next(request)

    def _clean_old_entries(self, current_time: float) -> None:
        """Remove old request timestamps."""
        for client_ip in list(self.client_requests.keys()):
            self.client_requests[client_ip] = [
                req_time for req_time in self.client_requests[client_ip]
                if current_time - req_time < self.window_size
            ]
            
            # Remove empty entries
            if not self.client_requests[client_ip]:
                del self.client_requests[client_ip]


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for handling errors gracefully."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Handle errors and return appropriate responses."""
        try:
            return await call_next(request)
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            # Log unexpected errors
            request_id = getattr(request.state, 'request_id', 'unknown')
            logger.error(
                "Unexpected error",
                request_id=request_id,
                error=str(e),
                error_type=type(e).__name__,
            )
            
            # Return generic error response
            raise HTTPException(
                status_code=500,
                detail="Internal server error occurred"
            )


# Global metrics instance for export
metrics_middleware_instance: Optional[MetricsMiddleware] = None

def get_metrics() -> Dict[str, Any]:
    """Get metrics from the global metrics middleware."""
    if metrics_middleware_instance:
        return metrics_middleware_instance.get_metrics()
    return {"error": "Metrics not available"}


# Export all middleware classes
__all__ = [
    "LoggingMiddleware",
    "MetricsMiddleware", 
    "SecurityHeadersMiddleware",
    "RateLimitMiddleware",
    "ErrorHandlingMiddleware",
    "get_metrics",
] 