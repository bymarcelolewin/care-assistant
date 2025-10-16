# CARE Assistant v0.3.0 - Complete Agent Workflow

**Version:** 0.3.0  
**Last Updated:** October 15, 2025  
**Architecture:** LangGraph-based conversational agent

## Visual Diagram

See the Mermaid flowchart in [v3-agent-workflow.mmd](./v3-agent-workflow.mmd)

The diagram includes **state management annotations** (green dashed boxes with 📊) showing exactly which state fields are updated after each major node. This helps visualize how data flows through the conversation.

To view the diagram:
- Open in VS Code with Mermaid extension
- View on GitHub (automatically renders)
- Use Mermaid Live Editor: https://mermaid.live/

---

## Workflow Overview

### **Phase 1: User Identification** (`identify_user` node)

The first phase handles user identification through a conversational name-based lookup:

1. **First Visit (No messages)**: Ask "What's your name?"
2. **Name Extraction**: Use LLM with structured output to extract name from natural language
3. **User Lookup**: Search `user_profiles.json` by name (case-insensitive)
4. **Welcome Message**: Personalized greeting with member history + set `first_greeting` flag
5. **Conditional Edge**: Skip tools on first greeting, wait for actual question

**Key Features:**
- Handles various name formats: "John", "I'm John", "My name is John Smith"
- Uses Pydantic model for structured LLM output
- Confidence scoring for retry logic
- Graceful handling of users not in system

### **Phase 2: Tool Orchestration** (`orchestrate_tools` node)

The second phase intelligently coordinates tool execution based on user questions:

1. **LLM Analysis**: Analyze user question to determine which tools are needed
2. **Multi-Tool Support**: Can call 1, 2, or 3 tools in a single turn
3. **Tool Execution**:
   - `coverage_lookup`: Plan details, deductibles, limits, member info
   - `benefit_verify`: Service coverage verification
   - `claims_status`: Claims history and pending/approved/denied status
4. **Progress Messages**: User-friendly status updates ("Let me check...")
5. **Result Storage**: All tool results stored in `tool_results` dict

**Key Features:**
- LLM decides which tools to call (no manual classification)
- Sequential tool execution with progress tracking
- Handles complex multi-intent questions
- Graceful handling of questions needing no tools

### **Phase 3: Response Generation** (`generate_response` node)

The final phase synthesizes a natural language response:

1. **Context Building**: Combine user profile + conversation history + tool results
2. **System Prompt**: Instruct LLM to use only provided information
3. **LLM Synthesis**: Generate natural, conversational response
4. **State Cleanup**: Clear `tool_results` and temporary flags for next turn

**Key Features:**
- Comprehensive context from multiple sources
- Privacy-aware (local deployment, user-consented data sharing)
- Error handling with friendly fallback messages
- Clean state management between turns

---

## Key Design Decisions

### ✅ **Eliminated Manual Intent Classification**

**Old Architecture (v0.1.0 - v0.2.0):**
```
identify_user → classify_intent → route_by_intent → single_tool → generate_response
```

**New Architecture (v0.3.0):**
```
identify_user → orchestrate_tools → generate_response
```

**Benefits:**
- Simpler graph structure (3 nodes vs 5+ nodes)
- Handles complex multi-intent questions in single turn
- LLM intelligence replaces manual routing logic
- More flexible and extensible

**Example:** User asks "What plan do I have and do I have pending claims?"
- **Old:** Would only route to one tool (likely `coverage_lookup`)
- **New:** Calls both `coverage_lookup` AND `claims_status` automatically

### ✅ **LLM-Powered Name Extraction**

Uses `with_structured_output()` with Pydantic model:

```python
class NameExtraction(BaseModel):
    name: Optional[str] = Field(description="The person's first name or full name")
    confidence: str = Field(description="Confidence level: 'high' or 'low'")
```

**Handles natural language:**
- "I'm Marcelo, your patient" → "Marcelo"
- "My name is Sarah Smith" → "Sarah Smith"
- "Call me Mike" → "Mike"
- "Emily" → "Emily"

**Confidence scoring enables retry logic:**
- High confidence → Proceed with user lookup
- Low confidence → Ask user to clarify

### ✅ **First Greeting Flag**

Prevents orchestrator from processing the welcome message as a question:

**Flow:**
1. User provides name → `first_greeting = True`
2. Send welcome message → END (wait for actual question)
3. User asks question → `first_greeting = False` → orchestrate_tools

**Without this flag:** The welcome message would trigger unnecessary tool calls

**UX Benefit:** Clean separation between identification and conversation

### ✅ **Multi-Tool Coordination**

Single question can trigger multiple tools:

**Example 1:** "What plan do I have, how long have I been a member, what does it cover, and do I have outstanding claims?"

**Tools Called:**
- `coverage_lookup` (plan info, member since)
- `benefit_verify` (coverage details)
- `claims_status` (pending claims)

**Example 2:** "Thank you for your help!"

**Tools Called:** None (general conversation)

**LLM Decision:** The orchestrator analyzes the question and intelligently selects 0, 1, 2, or 3 tools based on what information is needed.

---

## State Management

### **Persistent State Fields**

These fields persist across the entire conversation:

| Field | Type | Purpose |
|-------|------|---------|
| `messages` | `List[BaseMessage]` | Full conversation history (with `add_messages` reducer) |
| `user_id` | `Optional[str]` | Identified user ID (e.g., "user_001") |
| `user_profile` | `Optional[dict]` | Complete user data from JSON |
| `conversation_context` | `dict` | Extracted entities and topics |
| `execution_trace` | `List[dict]` | Node execution log for debugging |

