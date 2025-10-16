"""
Session management for conversation state persistence.

This module provides in-memory session storage to maintain conversation state
across HTTP requests. Each session is identified by a unique session_id (UUID)
and includes the full LangGraph conversation state.
"""

from typing import Dict, Optional
from datetime import datetime, timedelta
from uuid import uuid4


# In-memory session store
# Structure: {session_id: {"state": ConversationState, "last_activity": datetime}}
sessions: Dict[str, Dict] = {}


def create_session() -> str:
    """
    Create a new session with empty state.

    Returns:
        str: New session_id (UUID)
    """
    session_id = str(uuid4())
    sessions[session_id] = {
        "state": {
            "messages": [],
            "user_id": None,
            "user_profile": None,
            "conversation_context": {},
            "tool_results": {},
            "execution_trace": []
        },
        "last_activity": datetime.now()
    }
    return session_id


def get_session(session_id: str) -> Optional[Dict]:
    """
    Retrieve session state by session_id.

    Updates last_activity timestamp to prevent premature cleanup.

    Args:
        session_id: Unique session identifier

    Returns:
        Dict: Session state, or None if session not found
    """
    if session_id in sessions:
        # Update last activity timestamp
        sessions[session_id]["last_activity"] = datetime.now()
        return sessions[session_id]["state"]
    else:
        return None


def update_session(session_id: str, state: Dict) -> None:
    """
    Update session state with new data.

    Args:
        session_id: Unique session identifier
        state: Updated conversation state
    """
    if session_id in sessions:
        sessions[session_id]["state"] = state
        sessions[session_id]["last_activity"] = datetime.now()


def delete_session(session_id: str) -> None:
    """
    Delete a session by session_id.

    Args:
        session_id: Unique session identifier
    """
    if session_id in sessions:
        del sessions[session_id]


def cleanup_sessions(max_inactive_minutes: int = 30) -> int:
    """
    Remove sessions inactive for longer than max_inactive_minutes.

    Should be called periodically (e.g., every 5 minutes) to prevent
    memory buildup from abandoned sessions.

    Args:
        max_inactive_minutes: Maximum allowed inactivity before cleanup (default: 30)

    Returns:
        int: Number of sessions cleaned up
    """
    cutoff = datetime.now() - timedelta(minutes=max_inactive_minutes)
    expired = [
        sid for sid, data in sessions.items()
        if data["last_activity"] < cutoff
    ]

    for sid in expired:
        del sessions[sid]

    return len(expired)


def get_session_count() -> int:
    """
    Get current number of active sessions.

    Returns:
        int: Number of active sessions
    """
    return len(sessions)
