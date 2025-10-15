# Version Design Document: v0.2.0 - Core Agent
Technical implementation and design guide for the upcoming version.

## 1. Features Summary
_Overview of features included in this version._

This version builds the core LangGraph agent that powers the CARE Assistant. It includes:

1. **LangGraph State Schema** - Define ConversationState with messages, user context, tool results, and execution trace
2. **Coverage Lookup Tool** - Query user's coverage details from mock data
3. **Benefit Verification Tool** - Check if specific services are covered
4. **Claims Status Tool** - Retrieve claims history and status
5. **Identify User Node** - Identifies or confirms user identity
6. **Classify Intent Node** - Determines user's intent using LLM
7. **Route to Tool Node** - Routes to appropriate tool based on intent
8. **Generate Response Node** - Generates conversational response using LLM
9. **Connect Graph Edges** - Define edges connecting nodes with conditional routing
10. **Ollama Integration** - Integrate LangChain's Ollama LLM for node operations
11. **Basic Conversation Test** - Test agent with simple conversation flow in CLI

**Success Criteria:**
- Agent successfully maintains state across multiple conversation turns
- Tools are called correctly based on user intent
- Conditional routing works (different questions trigger different execution paths)
- Execution trace captures all node transitions
- LLM generates contextually appropriate responses

## 2. Technical Architecture Overview
_High-level technical structure that supports all features in this version._

### Core Components

**LangGraph State Management:**
- `ConversationState` (TypedDict or Pydantic model) containing:
  - `messages: List[BaseMessage]` - Conversation history
  - `user_id: Optional[str]` - Current user identifier
  - `user_profile: Optional[dict]` - Full user data from mock files
  - `conversation_context: dict` - Extracted entities (plan names, service types, etc.)
  - `tool_results: dict` - Results from tool calls in current turn
  - `execution_trace: List[dict]` - Node transitions for visualization

**Tools Architecture:**
- All tools defined as callable functions with `@tool` decorator
- Tools receive user_id and query parameters
- Tools use `app.data.loader` functions to query mock data
- Each tool returns structured dict with results and metadata

**Graph Structure:**
```
START → identify_user → classify_intent → [conditional routing]
                                          ↓
                          ┌───────────────┼───────────────┐
                          ↓               ↓               ↓
                    coverage_lookup  benefit_verify  claims_status
                          ↓               ↓               ↓
                          └───────────────┼───────────────┘
                                          ↓
                                  generate_response → END
```

**Node Explanations:**

| Node | Description |
|------|-------------|
| **START** | LangGraph's entry point. The graph begins execution here and immediately transitions to the first node. No logic executes at START - it's just the starting marker. |
| **identify_user** | Checks if `user_id` exists in the conversation state. If not, this node either prompts the user to identify themselves or defaults to a test user. Once identified, it loads the full user profile from mock data and adds it to state. This ensures all subsequent nodes have access to user-specific insurance information. |
| **classify_intent** | Uses the LLM (Ollama) to analyze the user's latest message and determine their intent. This node examines the message content and classifies it into one of several categories: "coverage" (asking about what's covered), "benefits" (asking about specific benefit details), "claims" (asking about claim status), or "general" (casual conversation). The classified intent is stored in state and used by the conditional edge to route to the appropriate tool node. |
| **[conditional routing]** | This is an **edge function**, not a node. After `classify_intent`, this conditional edge examines the intent stored in state and decides which path to take next. If intent is "coverage", route to `coverage_lookup`. If "benefits", route to `benefit_verify`. If "claims", route to `claims_status`. If "general" (no tool needed), skip directly to `generate_response`. |
| **coverage_lookup** | A tool-calling node that queries the user's coverage details from mock data. It uses the user_id from state and any relevant context from the user's message (e.g., "What's covered for physical therapy?"). It calls the coverage lookup tool, receives structured data about the user's plan, and stores the results in `state["tool_results"]` for use by the response generator. |
| **benefit_verify** | A tool-calling node that checks if a specific medical service or procedure is covered under the user's plan. For example, if the user asks "Is my MRI covered?", this node looks up the user's plan benefits, checks coverage for MRI scans, and returns whether it's covered, any copay amounts, deductible requirements, etc. Results are stored in `state["tool_results"]`. |
| **claims_status** | A tool-calling node that retrieves the user's claims history and current claim statuses from mock data. It can answer questions like "What's the status of my recent claim?" or "How much have I paid out-of-pocket this year?" It queries the claims data, filters by user_id, and returns relevant claim records with their status, amounts, and dates. Results stored in `state["tool_results"]`. |
| **generate_response** | The final node that generates a natural language response to the user. It uses the LLM (Ollama) with a prompt that includes: the conversation history, any tool results from the previous nodes, and the user's original question. The LLM synthesizes all this information into a helpful, conversational response. This response is added to `state["messages"]` and becomes part of the conversation history. |
| **END** | LangGraph's exit point. After `generate_response` completes, the graph transitions to END, which signals that execution is complete. The final state (including all messages, tool results, and execution trace) is returned to the caller. |

