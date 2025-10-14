# CARE Assistant - Coverage Analysis and Recommendation Engine

A hands-on learning application demonstrating core LangGraph concepts through a practical example: an AI-powered insurance coverage assistant that helps users understand their healthcare benefits.

**Version:** 0.1.0 - Environment & Foundation
**Status:** ✅ Development Environment Ready

## 🎯 Project Goals

This is a **learning-focused POC** designed to demonstrate:
- **State management** across conversation turns
- **Tool integration** for querying insurance data
- **Conditional routing** based on user intent
- **Graph structure** with nodes and edges
- **Execution visibility** for understanding LangGraph internals

## 🏗️ Architecture

- **Backend**: Python 3.10+ with FastAPI
- **LLM Framework**: LangGraph + LangChain
- **Local LLM**: Ollama (llama3.3:70b-instruct-q4_K_S)
- **Frontend**: Simple HTML/CSS/JS (to be built in v0.3.0)
- **Package Management**: uv
- **Data**: Mock JSON files (no real APIs or databases)

## 📁 Project Structure

```
.
├── app/                      # Application code
│   ├── main.py              # FastAPI entry point
│   ├── data/                # Mock data and loader
│   │   ├── user_profiles.json
│   │   ├── insurance_plans.json
│   │   ├── claims_data.json
│   │   ├── loader.py
│   │   └── README.md        # Data documentation
│   ├── tools/               # LangGraph tools (v0.2.0)
│   ├── graph/               # LangGraph nodes/edges (v0.2.0)
│   ├── api/                 # API endpoints (future)
│   └── static/              # Frontend files (v0.3.0)
├── tests/                   # Test files
│   └── test_ollama.py      # Ollama integration test
├── .venv/                   # Virtual environment
├── .cody/                   # Cody framework files
│   ├── config/
│   └── project/
│       ├── plan/            # Planning documents
│       └── build/           # Build artifacts
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:
- ✅ Python 3.10 or higher
- ✅ [uv](https://github.com/astral-sh/uv) package manager installed
- ✅ [Ollama](https://ollama.ai/) installed and running
- ✅ Ollama model: `llama3.3:70b-instruct-q4_K_S` or `llama3.2:latest`

### Installation

**1. Clone or navigate to the project directory**
```bash
cd "/Volumes/NCC1701/Development/playground/LangGraph Playground"
```

**2. Create and activate virtual environment**
```bash
# Create virtual environment with uv
uv venv

# Activate (macOS/Linux)
source .venv/bin/activate
```

**3. Install dependencies**
```bash
# Install core dependencies
uv pip install langgraph langchain langchain-community

# Install web framework
uv pip install fastapi uvicorn
```

**4. Verify Ollama is running**
```bash
# Check Ollama service
ollama list

# Should show llama3.3:70b-instruct-q4_K_S or llama3.2:latest
```

**5. Test the installation**
```bash
# Test Ollama integration
python tests/test_ollama.py

# Should show successful connection and LLM responses
```

## 🏃 Running the Application

### Start the FastAPI Server

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Run the server
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### Available Endpoints

**Version 0.1.0** includes basic endpoints:

- **GET /** - API information
  ```bash
  curl http://localhost:8000/
  ```

- **GET /health** - Health check
  ```bash
  curl http://localhost:8000/health
  ```

- **GET /docs** - Interactive API documentation (Swagger UI)
  - Open in browser: http://localhost:8000/docs

- **GET /redoc** - Alternative API documentation
  - Open in browser: http://localhost:8000/redoc

### Verify Data Loading

When the server starts, you should see:
```
🚀 Starting CARE Assistant - Coverage Analysis and Recommendation Engine...
📚 Version 0.1.0 - Environment & Foundation
📂 Loading mock data...
  ✓ Loaded 3 user profiles
  ✓ Loaded 3 insurance plans
  ✓ Loaded 9 claims records
