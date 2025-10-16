"""
LangGraph Graph Construction for CARE Assistant.

This module builds and compiles the conversation graph by:
1. Creating a StateGraph with the ConversationState schema
2. Adding all nodes (identify_user, orchestrate_tools, generate_response)
3. Connecting nodes with edges (including conditional routing)
4. Compiling the graph into an executable agent

The compiled graph can then be invoked with an initial state to run conversations.
"""

from langgraph.graph import StateGraph, END
from .state import ConversationState
from .nodes import (
    identify_user,
    orchestrate_tools,
    generate_response
)
from .edges import should_continue_after_identify


def create_graph() -> StateGraph:
    """
    Create and configure the LangGraph state graph for CARE Assistant.

    This function builds the graph structure by:
    1. Creating a StateGraph with ConversationState schema
    2. Adding all node functions
    3. Connecting nodes with edges (normal and conditional)
    4. Defining the entry point (START)

    The graph structure:
        START → identify_user → orchestrate_tools → generate_response → END

    The orchestrate_tools node uses LLM with tool binding to intelligently
    determine which tools to call (coverage_lookup, benefit_verify, claims_status).
    It can call multiple tools in one turn to handle complex multi-intent questions.

    This demonstrates:
    - StateGraph creation with type schema
    - Adding nodes with descriptive names
    - Normal and conditional edges
    - LLM-based tool orchestration for multi-tool/multi-intent scenarios
    - Eliminating manual intent classification (LLM handles it automatically)
    - Graph entry and exit points

    Returns:
        StateGraph: Configured (but not compiled) graph

    Example:
        >>> graph = create_graph()
        >>> compiled = graph.compile()
        >>> result = compiled.invoke({"messages": [], "execution_trace": []})
    """
    # Create the state graph with ConversationState schema
    # This tells LangGraph what fields exist in state and how to merge updates
    workflow = StateGraph(ConversationState)

    # ========================================================================
    # Add Nodes
    # ========================================================================
    # Each node is added with a name (string) and the async function to execute
    # The name is used when defining edges to connect nodes

    # User identification node (first step)
    workflow.add_node("identify_user", identify_user)

    # Tool orchestration node (LLM intelligently calls one or more tools based on question)
    # This replaces manual intent classification - the LLM handles multi-intent questions
    workflow.add_node("orchestrate_tools", orchestrate_tools)

    # Response generation node (synthesizes tool results into natural language)
    workflow.add_node("generate_response", generate_response)

    # ========================================================================
    # Add Edges
    # ========================================================================

    # Set the entry point: START always goes to identify_user first
    workflow.set_entry_point("identify_user")

    # Conditional edge: check if user is identified before continuing
    # If user is not identified yet (waiting for name), stop and wait for input
    # If identified, go directly to orchestrate_tools (no manual intent classification needed)
    workflow.add_conditional_edges(
        "identify_user",
        should_continue_after_identify,
        {
            "orchestrate_tools": "orchestrate_tools",
            "__end__": END
        }
    )

    # After orchestrate_tools completes, go to generate_response
    workflow.add_edge("orchestrate_tools", "generate_response")

    # generate_response is the final node, so it goes to END
    workflow.add_edge("generate_response", END)

    return workflow


def compile_agent():
    """
    Create and compile the CARE Assistant agent.

    This is a convenience function that:
    1. Creates the graph
    2. Compiles it into an executable agent
    3. Returns the compiled agent ready for use

    Compiling the graph:
    - Validates the graph structure (all referenced nodes exist, no cycles, etc.)
    - Optimizes the execution plan
    - Returns a runnable agent that can be invoked

    Returns:
        CompiledGraph: The compiled agent ready to run conversations

    Example:
        >>> agent = compile_agent()
        >>> # Run a single turn
        >>> result = agent.invoke({
        ...     "messages": [HumanMessage("Hello")],
        ...     "execution_trace": [],
        ...     "conversation_context": {}
        ... })
        >>> print(result["messages"][-1].content)
        Hello! I'm your CARE insurance assistant. What's your name?

    Note:
        The compiled agent is stateless between invocations.
        For multi-turn conversations, you need to pass the previous state
        back in on the next invocation to maintain conversation context.
    """
    graph = create_graph()
    return graph.compile()


# ============================================================================
# Module-level compiled agent (optional convenience)
# ============================================================================

# You can uncomment this to have a module-level agent instance
# that's compiled once when the module is imported:
#
# agent = compile_agent()
#
# Then in other modules:
# from app.graph.graph import agent
# result = agent.invoke(...)