**Conditional Routing Logic:**
- After `classify_intent`, edge function determines next node
- Routes based on extracted intent: "coverage", "benefits", "claims", "general"
- If no tools needed, routes directly to `generate_response`

### Technology Stack
- **LangGraph** - StateGraph, nodes, conditional edges
- **LangChain** - Ollama LLM integration, message types, tool decorators
- **Pydantic** - State schema validation (or TypedDict for simplicity)
- **Ollama** - Local LLM (llama3.3:70b-instruct-q4_K_S)
- **Python 3.13** - async/await for LLM calls

### File Organization
```
app/
  graph/
    __init__.py
    state.py          # ConversationState definition
    nodes.py          # All node functions
    edges.py          # Conditional edge functions
    graph.py          # Graph construction and compilation
  tools/
    __init__.py
    coverage.py       # Coverage lookup tool
    benefits.py       # Benefit verification tool
    claims.py         # Claims status tool
```

## 3. Implementation Notes
_Shared technical considerations across all features in this version._

### State Management
- Use TypedDict for simplicity initially (can upgrade to Pydantic later)
- State is passed through all nodes automatically by LangGraph
- Each node receives state and returns updated state dict
- Use `Annotated[List, add_messages]` for messages field to enable automatic message appending

### Tool Implementation Pattern
```python
from langchain.tools import tool

@tool
def coverage_lookup(user_id: str, query: str) -> dict:
    """Lookup coverage details for a user."""
    # Implementation
    return {"status": "success", "data": {...}}
```

### Node Implementation Pattern
```python
def node_name(state: ConversationState) -> dict:
    """Node description."""
    # Add to execution trace
    state["execution_trace"].append({
        "node": "node_name",
        "timestamp": datetime.now().isoformat()
    })

    # Node logic here

    # Return state updates
    return {"key": "value"}
```

### LLM Integration
- Use `ChatOllama` from `langchain_ollama` (NOT `langchain_community` - deprecated!)
- Install with: `uv pip install langchain-ollama`
- Configure with model name and temperature
- Use structured prompts with system and user messages
- Parse LLM responses to extract intent or generate replies

**Example:**
```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.3:70b-instruct-q4_K_S",
    temperature=0.7
)
```

### Testing Strategy
- Create CLI test script (`tests/test_agent.py`)
- Test each node individually first
- Test full graph with sample conversations
- Verify state persistence across turns
- Check execution trace completeness

### Learning Focus
- Add extensive inline comments explaining LangGraph concepts
- Document why each design decision was made
- Include examples of how to extend the graph
- Make execution trace human-readable

## 4. Other Technical Considerations
_Any other technical information that might be relevant to building this version._

### Performance
- All operations are in-memory (no database calls)
- Ollama inference is local but may take 2-5 seconds per call
- Keep prompts concise to reduce latency
- Consider streaming responses in future version

