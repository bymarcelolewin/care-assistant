# Version Design Document : v0.8.0 - Add LangSmith Observability

Technical implementation and design guide for integrating LangSmith tracing and monitoring into the CARE Assistant project.

## 1. Features Summary
_Overview of features included in this version._

This version adds **LangSmith** integration to provide professional-grade observability for the LangGraph agent. LangSmith is LangChain's official platform for tracing, debugging, and monitoring LLM applications.

**Key Features:**
- **Automatic Tracing** - All LangGraph executions, LLM calls, and tool invocations are traced
- **Visual Debugging** - View execution traces in the LangSmith web dashboard
- **Optional Integration** - Application works with or without LangSmith (graceful degradation)
- **Environment-Based Config** - API keys stored in `.env` file (not committed to git)
- **Rich Metadata** - Traces include session_id, user_id, and conversation context
- **Learning Tool** - Students can compare local execution traces with cloud-based LangSmith traces

**Learning Value:**
- Demonstrates production-ready observability patterns
- Shows how to instrument LangGraph applications
- Teaches environment variable management for API keys
- Provides dual observability (local draggable windows + LangSmith cloud)

## 2. Technical Architecture Overview
_High-level technical structure that supports all features in this version._

### Technology Stack
- **LangSmith SDK**: `langsmith` Python package for tracing
- **Environment Management**: `python-dotenv` for `.env` file handling
- **Tracing Layer**: Automatic via LangChain/LangGraph integration (no code changes to nodes)
- **Configuration**: Environment variables (`LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`)

### Architecture Pattern
```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. Load .env (optional)                              │  │
│  │  2. Check LANGCHAIN_TRACING_V2 env var                │  │
│  │  3. Initialize LangSmith client if enabled            │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         LangGraph Agent Execution                     │  │
│  │  - Nodes, Edges, Tools (unchanged)                    │  │
│  │  - LangSmith auto-captures all LangChain calls        │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌─────────────────┐              ┌────────────────────┐  │
│  │ Local Traces    │              │ LangSmith Cloud    │  │
│  │ (Draggable      │ ───────────→ │ (Web Dashboard)    │  │
│  │  Windows)       │              │                    │  │
│  └─────────────────┘              └────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Integration Points
1. **app/main.py** - Load environment variables and initialize LangSmith on startup
2. **app/graph/graph.py** - No changes needed (auto-instrumented by LangChain)
3. **.env** - New file for API keys (git-ignored)
4. **.env.example** - Template file showing required variables (committed to git)
5. **.gitignore** - Ensure `.env` is ignored

### Data Flow
1. User starts application → `main.py` loads `.env` file
2. If `LANGCHAIN_TRACING_V2=true` → LangSmith client initializes
3. User sends message → LangGraph processes
4. LangChain automatically sends traces to LangSmith
5. User sees traces in both local UI and LangSmith dashboard

## 3. Implementation Notes
_Shared technical considerations across all features in this version._

### LangSmith Setup
**Prerequisites:**
- LangSmith account (free tier available at https://smith.langchain.com/)
- API key from LangSmith dashboard
- Project name in LangSmith

**Environment Variables:**
```bash
# .env file
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your_api_key_here
LANGCHAIN_PROJECT=care-assistant
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

### Code Changes

**1. Dependencies (`requirements.txt` or install command):**
```bash
uv pip install langsmith python-dotenv
```

**2. Update `app/main.py`:**
```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LangSmith will auto-initialize if env vars are set
# No additional code needed - LangChain handles it automatically

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    print("🚀 Starting CARE Assistant...")
    
    # Check if LangSmith tracing is enabled
    if os.getenv("LANGCHAIN_TRACING_V2") == "true":
        print("✅ LangSmith tracing enabled")
        print(f"📊 Project: {os.getenv('LANGCHAIN_PROJECT', 'default')}")
    else:
        print("⚪ LangSmith tracing disabled (optional)")
    
    # ... rest of startup code
```

**3. Add trace metadata and error handling:**
```python
# In app/api/chat.py - add metadata to traces with graceful degradation
import os

async def chat_endpoint(request: ChatRequest):
    # Add metadata to LangSmith trace
    metadata = {
        "session_id": session_id,
        "user_id": state.get("user_id"),
        "environment": os.getenv("ENVIRONMENT", "development")
    }
    
    # Wrap in try/except for offline/network failures
    try:
        # Set environment variables for this specific trace
        os.environ["LANGCHAIN_METADATA"] = json.dumps(metadata)
        
        # Invoke agent (automatically traced if LangSmith enabled)
        result = await agent.ainvoke(...)
    except Exception as e:
        # If LangSmith fails (offline, timeout, etc.), log and continue
        if "langsmith" in str(e).lower() or "smith.langchain" in str(e).lower():
            print(f"⚠️  LangSmith tracing failed (possibly offline): {e}")
            # Continue execution - don't let tracing block the agent
        else:
            raise  # Re-raise non-LangSmith errors
```

