"""FastAPI application entry point for The Great GASPI"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import logging

from .routes import router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="The Great GASPI",
    description="Global Asymmetric Sovereignty & Power Index - Geopolitical analytics platform",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Local React dev
        "http://localhost:5173",      # Vite dev
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "gasapi-backend",
        "version": "0.1.0"
    }


@app.get("/")
async def root():
    """Root endpoint with service info"""
    return {
        "service": "The Great GASPI",
        "version": "0.1.0",
        "description": "Global Asymmetric Sovereignty & Power Index API",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "base_api": "/api/v1",
        "status": "Phase 2 - Backend Development"
    }


# ============================================================================
# INCLUDE ROUTERS
# ============================================================================

app.include_router(router)


# ============================================================================
# CUSTOM OPENAPI SCHEMA
# ============================================================================

def custom_openapi():
    """Customize OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="The Great GASPI API",
        version="0.1.0",
        description="Geopolitical analytics platform for analyzing territorial asymmetry and sovereignty",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def universal_exception_handler(request, exc):
    """Catch-all exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {
        "detail": str(exc),
        "status_code": 500,
        "error_type": type(exc).__name__
    }


# ============================================================================
# STARTUP / SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting The Great GASPI Backend")
    logger.info("Phase 2: Database schema and endpoint scaffolding initialized")
    logger.info("Database integration: PENDING (requires migrations)")
    logger.info("ETL pipeline: PENDING (requires data ingestion)")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down The Great GASPI Backend")


# ============================================================================
# DEVELOPMENT UTILITIES
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
