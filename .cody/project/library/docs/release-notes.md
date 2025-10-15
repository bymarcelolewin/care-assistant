# CARE Assistant - Release Notes

This document tracks all releases of the CARE Assistant (Coverage Analysis and Recommendation Engine), a LangGraph-based learning application for understanding conversational AI agents.

---

## Version 0.2.0 - Core Agent
**Release Date:** October 14, 2025
**Status:** ✅ Completed

### Overview
Version 0.2.0 introduces the complete LangGraph agent with intelligent tool orchestration, multi-intent handling, and comprehensive execution tracing. This version represents a fully functional conversational insurance assistant that can handle complex, multi-part questions.

### 🎯 Key Features

#### 1. Intelligent Tool Orchestration
- **LLM-Based Tool Selection**: Replaced manual intent classification with an intelligent orchestrator that uses the LLM to determine which tools to call
- **Multi-Tool Support**: Can call multiple tools in a single turn to answer complex questions
- **Multi-Intent Handling**: Naturally handles questions with multiple intents (e.g., "What plan do I have, what does it cover, and do I have outstanding claims?")

#### 2. LangGraph Agent Architecture
- **State Management**: Full conversation state with messages, user profile, tool results, and execution trace
- **Graph Flow**: `identify_user → orchestrate_tools → generate_response`
- **Conditional Routing**: Smart routing based on user identification status
- **Async/Await**: All LLM and tool calls use async operations for efficiency

#### 3. Conversational User Identification
- Natural language name lookup instead of dropdown selection
- Searches `user_profiles.json` by name field (case-insensitive)
- Loads complete user profile into state for context

#### 4. Three Insurance Tools
- **coverage_lookup**: Returns comprehensive coverage information (plan details, deductibles, limits, member date)
- **benefit_verify**: Checks if specific medical services are covered
- **claims_status**: Retrieves claims history with filtering (pending, approved, denied)

#### 5. Execution Trace & Debugging
- Detailed trace of every node execution, LLM call, and tool invocation
- CLI commands: `trace` (last turn), `trace full` (entire conversation)
- Invaluable for learning how LangGraph works and debugging issues

#### 6. Interactive CLI
- Full-featured command-line interface for testing
- Commands: `trace`, `state`, `clear`, `quit`
- Real-time conversation with execution visibility
- Per-turn trace entry counts

### 📋 What's Included

**Core Implementation:**
- ✅ `app/graph/state.py` - ConversationState schema with reducers
- ✅ `app/graph/nodes.py` - All node implementations (identify_user, orchestrate_tools, generate_response)
- ✅ `app/graph/edges.py` - Conditional edge functions
- ✅ `app/graph/graph.py` - Graph construction and compilation
- ✅ `app/tools/coverage.py` - Coverage lookup tool
- ✅ `app/tools/benefits.py` - Benefit verification tool
- ✅ `app/tools/claims.py` - Claims status tool
- ✅ `tests/test_agent.py` - Interactive CLI test harness

**Documentation:**
- ✅ `.cody/project/library/docs/langgraph-agent-architecture.md` - Complete architecture guide
- ✅ README.md - Updated with v0.2.0 usage instructions and examples
- ✅ Example conversations demonstrating single-tool and multi-tool scenarios
- ✅ Comprehensive inline code comments for learning

**Build Artifacts:**
- ✅ `.cody/project/build/v0.2.0-core-agent/tasklist.md` - All 56 tasks completed
- ✅ `.cody/project/build/v0.2.0-core-agent/design.md` - Architecture decisions documented
- ✅ Updated workflow diagrams and PRD

### 🔧 Technical Details

**Architecture Pattern:** LLM-Based Orchestration
- Instead of hardcoded intent classification → tool routing, the orchestrator asks the LLM which tools are needed
- LLM responds with tool names (text-based, works with Ollama)
- Orchestrator parses response and executes all necessary tools
- Results aggregated in `tool_results` dict for response generation

**Why This Pattern?**
- Handles multi-intent questions naturally
- Simpler graph structure (3 nodes vs 6+)
- More flexible - LLM adapts to any question
- Eliminates need for maintaining intent classification logic

**State Schema:**
```python
class ConversationState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_id: Optional[str]
    user_profile: Optional[dict]
    tool_results: Optional[dict]  # Supports multiple tool results
    conversation_context: dict
    execution_trace: List[dict]
    needs_tool_call: Optional[bool]
```