### Error Handling
- Wrap tool calls in try/except blocks
- Return error status in tool results
- Allow graph to continue even if tool fails
- Log errors to execution trace

### Mock Data Integration
- Reuse existing `app.data.loader` functions
- No changes needed to mock data files
- Tools should handle missing data gracefully

### State Persistence
- State only persists within a single graph invocation
- Multi-turn conversations will need session management (v0.3.0)
- For now, test with single invocations that simulate turns

### LangGraph Best Practices
- Keep nodes focused on single responsibility
- Use conditional edges for routing logic
- Don't mutate state directly; return updates
- Build graph once at startup, invoke multiple times

### Deprecation Note
- Use `langchain_ollama.ChatOllama` instead of `langchain_community.llms.Ollama`
- This avoids deprecation warnings from v0.1.0 retrospective

## 5. Design Decisions
_Technical and product decisions finalized for this version._

### ✅ D1: TypedDict for State Schema
**Decision:** Use TypedDict for state management.

**Rationale:** Simpler, less boilerplate, Python native. Sufficient for learning purposes. Can migrate to Pydantic in later version if runtime validation becomes important.

### ✅ D2: Detailed Execution Trace
**Decision:** Implement detailed execution trace with comprehensive information.

**Rationale:** For learning purposes, capture node name, timestamp, action taken, tool calls, LLM prompts/responses, and key state changes. This visibility is essential for understanding LangGraph internals.

**Trace Format:**
```python
{
    "node": "classify_intent",
    "timestamp": "2025-10-14T12:34:56",
    "action": "LLM call to classify user intent",
    "llm_prompt": "System: Classify intent...\nUser: What's covered?",
    "llm_response": "coverage",
    "state_changes": {"intent": "coverage"}
}
```

### ✅ D3: Single nodes.py File
**Decision:** Keep all node functions in a single `app/graph/nodes.py` file.

**Rationale:** With only 4-5 nodes, a single file is easier to navigate and understand the full flow. Can split into multiple files in future versions if complexity grows (e.g., `nodes/user.py`, `nodes/tools.py`, `nodes/response.py`).

**Note:** If maintenance becomes difficult (file >500 lines), consider splitting in v0.3.0 or later.

### ✅ D4: CLI Testing Only
**Decision:** Test with CLI script (`tests/test_agent.py`), no API endpoint in this version.

**Rationale:** Focus on LangGraph concepts without HTTP/WebSocket complexity. API endpoint and web interface come in v0.3.0. CLI testing provides direct access to graph internals for learning and debugging.

### ✅ D5: Conversational User Identification
**Decision:** Start conversations with "Who are you?" and identify user by name lookup.

**Implementation:**
1. Agent asks: "Hello! I'm your CARE insurance assistant. What's your name?"
2. User responds with first name (e.g., "Sarah", "John", "Emily")
3. `identify_user` node searches `user_profiles.json` by matching the `name` field
4. If found: Load full user profile into state
5. If not found: Respond "Sorry, you are not in our system. Please contact support."

**Example Flow:**
```
Agent: Hello! I'm your CARE insurance assistant. What's your name?
User: Sarah
Agent: Hi Sarah! I found your account. How can I help you today?

# OR if not found:
User: Bob
Agent: Sorry Bob, you are not in our system. Please contact support.
```

**Benefits:** More realistic conversation flow, demonstrates state management, teaches entity extraction.

### ✅ D6: Async Implementation
**Decision:** Use async/await for LLM calls and node functions.

**Rationale:** LangChain naturally supports async with Ollama. Modern Python pattern, better performance for I/O operations, scalable for future enhancements. Node functions will be `async def` and use `await` for LLM invocations.

**Example:**
```python
async def classify_intent(state: ConversationState) -> dict:
    """Async node for intent classification."""
    response = await llm.ainvoke(messages)  # Note: ainvoke, not invoke
    return {"intent": response.content}
```
