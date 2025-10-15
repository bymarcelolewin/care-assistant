"""
LangGraph State Schema for CARE Assistant.

This module defines the conversation state that flows through all nodes in the graph.
State is the core of LangGraph - it's how data is passed between nodes and persisted
across the conversation.
"""

from typing import TypedDict, List, Optional, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ConversationState(TypedDict):
    """
    State schema for the CARE Assistant conversation graph.

    This TypedDict defines all fields that can exist in the conversation state.
    Each node in the graph receives this state as input and can return updates to it.

    LangGraph automatically merges returned updates into the state, so nodes only
    need to return the fields they want to update, not the entire state.

    Fields:
        messages: List of conversation messages (Human, AI, System, Tool).
                  Uses add_messages reducer to automatically append new messages
                  instead of replacing the entire list.

        user_id: Unique identifier for the current user (e.g., "user_001").
                 Set by the identify_user node after name lookup.

        user_profile: Full user data loaded from user_profiles.json.
                      Contains insurance plan, coverage details, deductible info, etc.

        intent: Classified user intent from classify_intent node.
                Values: "coverage", "benefits", "claims", "general"
                Used by conditional routing to determine which tool to call.

        tool_results: Results from tool calls (coverage_lookup, benefit_verify, claims_status).
                      Stored here so generate_response can access them.
                      Cleared after each turn to avoid stale data.

        conversation_context: Dictionary for storing extracted entities and context.
                             Examples: plan names mentioned, service types discussed, etc.
                             Helps maintain context across multiple turns.

        execution_trace: List of trace entries showing graph execution flow.
                        Each entry contains: node name, timestamp, action, LLM calls, state changes.
                        Used for learning visibility - shows exactly how the graph executes.
    """

    # Message history with automatic appending behavior
    # The add_messages reducer tells LangGraph: when a node returns messages,
    # append them to the existing list instead of replacing it
    messages: Annotated[List[BaseMessage], add_messages]

    # User identification and profile data
    user_id: Optional[str]
    user_profile: Optional[dict]

    # Intent classification for routing
    intent: Optional[str]

    # Tool results from current turn - now supports multiple tools
    # Dictionary mapping tool names to their results
    tool_results: Optional[dict]

    # Flag to track if we need to call more tools
    needs_tool_call: Optional[bool]

    # Context tracking across conversation
    conversation_context: dict

    # Execution trace for learning visibility
    execution_trace: List[dict]