**Ollama Integration:**
- Model: `llama3.3:70b-instruct-q4_K_S`
- Temperature: 0.7
- All LLM calls use `ainvoke()` for async operation
- Text-based tool orchestration (Ollama doesn't support native tool calling)

### 📊 Example Usage

**Simple Question (Single Tool):**
```
You: Do I have any pending claims?
Agent: [Calls claims_status tool]
      You have 1 pending claim: Physical Therapy ($250, submitted 2024-02-20)
```

**Complex Question (Multiple Tools):**
```
You: What plan do I have, how long have I been a member, what does it cover,
     and do I have outstanding claims?
Agent: [Calls coverage_lookup + benefit_verify + claims_status]
      Provides comprehensive answer covering all aspects
```

**Trace Output:**
```
[1] Node: identify_user - User already identified
[2] Node: orchestrate_tools - Determining tools needed
[3] Node: orchestrate_tools - LLM suggested: coverage_lookup, claims_status
[4] Node: orchestrate_tools - Executing coverage_lookup
[5] Node: orchestrate_tools - Executing claims_status
[6] Node: generate_response - Synthesizing response
```

### 🐛 Bug Fixes

**Fixed during development:**
1. **Initial bug**: Agent didn't stop at user identification, continued through entire graph
   - **Fix**: Added conditional edge that returns END when waiting for user name

2. **Orchestrator bug**: LLM wasn't calling any tools
   - **Root cause**: Ollama doesn't support `llm.bind_tools()` API
   - **Fix**: Switched to text-based orchestration where LLM returns tool names as text

3. **Empty LLM response**: Orchestrator prompt wasn't working with Ollama
   - **Fix**: Improved prompt with explicit examples and clearer instructions

4. **Trace accumulation**: `trace` command showed all events from conversation start
   - **Fix**: Track previous trace count, show only new entries per turn
   - **Added**: `trace full` command to see complete history

5. **Data hallucination**: Agent made up data instead of using actual profile data
   - **Fix**: Enhanced system prompt with complete user profile fields and explicit instructions

6. **Personal info refusal**: Agent refused to share age/member date
   - **Fix**: Added explicit permission in system prompt (local app with user consent)

### 📚 Learning Outcomes

By studying this version, developers learn:
- ✅ LangGraph state management with reducers
- ✅ Building nodes as async functions
- ✅ Conditional edge routing
- ✅ Tool integration with LangChain's @tool decorator
- ✅ LLM-based orchestration patterns
- ✅ Execution tracing for visibility
- ✅ Handling multi-intent questions
- ✅ Ollama integration with langchain-ollama

### 🔄 Breaking Changes
None - this is the first functional version of the agent.

### ⚠️ Known Limitations
1. **Tool parameter extraction**: `benefit_verify` uses default "general medical" for service_type instead of extracting from question
2. **Error handling**: Limited error handling for LLM failures or tool errors
3. **Tool selection accuracy**: Depends on LLM's ability to parse question correctly
4. **No tool validation**: Doesn't validate if selected tools make sense together

### 🎯 Next Steps (v0.3.0)
- Web interface with HTML/CSS/JS
- User selection UI
- Chat interface with message history
- Collapsible execution trace visualization
- WebSocket streaming for real-time responses

---

## Version 0.1.0 - Environment & Foundation
**Release Date:** October 13, 2025
**Status:** ✅ Completed

### Overview
Version 0.1.0 establishes the foundational environment and infrastructure for the CARE Assistant project. This version focuses on setting up the development environment, creating mock data, and verifying that all core dependencies work correctly.

### 🎯 Key Features

#### 1. Development Environment
- **Python 3.10+** with modern async/await support
- **UV Package Manager**: Fast, reliable dependency management
- **Virtual Environment**: Isolated Python environment with .venv
- **FastAPI Server**: Basic REST API skeleton with health checks

#### 2. Mock Data System
- **Three JSON Data Files**:
  - `user_profiles.json` - 3 mock users with insurance information
  - `insurance_plans.json` - 3 plan types (PPO Gold, HMO Silver, EPO Bronze)
  - `claims_data.json` - 9 mock claims across different statuses
- **Data Loader Module**: Centralized data access functions
- **Data Documentation**: README explaining data structure and purpose

#### 3. Ollama Integration
- **Local LLM**: Ollama with llama3.3:70b-instruct-q4_K_S
- **Integration Package**: langchain-ollama (non-deprecated)
- **Test Script**: Verification that Ollama connection works
- **No External APIs**: Completely local execution

#### 4. Project Structure
- Clean directory organization for future development
- Separation of concerns (data, tools, graph, API, tests)
- Documentation at each level
- Cody Framework integration for spec-driven development

### 📋 What's Included

**Environment & Dependencies:**
- ✅ Virtual environment with UV
- ✅ LangGraph and LangChain packages
- ✅ langchain-ollama for local LLM integration
- ✅ FastAPI and Uvicorn for web server
- ✅ Python 3.13 support

**Mock Data:**
- ✅ 3 user profiles (Sarah Johnson, Michael Chen, Emily Rodriguez)
- ✅ 3 insurance plans (PPO Gold, HMO Silver, EPO Bronze)
- ✅ 9 claims records (approved, pending, denied)
- ✅ Data loader with utility functions
- ✅ Data documentation

**Basic API:**
- ✅ FastAPI application skeleton
- ✅ GET / - API information endpoint
- ✅ GET /health - Health check endpoint
- ✅ Startup event with data loading
- ✅ Interactive API docs (Swagger UI)

**Testing:**
- ✅ `tests/test_ollama.py` - Ollama connection test
- ✅ Verification script for data loading

**Documentation:**
- ✅ README.md with setup instructions
- ✅ app/data/README.md explaining data structure
- ✅ Inline comments throughout code
- ✅ Cody Framework specifications

### 🔧 Technical Details

**Package Versions:**
- Python: 3.13
- LangGraph: Latest
- LangChain: Latest
- langchain-ollama: Latest (replaces deprecated langchain-community.llms.Ollama)
- FastAPI: Latest
- Uvicorn: Latest

**Mock Data Structure:**

**User Profile:**
```json
{
  "user_id": "user_001",
  "name": "Sarah Johnson",
  "age": 34,
  "plan_id": "ppo_gold",
  "member_since": "2022-03-15",
  "deductible_annual": 1500,
  "deductible_met": 800,
  "out_of_pocket_max": 6000,
  "out_of_pocket_spent": 2100,
  "dependents": 2
}
```

**Insurance Plan:**
```json
{
  "plan_id": "ppo_gold",
  "plan_name": "PPO Gold Plan",
  "plan_type": "PPO",
  "monthly_premium": 450,
  "deductible_individual": 1500,
  "out_of_pocket_max": 6000,
  "coverage": {
    "primary_care": { "copay": 25, "coverage_percent": 100 },
    "specialist": { "copay": 50, "coverage_percent": 100 },
    ...
  }
}
```

**Claim Record:**
```json
{
  "claim_id": "CLM-2024-001",
  "user_id": "user_001",
  "service_type": "Primary Care Visit",
  "provider": "Dr. Smith Medical",
  "date_of_service": "2024-01-15",
  "amount_billed": 150,
  "amount_covered": 125,
  "patient_responsibility": 25,
  "status": "approved"
}
```

**Ollama Configuration:**
- Model: llama3.3:70b-instruct-q4_K_S
- Running locally on default port (11434)
- No API keys or external connections required

### 📊 How to Use

**Start the FastAPI Server:**
```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

**Test Ollama Integration:**
```bash
python tests/test_ollama.py
```

**Expected Output:**
```
🚀 Starting CARE Assistant...
📂 Loading mock data...
  ✓ Loaded 3 user profiles
  ✓ Loaded 3 insurance plans
  ✓ Loaded 9 claims records
✅ Application startup complete!
```

### 🐛 Bug Fixes
None - initial release.

### 📚 Learning Outcomes

By studying this version, developers learn:
- ✅ Setting up Python virtual environments with UV
- ✅ Integrating Ollama with LangChain
- ✅ Creating mock data for development
- ✅ Basic FastAPI server setup
- ✅ Project structure best practices
- ✅ Documentation standards

### 🔄 Breaking Changes
None - initial release.

### ⚠️ Known Limitations
1. **No agent logic**: Just environment setup, no LangGraph agent yet
2. **Static data**: All data is hardcoded in JSON files
3. **No web UI**: API only, no frontend
4. **Basic endpoints**: Only health check and info endpoints

### 🎯 Next Steps (v0.2.0)
- LangGraph state schema
- Tools for coverage, benefits, claims
- Graph nodes and edges
- Conditional routing
- Basic conversation flow

---

## Future Versions

### Version 0.3.0 - Web Interface (Planned)
- HTML/CSS/JS chat interface
- User selection dropdown
- Message send/receive
- Execution trace visualization
- WebSocket streaming

### Version 1.0.0 - Enhanced Learning Features (Planned)
- Detailed execution traces with filtering
- State visualization
- Comprehensive documentation
- Extension guide for adding new features
- Video walkthroughs

---

## Changelog Summary

| Version | Release Date | Key Features | Status |
|---------|-------------|--------------|--------|
| v0.1.0 | Oct 13, 2025 | Environment, mock data, Ollama integration | ✅ Complete |
| v0.2.0 | Oct 14, 2025 | LangGraph agent, tool orchestration, CLI | ✅ Complete |
| v0.3.0 | TBD | Web interface, chat UI | 🔄 Planned |
| v1.0.0 | TBD | Enhanced learning features | 🔄 Planned |

---

## Contributing

This is a learning project demonstrating LangGraph concepts. Contributions are welcome! Please refer to the main README.md for development setup instructions.

## Support

For questions or issues:
- Review the architecture documentation in `.cody/project/library/docs/`
- Check the example conversations in README.md
- Examine the execution traces using the CLI `trace` command

## License

See main repository for license information.
