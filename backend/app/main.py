"""FastAPI application entry point for The Great GSAPI"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="The Great GSAPI",
    description="Global Sovereignty & Asymmetric Power Index API",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "gsapi-backend"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "The Great GSAPI",
        "version": "0.1.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


# TODO: Add routes for:
# - /api/territories — List disputed territories
# - /api/sovereignty — Get sovereignty scores
# - /api/hydrology — Water sovereignty data
# - /api/sources — Data source attribution
