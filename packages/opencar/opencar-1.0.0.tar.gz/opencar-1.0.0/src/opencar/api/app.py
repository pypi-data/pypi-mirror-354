"""FastAPI application for OpenCar."""

from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from opencar import __version__
from opencar.config.settings import get_settings
from opencar.api.routes import main_router
from opencar.api.middleware import (
    LoggingMiddleware,
    MetricsMiddleware,
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    ErrorHandlingMiddleware,
    metrics_middleware_instance
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    settings = get_settings()
    app.state.settings = settings

    # Initialize models
    await _initialize_models()

    yield

    # Shutdown
    await _cleanup_resources()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="OpenCar API",
        description="Advanced Autonomous Vehicle Perception System",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Add middleware (order matters - first added is outermost)
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(LoggingMiddleware)
    
    # Add metrics middleware and store reference
    metrics_middleware = MetricsMiddleware(app)
    app.add_middleware(MetricsMiddleware)
    
    # Store global reference for metrics endpoint
    import opencar.api.middleware as middleware_module
    middleware_module.metrics_middleware_instance = metrics_middleware
    
    if not settings.debug:
        app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
    
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"] if settings.debug else ["localhost", "*.opencar.ai", "testserver"],
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add routes
    app.include_router(main_router, prefix="/api/v1")
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "version": __version__}

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "name": "OpenCar API",
            "version": __version__,
            "status": "operational",
            "documentation": "/docs",
        }

    return app


async def _initialize_models() -> None:
    """Initialize ML models."""
    # Mock implementation
    pass


async def _cleanup_resources() -> None:
    """Cleanup resources on shutdown."""
    # Mock implementation
    pass


app = create_app() 