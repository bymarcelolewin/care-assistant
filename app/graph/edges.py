"""
LangGraph Conditional Edge Functions for CARE Assistant.

This module contains edge functions that determine routing logic in the graph.
Conditional edges examine the state and decide which node to execute next.

In LangGraph, edges connect nodes. Conditional edges add branching logic,
allowing the graph to take different paths based on state values.
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


# Note: The route_after_intent function has been removed as it's no longer used.
# The current architecture uses orchestrate_tools which intelligently selects
# and calls multiple tools using LLM-based decision making, eliminating the need
# for manual intent classification and routing.
