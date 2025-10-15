# LangGraph Agent Architecture

This directory contains the core LangGraph agent implementation for the CARE Assistant.

## Overview

The agent is built using LangGraph, a framework for building stateful, multi-actor applications with LLMs. The agent follows a graph-based architecture where nodes represent operations (LLM calls, tool invocations, data processing) and edges define the flow between operations.

## Graph Flow

```
START → identify_user → orchestrate_tools → generate_response → END
              ↓                   ↓
         (conditional)      (calls multiple tools
          based on              as needed)
          user_id)
```

### Key Architectural Decision: LLM-Based Tool Orchestration

Instead of using manual intent classification and conditional routing to tools, this implementation uses an **intelligent orchestrator** that:

1. Analyzes the user's question using an LLM
2. Determines which tools are needed (can be multiple!)
3. Calls all necessary tools
4. Returns aggregated results

This approach handles **multi-intent questions** naturally. For example:
> "What plan do I have, how long have I been a member, what does it cover, and do I have outstanding claims?"

The orchestrator automatically identifies this needs:
- `coverage_lookup` (for plan info and member date)
- `benefit_verify` (for coverage details)
- `claims_status` (for outstanding claims)

## Files

### `state.py`
Defines the conversation state schema (`ConversationState`) that flows through all nodes.

**Key Fields:**
- `messages`: Conversation history (uses `add_messages` reducer)
- `user_id`: Identified user
- `user_profile`: Full user data from JSON
- `tool_results`: Results from tool calls (dict mapping tool_name → result)
- `execution_trace`: Detailed trace of graph execution for debugging/learning

### `nodes.py`
Contains all node implementations. Each node is an async function that:
1. Receives current state
2. Performs an operation (LLM call, tool call, data lookup)
3. Returns state updates

**Nodes:**
- `identify_user`: Conversational name-based user lookup
- `orchestrate_tools`: LLM-based multi-tool coordinator (replaces manual intent classification)
- `generate_response`: Synthesizes tool results into natural language response

**Legacy Nodes (kept for reference but not used in main flow):**
- `classify_intent`: Manual intent classification
- `coverage_lookup_node`, `benefit_verify_node`, `claims_status_node`: Single-tool nodes

### `edges.py`
Conditional edge functions that determine routing between nodes.

**Edge Functions:**
- `should_continue_after_identify`: Checks if user is identified before proceeding
- `route_after_intent`: (Legacy) Routes based on classified intent

### `graph.py`
Constructs and compiles the LangGraph agent.

**Key Functions:**
- `create_graph()`: Builds the StateGraph with all nodes and edges
- `compile_agent()`: Compiles the graph into an executable agent

## How It Works

### 1. User Identification
The agent starts by identifying the user conversationally:
- Asks "What's your name?"
- Extracts name from response
- Looks up user in `user_profiles.json` by name field
- Loads full profile into state

### 2. Tool Orchestration
The orchestrator uses a text-based approach (works with Ollama models):
- Sends user's question to LLM with list of available tools
- LLM responds with tool names needed (one per line)
- Parses response and executes each tool
- Aggregates all results into `tool_results` dict

Example:
```python
User: "What plan do I have and do I have pending claims?"

LLM Response:
coverage_lookup
claims_status

Orchestrator executes both tools and stores:
tool_results = {
    "coverage_lookup": {...plan data...},
    "claims_status": {...claims data...}
}
```

### 3. Response Generation
The final node:
- Receives user's question + all tool results
- Uses LLM to synthesize natural language response
- Includes user profile data for context
- Returns conversational answer

## Extending the Agent

### Adding a New Tool

1. **Create the tool** in `app/tools/your_tool.py`:
```python
from langchain_core.tools import tool
from typing import Dict, Any

@tool
def your_tool(user_id: str, param: str) -> Dict[str, Any]:
    """
    Description of what your tool does.

    Args:
        user_id: The user's ID
        param: Some parameter

    Returns:
        Dict with 'status' and 'data' keys
    """
    # Your implementation
    return {"status": "success", "data": {...}}
```

2. **Import the tool** in `app/graph/nodes.py`:
```python
from app.tools import your_tool
```

3. **Add to orchestrator** in `orchestrate_tools` node:
   - Add tool description to the prompt (line ~370)
   - Add tool execution logic (line ~445)

4. **That's it!** The LLM orchestrator will automatically use your tool when appropriate.

### Adding a New Node

1. **Define the node function** in `nodes.py`:
```python
async def your_node(state: ConversationState) -> Dict[str, Any]:
    """Node description."""
    # Your logic here
    return {
        "field_to_update": new_value,
        "execution_trace": updated_trace
    }
```

2. **Add to graph** in `graph.py`:
```python
workflow.add_node("your_node", your_node)
```

3. **Connect with edges**:
```python
workflow.add_edge("previous_node", "your_node")
workflow.add_edge("your_node", "next_node")
```

### Modifying the Flow

To change the graph structure, edit `create_graph()` in `graph.py`:

```python
# Add conditional routing
workflow.add_conditional_edges(
    "source_node",
    your_routing_function,
    {
        "option_a": "node_a",
        "option_b": "node_b"
    }
)
```

## Execution Trace

Every node appends entries to `execution_trace` showing:
- Node name
- Timestamp
- Action description
- LLM calls, tool invocations, state changes

This is invaluable for:
- **Learning**: See exactly how the graph executes
- **Debugging**: Identify where things go wrong
- **Optimization**: Find bottlenecks

View traces in the CLI with the `trace` command after each turn.

## State Management

LangGraph automatically merges state updates:
- Nodes only return fields they want to update
- `messages` field uses `add_messages` reducer (automatic appending)
- Other fields are replaced with new values

Example:
```python
# Node returns this
return {
    "user_id": "user_001",
    "messages": [AIMessage("Hello!")]
}

# LangGraph merges with existing state:
# - user_id is replaced
# - messages is appended (due to add_messages reducer)
# - other fields remain unchanged
```

## Best Practices

1. **Always add trace entries** - They're crucial for understanding execution
2. **Use async/await** - All LLM calls should use `ainvoke()`
3. **Handle errors gracefully** - Wrap LLM/tool calls in try/except
4. **Document everything** - Future you will thank present you
5. **Test incrementally** - Use the CLI to test each change

## Testing

Run the interactive CLI:
```bash
python tests/test_agent.py
```

Commands:
- `trace` - Show last turn's execution trace
- `trace full` - Show full trace from conversation start
- `state` - Display current state summary
- `clear` - Start fresh conversation
- `quit` - Exit

## Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Tools](https://python.langchain.com/docs/modules/agents/tools/)
- [Ollama Integration](https://python.langchain.com/docs/integrations/llms/ollama)