✅ Application startup complete!
```

## 📚 Mock Data

The application uses mock insurance data to demonstrate LangGraph concepts:

- **3 User Profiles**: Diverse scenarios (individual, family, different plan types)
- **3 Insurance Plans**: PPO Gold, HMO Silver, EPO Bronze
- **9 Claims Records**: Mix of approved, pending, and denied claims

See [app/data/README.md](app/data/README.md) for detailed schema documentation.

## 🧪 Testing

### Test Ollama Integration

```bash
python tests/test_ollama.py
```

This verifies:
- ✅ LangChain can connect to Ollama
- ✅ llama3.3:70b model responds correctly
- ✅ Insurance-related prompts work

### Verify Dependencies

```bash
python -c "
import langgraph
import langchain
import langchain_community
import fastapi
import uvicorn
import pydantic
print('✅ All imports successful!')
"
```

### Check Installed Packages

```bash
uv pip list
```

## 📖 Learning Path

This project is structured for progressive learning:

### ✅ Version 0.1.0 - Environment & Foundation (Current)
- Virtual environment setup
- Dependency installation
- Project structure
- Mock data creation
- Basic FastAPI server
- Ollama integration verification

### 🔄 Version 0.2.0 - Core Agent (Next)
- LangGraph state schema
- Tools for coverage lookup, benefit verification, claims status
- Graph nodes (identify user, classify intent, route to tools, generate response)
- Conditional edges and routing
- Basic conversation flow

### 🔄 Version 0.3.0 - Web Interface
- HTML/CSS/JS chat interface
- User selection dropdown
- Message send/receive
- Execution trace visualization

### 🔄 Version 1.0.0 - Enhanced Learning Features
- Detailed execution traces
- State visualization
- Comprehensive documentation
- Extension guide

## 🛠️ Development

### Key Files to Understand

1. **[app/main.py](app/main.py)** - FastAPI application and startup logic
2. **[app/data/loader.py](app/data/loader.py)** - Data loading and query functions
3. **[tests/test_ollama.py](tests/test_ollama.py)** - Ollama integration testing

### Adding Code

All application code lives in the `app/` directory:
- Use type hints throughout
- Add docstrings to functions
- Follow PEP 8 conventions
- Keep learning focus (extensive comments)

### Running Tests

```bash
# Run Ollama test
python tests/test_ollama.py

# Future: Run all tests
# pytest tests/
```

## 🐛 Troubleshooting

### Virtual Environment Issues

**Problem:** `source .venv/bin/activate` fails
```bash
# Make sure you're in the project directory
pwd

# Should show: /Volumes/NCC1701/Development/playground/LangGraph Playground

# Try with explicit path
source ./.venv/bin/activate
```

### Ollama Connection Issues

**Problem:** Test fails to connect to Ollama
```bash
# Check Ollama is running
ollama list

# If not running, start it (depends on installation method)
# Then verify model is available
ollama pull llama3.3:70b-instruct-q4_K_S
```

### Import Errors

**Problem:** Modules not found
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Verify packages are installed
uv pip list | grep -E "(langgraph|langchain|fastapi)"

# Reinstall if needed
uv pip install langgraph langchain langchain-community fastapi uvicorn
```

### Server Won't Start

**Problem:** FastAPI server fails to start
```bash
# Check for syntax errors
python -m py_compile app/main.py

# Try running directly
python -m uvicorn app.main:app

# Check port isn't already in use
lsof -i :8000
```

## 📝 Documentation

- **Project Planning**: [.cody/project/plan/](./cody/project/plan/)
  - [discovery.md](.cody/project/plan/discovery.md) - Initial requirements gathering
  - [prd.md](.cody/project/plan/prd.md) - Product requirements
  - [plan.md](.cody/project/plan/plan.md) - Implementation plan
  - [workflow_diagram.mmd](.cody/project/plan/workflow_diagram.mmd) - System architecture

- **Build Tracking**: [.cody/project/build/](./cody/project/build/)
  - [feature-backlog.md](.cody/project/build/feature-backlog.md) - All versions and features
  - [v0.1.0-environment-foundation/](.cody/project/build/v0.1.0-environment-foundation/) - Current version docs

- **Mock Data**: [app/data/README.md](app/data/README.md) - Data schemas and usage

## 🤝 Contributing

This is a learning project! Feel free to:
- Experiment with the code
- Add new tools or nodes
- Create additional mock data scenarios
- Extend the functionality

## 📄 License

This is an educational project for learning LangGraph concepts.

## 🙏 Acknowledgments

- **LangGraph** - For the amazing agent framework
- **LangChain** - For LLM abstractions
- **FastAPI** - For the web framework
- **Ollama** - For local LLM inference
- **Cody Framework** - For structured development approach

---

**Built with ❤️ for learning LangGraph**

*Generated with [Claude Code](https://claude.com/claude-code)*
