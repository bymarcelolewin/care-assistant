"""
Main application entry point for CARE Assistant - Coverage Analysis and Recommendation Engine.

This FastAPI application demonstrates LangGraph concepts including:
- State management across conversation turns
- Tool integration for querying insurance data
- Conditional routing based on user intent
- Execution trace visibility for learning

Run with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import data loader
from app.data.loader import initialize_data

# Initialize FastAPI application
app = FastAPI(
    title="CARE Assistant - Coverage Analysis and Recommendation Engine",
    description="A learning-focused application demonstrating LangGraph concepts",
    version="0.1.0"
)

# Configure CORS for local development
# This allows the frontend (served from the same origin) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - provides basic API information.
    """
    return {
        "message": "CARE Assistant- Coverage Analysis and Recommendation Engine API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint - verifies the server is running.

    Returns:
        dict: Health status of the application
    """
    return {
        "status": "healthy",
        "service": "care-assistant-api"
    }


# Application lifecycle events
@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.
    Loads mock data into memory for use by the agent.
    """
    print("🚀 Starting CARE Assistant - Coverage Analysis and Recommendation Engine...")
    print("📚 Version 0.1.0 - Environment & Foundation")

    # Load mock data into memory
    initialize_data()
    print("✅ Application startup complete!")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application shuts down.
    """
    print("👋 Shutting down CARE Assistant...")


if __name__ == "__main__":
    import uvicorn

    # Run the application
    # --reload enables auto-restart on code changes (development only)
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