### **Temporary State Fields**

These fields are cleared after each turn:

| Field | Type | Purpose |
|-------|------|---------|
| `tool_results` | `Optional[dict]` | Tool outputs for current turn |
| `progress_messages` | `Optional[List[str]]` | UI feedback messages |
| `first_greeting` | `Optional[bool]` | One-time flag after identification |

**Why clear temporary fields?**
- Prevents stale data from previous turns
- Ensures each turn starts fresh
- Reduces state size

---

## Conditional Routing

### **`should_continue_after_identify` Edge Function**

This is the only conditional edge in the graph, and it handles three scenarios:

```python
def should_continue_after_identify(state: ConversationState) -> Literal["orchestrate_tools", "__end__"]:
    # Scenario 1: First greeting after identification
    if state.get("first_greeting"):
        return "__end__"  # Show welcome only, wait for question
    
    # Scenario 2: User is identified and ready for question
    if state.get("user_id"):
        return "orchestrate_tools"  # Continue to tools
    
    # Scenario 3: No user_id yet
    return "__end__"  # Wait for name input
```

**Flow Control:**

| State | Route | Reason |
|-------|-------|--------|
| `first_greeting = True` | END | Just showed welcome, wait for question |
| `user_id = "user_001"` | orchestrate_tools | User identified, process question |
| `user_id = None` | END | Still waiting for name |

This ensures proper flow control at the critical user identification checkpoint.

---

## Graph Structure

### **Nodes (3)**

| Node | Type | Purpose |
|------|------|---------|
| `identify_user` | Data Lookup | Find user by name, load profile |
| `orchestrate_tools` | LLM + Tools | Intelligently select and execute tools |
| `generate_response` | LLM | Synthesize natural language response |

### **Edges**

| From | To | Type | Condition |
|------|-----|------|-----------|
| START | `identify_user` | Normal | Always |
| `identify_user` | `orchestrate_tools` | Conditional | User identified & not first greeting |
| `identify_user` | END | Conditional | Waiting for name or first greeting |
| `orchestrate_tools` | `generate_response` | Normal | Always |
| `generate_response` | END | Normal | Always |

### **Tools (3)**

| Tool | Input | Output |
|------|-------|--------|
| `coverage_lookup` | user_id, query | Plan details, deductible, limits |
| `benefit_verify` | user_id, service_type | Coverage verification |
| `claims_status` | user_id, status_filter | Claims history |

---

## Example Execution Traces

### **Example 1: Simple Question (Single Tool)**

**User:** "Do I have any pending claims?"

**Execution:**
1. `identify_user` → User already identified: user_001
2. `orchestrate_tools` → LLM selects: `claims_status`
3. Tool execution → Returns 1 pending claim
4. `generate_response` → "You have 1 pending claim: Physical Therapy ($250)"

**Trace Entries:** 5

### **Example 2: Complex Question (Multiple Tools)**

**User:** "What plan do I have, how long have I been a member, what does it cover, and do I have outstanding claims?"

**Execution:**
1. `identify_user` → User already identified: user_001
2. `orchestrate_tools` → LLM selects: `coverage_lookup`, `benefit_verify`, `claims_status`
3. Tool execution:
   - `coverage_lookup` → PPO Gold, member since March 2022
   - `benefit_verify` → Comprehensive coverage details
   - `claims_status` → 1 pending claim
4. `generate_response` → Comprehensive answer combining all results

**Trace Entries:** 10+

### **Example 3: General Conversation (No Tools)**

**User:** "Thank you for your help!"

**Execution:**
1. `identify_user` → User already identified: user_001
2. `orchestrate_tools` → LLM decides: No tools needed
3. `generate_response` → "You're welcome! Feel free to ask anything else."

**Trace Entries:** 4

---

## Architecture Evolution

### **v0.1.0 - Environment & Foundation**
- Basic setup, mock data, Ollama integration

### **v0.2.0 - Core Agent**
- Initial graph with `classify_intent` node
- Manual routing: intent → specific tool
- Single-tool execution per turn
- CLI interface

### **v0.3.0 - Web Interface (Current)**
- ✅ Eliminated `classify_intent` node
- ✅ LLM-based tool orchestration
- ✅ Multi-tool coordination
- ✅ Modern web UI with Next.js
- ✅ Session management
- ✅ Enhanced UX features

### **v1.0.0 - Enhanced Learning Features (Planned)**
- Enhanced execution traces
- Better state visualization
- Comprehensive documentation
- Extension guides

---

## Technical Specifications

**Graph Nodes:** 3 (identify_user, orchestrate_tools, generate_response)  
**Conditional Edges:** 1 (should_continue_after_identify)  
**Tools:** 3 (coverage_lookup, benefit_verify, claims_status)  
**LLM:** Ollama (llama3.3:70b-instruct-q4_K_S)  
**Framework:** LangGraph + LangChain  
**Backend:** FastAPI (Python 3.13)  
**Frontend:** Next.js 15 + TypeScript + shadcn/ui  

---

## Learning Resources

For more information about the implementation:

- **Code:** `app/graph/` folder
- **Planning:** `.cody/project/plan/` folder
- **Build History:** `.cody/project/build/` folder
- **Architecture Docs:** `.cody/project/library/docs/langgraph-agent-architecture.md`

---

*This document describes the v0.3.0 architecture as of October 15, 2025.*
