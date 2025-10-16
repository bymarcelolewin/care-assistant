"""
Chat API endpoint for web frontend.

This module provides the REST API endpoint for the web interface to interact
with the LangGraph agent. It handles session management, message processing,
and response formatting.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage

from app.graph.graph import compile_agent
from app.api.sessions import (
    create_session,
    get_session,
    update_session
)


# ============================================================================
# Pydantic Models for API Request/Response
# ============================================================================

class ChatRequest(BaseModel):
    """
    Request model for POST /api/chat endpoint.

    Attributes:
        session_id: Optional session identifier. If None, a new session is created.
        message: User's message text
    """
    session_id: Optional[str] = None
    message: str


class TraceEntry(BaseModel):
    """
    Single execution trace entry showing a node's execution.

    Attributes:
        node: Name of the graph node that executed
        timestamp: ISO format timestamp
        action: Description of what the node did
        details: Optional additional details (tool calls, state changes, etc.)
    """
    node: str
    timestamp: str
    action: str
    details: Optional[Dict[str, Any]] = None


class ConversationStateResponse(BaseModel):
    """
    Simplified conversation state for frontend display.

    Attributes:
        user_id: Current user identifier
        user_profile: User's insurance profile data
        tool_results: Results from tool executions in this turn
    """
    user_id: Optional[str] = None
    user_profile: Optional[Dict[str, Any]] = None
    tool_results: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """
    Response model for POST /api/chat endpoint.

    Attributes:
        session_id: Session identifier for this conversation
        response: AI's response message text
        trace: List of execution trace entries showing graph flow
        state: Current conversation state (user profile, tool results, etc.)
        progress_messages: Optional list of friendly progress messages during tool execution
    """
    session_id: str
    response: str
    trace: List[TraceEntry]
    state: ConversationStateResponse
    progress_messages: Optional[List[str]] = None


# ============================================================================
# API Router
# ============================================================================

router = APIRouter()


@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chat messages from the web frontend.

    This endpoint:
    1. Gets or creates a session
    2. Adds the user's message to the conversation state
    3. Invokes the LangGraph agent
    4. Extracts the AI response
    5. Updates the session with new state
    6. Returns the response, trace, and state to the frontend

    Args:
        request: ChatRequest containing session_id and message

    Returns:
        ChatResponse: AI response, execution trace, and conversation state

    Raises:
        HTTPException: 500 if agent execution fails
    """
    try:
        # ====================================================================
        # 1. Session Management
        # ====================================================================
        session_id = request.session_id
        if session_id:
            state = get_session(session_id)
            if state is None:
                # Session expired or invalid, create new one
                session_id = create_session()
                state = get_session(session_id)
        else:
            # First message, create new session
            session_id = create_session()
            state = get_session(session_id)

        # ====================================================================
        # 2. Add user message to state
        # ====================================================================
        state["messages"].append(HumanMessage(content=request.message))

        # Clear first_greeting flag so subsequent messages continue to orchestrate_tools
        if state.get("first_greeting"):
            state["first_greeting"] = False

        # ====================================================================
        # 3. Invoke LangGraph agent (async)
        # ====================================================================
        agent = compile_agent()
        result = await agent.ainvoke(state)

        # ====================================================================
        # 4. Extract AI response from last message
        # ====================================================================
        ai_response = ""
        if result["messages"]:
            last_message = result["messages"][-1]
            if isinstance(last_message, AIMessage):
                ai_response = last_message.content

        # ====================================================================
        # 5. Update session with new state
        # ====================================================================
        update_session(session_id, result)

        # ====================================================================
        # 6. Format response for frontend
        # ====================================================================

        # Convert execution trace to TraceEntry models
        trace_entries = [
            TraceEntry(
                node=entry.get("node", "unknown"),
                timestamp=entry.get("timestamp", ""),
                action=entry.get("action", ""),
                details=entry.get("details")
            )
            for entry in result.get("execution_trace", [])
        ]

        # Build conversation state response
        state_response = ConversationStateResponse(
            user_id=result.get("user_id"),
            user_profile=result.get("user_profile"),
            tool_results=result.get("tool_results", {})
        )

        # Extract progress messages if they exist
        progress_messages = result.get("progress_messages", [])

        return ChatResponse(
            session_id=session_id,
            response=ai_response,
            trace=trace_entries,
            state=state_response,
            progress_messages=progress_messages if progress_messages else None
        )

    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Chat endpoint error: {str(e)}")
        import traceback
        traceback.print_exc()

        # Return user-friendly error message
        raise HTTPException(
            status_code=500,
            detail="Sorry, I encountered an error processing your message. Please try again."
        )