**4. Track token usage:**
```python
# In app/api/chat.py - capture token counts
from langchain.callbacks import get_openai_callback

# After agent invocation, check if token info is available
if hasattr(result, 'usage_metadata'):
    print(f"📊 Tokens: {result.usage_metadata.get('input_tokens', 0)} in / "
          f"{result.usage_metadata.get('output_tokens', 0)} out")
```

### File Structure
```
.
├── .env                          # API keys (git-ignored) - NEW
├── .env.example                  # Template (committed) - NEW
├── .gitignore                    # Updated to ignore .env
├── app/
│   ├── main.py                   # Load .env, check LangSmith - MODIFIED
│   └── api/
│       └── chat.py               # Optional: Add trace metadata - MODIFIED
└── .cody/
    └── project/
        └── library/
            └── docs/
                └── langsmith-setup.md  # Setup guide - NEW
```

### Graceful Degradation
- If `.env` file doesn't exist → app works normally (no tracing)
- If `LANGCHAIN_TRACING_V2` is not set → app works normally
- If API key is invalid → LangSmith logs warning but app continues
- **If internet is down** → LangSmith silently fails, app continues (wrapped in try/except)
- **Network timeout** → Don't block agent execution, log error and continue
- No breaking changes to existing functionality

### Testing Strategy
1. **Without LangSmith** - Run app without `.env` file → should work as before
2. **With LangSmith** - Add `.env` with valid credentials → traces appear in dashboard
3. **Invalid Credentials** - Test with bad API key → app should still run
4. **Trace Verification** - Send messages, check LangSmith dashboard for traces

## 4. Other Technical Considerations
_Shared any other technical information that might be relevant to building this version._

### Security
- **Never commit `.env` file** - Contains sensitive API keys
- Add `.env` to `.gitignore` immediately
- Provide `.env.example` as template with dummy values
- Document in README that users need to create their own `.env`

### Performance
- LangSmith adds minimal latency (~10-50ms per trace)
- Traces sent asynchronously (doesn't block agent execution)
- No impact on local execution traces

### Learning Experience
- Students can compare local traces vs. cloud traces
- LangSmith UI provides different insights (timing, token usage, costs)
- Shows production-ready patterns for monitoring LLM applications
- Optional feature means students can use with or without LangSmith account

### Documentation Updates
1. **README.md** - Add "Optional: LangSmith Integration" section
2. **Setup Instructions** - How to create account and get API key
3. **`.env.example`** - Clear comments explaining each variable
4. **Library Docs** - Create detailed LangSmith guide with screenshots

### Benefits for CARE Assistant
- **Debugging** - Easier to debug complex multi-tool conversations
- **Performance Analysis** - See which nodes/tools are slowest
- **Token Tracking** - Monitor LLM token usage per conversation
- **Production Pattern** - Students learn industry-standard monitoring
- **Dual Observability** - Local UI for learning, LangSmith for production insights

## 5. Open Questions
_Unresolved technical or product questions affecting this version._

### Resolved Questions
✅ **Should LangSmith be required or optional?**  
→ **Decision**: Optional. Application must work without it for students who don't want to create accounts.

✅ **Where should API keys be stored?**  
→ **Decision**: `.env` file (git-ignored) with `.env.example` template committed.

✅ **Do we need to modify nodes/tools for tracing?**  
→ **Decision**: No. LangChain auto-instruments all LangGraph components.

### Outstanding Questions - ✅ RESOLVED

✅ **Should we add custom tags or metadata to traces?**  
→ **Decision**: YES. Add session_id, user_id, and environment tags to make traces easier to filter in LangSmith dashboard.

✅ **Should we document LangSmith UI navigation?**  
→ **Decision**: NO. Keep documentation focused on setup and integration, not UI navigation.

✅ **Should we track any custom metrics?**  
→ **Decision**: YES. Track token usage (input/output tokens) for each conversation turn. This helps students understand LLM costs and performance.

✅ **Should we add LangSmith to the observability windows?**  
→ **Decision**: Future enhancement (v0.9.0 or later). Focus on core integration first.

### Implementation Decisions
- ✅ **Add custom tags**: session_id, user_id, environment
- ✅ **Track token metrics**: Capture input/output tokens via LangSmith callbacks
- ✅ **Internet resilience**: Wrap LangSmith calls in try/except, continue if offline
- ✅ **No UI docs**: Keep focus on setup and code integration
- ✅ **4th window**: Defer to future version
