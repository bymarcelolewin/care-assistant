"""
Graph Visualization API endpoint.

This module provides an API endpoint to retrieve the LangGraph structure
as a PNG image for visualization in the frontend.
"""

from fastapi import APIRouter, Response
from app.graph.graph import compile_agent


# ============================================================================
# API Router
# ============================================================================

router = APIRouter()


@router.get("/api/graph")
async def get_graph_visualization():
    """
    Get the LangGraph structure as a PNG image.

    This endpoint:
    1. Compiles the LangGraph agent
    2. Generates a Mermaid diagram visualization
    3. Returns the PNG bytes with proper content type

    Returns:
        Response: PNG image of the graph structure

    Example:
        GET /api/graph
        Returns: PNG image showing the conversation flow graph
    """
    try:
        # Compile the agent
        agent = compile_agent()

        # Generate PNG visualization using Mermaid
        png_bytes = agent.get_graph().draw_mermaid_png()

        # Return as image response
        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={
                "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
            }
        )
    except Exception as e:
        # If visualization fails, return error details
        print(f"Graph visualization error: {str(e)}")
        import traceback
        traceback.print_exc()

        # Return a simple error response
        raise
