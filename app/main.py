"""
Main application entry point for CARE Assistant - Coverage Analysis and Recommendation Engine.

This FastAPI application demonstrates LangGraph concepts including:
- State management across conversation turns
- Tool integration for querying insurance data
- Intelligent tool orchestration using LLM-based multi-tool coordination
- Execution trace visibility for learning

Run with: uvicorn app.main:app --reload
"""

import asyncio
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

# Load environment variables from .env file
# This must happen before any LangChain/LangGraph imports
load_dotenv()

# Import data loader
from app.data.loader import initialize_data

# Import API routers
from app.api.chat import router as chat_router
from app.api.graph import router as graph_router
from app.api.sessions import cleanup_sessions

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

# Include API routers
app.include_router(chat_router)
app.include_router(graph_router)

# Serve static files from Next.js build
FRONTEND_BUILD_DIR = Path(__file__).parent.parent / "frontend" / "out"

# Mount static assets (_next folder) first with longer paths
if (FRONTEND_BUILD_DIR / "_next").exists():
    app.mount("/_next", StaticFiles(directory=str(FRONTEND_BUILD_DIR / "_next")), name="next-static")


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


# Background task for session cleanup
cleanup_task = None


async def periodic_session_cleanup():
    """
    Background task that runs every 5 minutes to clean up expired sessions.
    """
    while True:
        await asyncio.sleep(300)  # 5 minutes
        cleaned = cleanup_sessions(max_inactive_minutes=30)
        if cleaned > 0:
            print(f"🧹 Cleaned up {cleaned} expired session(s)")


# Application lifecycle events
@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.
    Loads mock data into memory for use by the agent.
    Starts the periodic session cleanup task.
    """
    global cleanup_task

    print("🚀 Starting CARE Assistant - Coverage Analysis and Recommendation Engine...")
    print("📚 Version 0.8.0 - LangSmith Observability")

    # Check if LangSmith tracing is enabled
    langsmith_enabled = os.getenv("LANGCHAIN_TRACING_V2", "").lower() == "true"
    
    if langsmith_enabled:
        project_name = os.getenv("LANGCHAIN_PROJECT", "default")
        print("✅ LangSmith tracing enabled")
        print(f"📊 Project: {project_name}")
        print(f"🌐 Dashboard: https://smith.langchain.com/")
    else:
        print("⚪ LangSmith tracing disabled (optional feature)")
        print("💡 To enable: Set LANGCHAIN_TRACING_V2=true in .env file")

    # Load mock data into memory
    initialize_data()

    # Start periodic session cleanup task
    cleanup_task = asyncio.create_task(periodic_session_cleanup())
    print("🧹 Session cleanup task started (runs every 5 minutes)")

    print("✅ Application startup complete!")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application shuts down.
    Cancels the cleanup task.
    """
    global cleanup_task

    print("👋 Shutting down CARE Assistant...")

    # Cancel cleanup task
    if cleanup_task:
        cleanup_task.cancel()
        try:
            await cleanup_task
        except asyncio.CancelledError:
            print("🧹 Session cleanup task cancelled")

    print("✅ Shutdown complete!")


# Catch-all route to serve index.html for SPA routing
# This must be AFTER all API routes
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """
    Serve the Next.js static frontend.

    For any route that doesn't match an API endpoint, try to serve the corresponding
    .html file from the Next.js export. Falls back to index.html for client-side routing.
    """
    # Try to serve the specific HTML file for this route (Next.js static export)
    if full_path and not full_path.startswith("_next"):
        html_file = FRONTEND_BUILD_DIR / f"{full_path}.html"
        if html_file.exists():
            return FileResponse(html_file)

    # Check if the frontend build exists
    index_file = FRONTEND_BUILD_DIR / "index.html"

    if index_file.exists():
        return FileResponse(index_file)
    else:
        return {
            "error": "Frontend not built",
            "message": "Please run 'cd frontend && npm run build' to build the frontend"
        }


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
