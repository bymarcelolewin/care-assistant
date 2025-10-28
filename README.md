# ❤️ CARE Assistant - Coverage Analysis and Recommendation Engine

![Version](https://img.shields.io/badge/version-0.9.0-blue)

![CARE Assistant](./sample-screen.png)

A hands-on learning application demonstrating core LangGraph concepts through a practical example: an AI-powered insurance coverage assistant that helps users understand their healthcare benefits.

### Using Observability Windows

The application includes three draggable windows for inspecting the agent's behavior:

**To open windows:**
1. Look for the checkboxes in the chat header (Observability section)
2. Check the boxes for the windows you want to view:
   - **Memory** - View current conversation state, user profile, and tool results
   - **Graph** - See the visual LangGraph structure
   - **Steps** - Watch the execution trace as the agent processes messages

**Window features:**
- **Draggable** - Click and drag the header to reposition anywhere on screen
- **Stackable** - Click any window to bring it to the front
- **Real-time updates** - All windows update live as you chat
- **Default closed** - Windows are hidden by default for a clean interface

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:
- **Python 3.12 or 3.13** (required: >=3.12, <3.14)
- **[uv](https://github.com/astral-sh/uv)** package manager - Install with:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **[Ollama](https://ollama.ai/)** - Download and install from https://ollama.ai/

### Step-by-Step Installation

**1. Clone the repository and navigate to the project folder**
```bash
git clone https://github.com/bymarcelolewin/care-assistant.git
cd care-assistant
```

**2. Pull an Ollama model**
```bash
# Pull the default model used in the code (or any model you prefer)
ollama pull llama3.2

# Or use a larger model for better quality:
# ollama pull llama3.3:70b-instruct-q4_K_S

# Verify the model is available
ollama list
```

**Note:** The code is configured to use `llama3.2` by default. You can change the model in [app/graph/nodes.py](app/graph/nodes.py#L32) to use any Ollama model.

All subsequent commands should be run from this `care-assistant` directory.

**3. Install Python dependencies**
```bash
# Install all dependencies and create virtual environment automatically
uv sync
```

This single command will:
- Create a virtual environment in `.venv/` (if it doesn't exist)
- Install Python 3.13 (as specified in pyproject.toml)
- Install all project dependencies

**4. (Optional) Configure LangSmith for tracing**

If you want cloud-based observability (optional):
```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your LangSmith API key from https://smith.langchain.com/
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=your_api_key_here
```

**Note:** The app works perfectly without LangSmith.

**5. Build the frontend**
```bash
cd frontend
npm install
npm run build
cd ..
```

This creates the static frontend files in `frontend/out/` that the backend will serve.

**6. Verify installation**
```bash
# Test Ollama integration
python tests/test_ollama.py
```

If successful, you should see: `✅ Ollama integration test PASSED!`

## 🏃 Running It

From the `care-assistant` directory, make sure Ollama is running, then start the server:

```bash
uv run uvicorn app.main:app --port 8000
```

When the server starts successfully, you should see:
```
🚀 Starting CARE Assistant - Coverage Analysis and Recommendation Engine...
📚 Version 0.9.0
📂 Loading mock data...
  ✓ Loaded 3 user profiles
  ✓ Loaded 3 insurance plans
  ✓ Loaded 9 claims records
✅ Application startup complete!
```

Open your browser to: **http://localhost:8000/**

That's it! You should see the CARE Assistant chat interface.

**Note:** The backend serves the pre-built static frontend from `frontend/out/`. If you make changes to the frontend, rebuild it with `cd frontend && npm run build && cd ..`

## 🎯 Project Goals

This is a **learning-focused POC** designed to demonstrate:
- **State management** across conversation turns
- **Tool integration** for querying insurance data
- **Intelligent tool orchestration** using LLM-based multi-tool coordination
- **Graph structure** with nodes and edges
- **Execution visibility** for understanding LangGraph internals

## 🏗️ Architecture

- **Backend**: Python 3.12-3.13 with FastAPI
- **LLM Framework**: LangGraph 1.0.1 + LangChain 1.0.2
- **Local LLM**: Ollama (default: llama3.2, configurable)
- **Observability**: LangSmith (optional cloud tracing)
- **Frontend**: Next.js 15 + TypeScript + shadcn/ui + Tailwind CSS
- **Package Management**: uv (Python) + npm (Frontend)
- **Data**: Mock JSON files (no real APIs or databases)
- **Deployment**: Static build with single-server architecture

## 📁 Project Structure

```
.
├── app/                          # Backend application code
│   ├── main.py                  # FastAPI entry point + static serving
│   ├── data/                    # Data loader module
│   │   ├── loader.py            # Data loading functions
│   │   └── __init__.py
│   ├── tools/                   # LangGraph tools
│   │   ├── __init__.py
│   │   ├── coverage.py          # Coverage lookup tool
│   │   ├── benefits.py          # Benefit verification tool
│   │   └── claims.py            # Claims status tool
│   ├── graph/                   # LangGraph agent
│   │   ├── __init__.py
│   │   ├── state.py             # State schema (TypedDict)
│   │   ├── nodes.py             # Nodes with LLM (llama3.2)
│   │   ├── edges.py             # Conditional routing
│   │   └── graph.py             # Graph construction
│   └── api/                     # REST API endpoints
│       ├── __init__.py
│       ├── chat.py              # POST /api/chat endpoint
│       ├── graph.py             # GET /api/graph endpoint
│       └── sessions.py          # Session management
├── frontend/                    # Next.js web application
│   ├── app/                     # Next.js App Router
│   │   ├── layout.tsx           # Root layout with ErrorBoundary
│   │   ├── page.tsx             # Main chat page
│   │   └── globals.css          # Global styles
│   ├── components/              # React components
│   │   ├── chat/                # Chat UI components
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── ChatHeader.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── ThinkingIndicator.tsx
│   │   ├── observability/       # Draggable observability windows
│   │   │   ├── DraggableMemoryWindow.tsx
│   │   │   ├── DraggableGraphWindow.tsx
│   │   │   ├── DraggableStepsWindow.tsx
│   │   │   ├── MemoryContent.tsx
│   │   │   ├── GraphContent.tsx
│   │   │   └── ExecutionStepsContent.tsx
│   │   ├── ui/                  # shadcn/ui components
│   │   └── ErrorBoundary.tsx
│   ├── lib/                     # Utilities
│   │   ├── api.ts               # API client
│   │   ├── types.ts             # TypeScript interfaces
│   │   └── utils.ts             # Helper functions
│   ├── out/                     # Static build output (generated by npm run build)
│   ├── next.config.ts           # Next.js configuration
│   ├── package.json             # Frontend dependencies
│   └── tsconfig.json            # TypeScript configuration
├── tests/                       # Test files
│   ├── test_ollama.py          # Ollama integration test
│   └── test_agent.py           # Interactive CLI test
├── data/                        # Mock JSON data files
│   ├── user_profiles.json      # User insurance profiles
│   ├── insurance_plans.json    # Plan types and coverage
│   └── claims_data.json        # Claims history
├── .cody/                       # Cody Framework (project management)
├── requirements.txt             # Python dependencies (pinned versions)
├── .venv/                       # Python virtual environment (gitignored)
└── README.md                    # This file
```

## 📚 Mock Data

The application uses mock insurance data to demonstrate LangGraph concepts:

- **3 User Profiles**: Diverse scenarios (individual, family, different plan types)
- **3 Insurance Plans**: PPO Gold, HMO Silver, EPO Bronze
- **9 Claims Records**: Mix of approved, pending, and denied claims

Data files are located in the [data/](data/) folder at the project root.

## 🧪 Testing

### Test Ollama Integration

```bash
python tests/test_ollama.py
```

### Test Interactive CLI

```bash
python tests/test_agent.py
```

**Available Commands:**
- Type your questions naturally
- `trace` - Show last turn's execution trace
- `state` - Display current state summary
- `clear` - Start a fresh conversation
- `quit` - Exit

## 📝 Documentation

### Build Tracking
- [feature-backlog.md](.cody/project/build/feature-backlog.md) - All versions and features
- [release-notes.md](.cody/project/build/release-notes.md) - Comprehensive release history

### Technical Documentation
- [LangGraph Agent Architecture](.cody/project/library/docs/langgraph-agent-architecture.md) - Deep dive into the agent design
- [Mock Data Guide](.cody/project/library/docs/mock-data.md) - Data schemas and usage
- [Agent Workflow (Technical)](.cody/project/library/docs/v3-agent-workflow.md) - Technical workflow documentation
- [Agent Workflow (Business)](.cody/project/library/docs/v3-agent-workflow-business.md) - Business-focused workflow

### Observability
- [LangSmith Setup Guide](.cody/project/library/docs/langsmith-setup.md) - Complete LangSmith configuration

