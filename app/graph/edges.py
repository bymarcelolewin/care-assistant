"""
LangGraph Conditional Edge Functions for CARE Assistant.

This module contains edge functions that determine routing logic in the graph.
Conditional edges examine the state and decide which node to execute next.

In LangGraph, edges connect nodes. Conditional edges add branching logic,
allowing the graph to take different paths based on state values (like intent).
"""

from typing import Literal
from langgraph.graph import END
from .state import ConversationState


def should_continue_after_identify(state: ConversationState) -> Literal["orchestrate_tools", "__end__"]:
    """
    Conditional edge to check if user is identified before continuing.

    This prevents the graph from continuing to orchestrate_tools when we're
    still waiting for the user to provide their name, OR when we just showed
    the first greeting and want to let the user ask a question.

    Args:
        state: Current conversation state

    Returns:
        str: "orchestrate_tools" if user is identified and not first greeting,
             END if waiting for name or showing first greeting
    """
    # If this is the first greeting after identification, stop and wait for user question
    if state.get("first_greeting"):
        return "__end__"

    # If user is identified (and not first greeting), continue to orchestrate_tools
    if state.get("user_id"):
        return "orchestrate_tools"

    # If no user_id and we have messages, we're waiting for user response
    # Return END to stop execution and wait for user input
    return "__end__"


def route_after_intent(state: ConversationState) -> Literal["coverage_lookup", "benefit_verify", "claims_status", "generate_response"]:
    """
    Conditional edge function that routes based on classified intent.

    This function is called after the classify_intent node completes.
    It examines the 'intent' field in state and returns the name of the next
    node to execute.

    This demonstrates LangGraph's conditional routing:
    - Read state to make routing decisions
    - Return a string matching a node name
    - Different intents lead to different execution paths

    Routing Logic:
        - "coverage" → coverage_lookup_node (query user's coverage details)
        - "benefits" → benefit_verify_node (check specific service coverage)
        - "claims" → claims_status_node (retrieve claims history)
        - "general" → generate_response (skip tools, respond directly)

    Args:
        state: Current conversation state with classified intent

    Returns:
        str: Name of the next node to execute
            - "coverage_lookup" for coverage questions
            - "benefit_verify" for benefit verification questions
            - "claims_status" for claims-related questions
            - "generate_response" for general conversation

    Example:
        >>> state = {"intent": "coverage", ...}
        >>> next_node = route_after_intent(state)
        >>> print(next_node)
        coverage_lookup

    Note:
        The return type uses Literal to help with type checking and ensure
        we only return valid node names. This is optional but recommended.
    """
    intent = state.get("intent", "general")

    # Route based on intent classification
    if intent == "coverage":
        return "coverage_lookup"
    elif intent == "benefits":
        return "benefit_verify"
    elif intent == "claims":
        return "claims_status"
    else:
        # Default to generate_response for general conversation
        # This includes greetings, unclear questions, or off-topic messages
        return "generate_response"
