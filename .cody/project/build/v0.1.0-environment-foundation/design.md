# Version Design Document : Version 0.1.0 - Environment & Foundation
Technical implementation and design guide for the upcoming version.

## 1. Features Summary
_Overview of features included in this version._

This version establishes the development environment and foundational infrastructure for the LangGraph learning application. It includes:

- **V1-1**: Virtual Environment Setup - Create isolated Python environment using uv
- **V1-2**: Dependency Installation - Install all required packages (LangGraph, LangChain, FastAPI, etc.)
- **V1-3**: Project Structure - Create organized folder structure for the application
- **V1-4**: Mock User Profiles - Generate realistic insurance user data (3-5 profiles)
- **V1-5**: Mock Insurance Plans - Create various plan types with coverage details
- **V1-6**: Mock Claims Data - Generate sample claims records for testing
- **V1-7**: Basic FastAPI Server - Set up minimal web server with health check
- **V1-8**: Verify Ollama Connection - Confirm local LLM is accessible

## 2. Technical Architecture Overview
_High-level technical structure that supports all features in this version._

**Environment**:
- Python 3.10+ virtual environment managed by `uv`
- Local package installation (no global dependencies)
- All code runs locally without external API calls

**Project Structure**:
```
/app
  /data          # Mock JSON files (users, plans, claims)
  /tools         # Tool implementations (will be built in v0.2.0)
  /graph         # LangGraph nodes and edges (will be built in v0.2.0)
  /api           # FastAPI endpoints (basic setup in this version)
  /static        # HTML/CSS/JS frontend (will be built in v0.3.0)
  main.py        # Application entry point
```

**Dependencies**:
- **LangGraph + LangChain**: Agent framework and LLM abstractions
- **LangChain-Community**: Ollama integration
- **FastAPI + Uvicorn**: Web server and ASGI runtime
- **Pydantic**: Data validation (used by LangGraph for state)

**Mock Data Storage**:
- JSON files in `/app/data/` directory
- Loaded into memory at application startup
- No database or persistence layer in this version

## 3. Implementation Notes
_Shared technical considerations across all features in this version._

**Virtual Environment (uv)**:
- Use `uv venv` to create environment
- Activate with `source .venv/bin/activate` (macOS/Linux)
- Install packages with `uv pip install <package>`
- uv is faster than pip and handles dependency resolution well

**Mock Data Design**:
- **User Profiles**: Include varied demographics, plan types, and coverage scenarios
  - Exactly 3 diverse profiles
  - Different insurance plan types (PPO, HMO, EPO)
  - Varied deductibles and out-of-pocket maximums
- **Insurance Plans**: Simple but realistic coverage details by category (5-7 main categories)
- **Claims Data**: Mix of pending, approved, and denied claims with realistic dates and amounts

**FastAPI Setup**:
- Minimal server for this version (just health check endpoint)
- Structure allows easy expansion in future versions
- Use `uvicorn app.main:app --reload` for development

**Ollama Verification**:
- Check that Ollama is running locally
- Use llama3.3:70b-instruct-q4_K_S (primary) or llama3.2:latest (fallback)
- Test LangChain's Ollama integration works

## 4. Other Technical Considerations
_Shared any other technical information that might be relevant to building this version._

**Code Organization**:
- Keep code well-commented from the start (learning-focused application)
- Use type hints throughout for clarity
- Follow Python conventions (PEP 8)

**Mock Data Realism**:
- Data should be realistic enough to demonstrate meaningful scenarios
- Include edge cases (high deductibles, partial coverage, denied claims)
- Balance between simplicity (for learning) and realism (for demonstration)

**Development Workflow**:
- Test each component as it's built
- Verify Ollama connection before moving to next version
- Ensure FastAPI server runs without errors

**File Naming**:
- Use lowercase with underscores: `user_profiles.json`, `insurance_plans.json`, `claims_data.json`
- Keep imports organized: standard library → third-party → local

## 5. Design Decisions
_Resolved technical and product decisions for this version._

1. **Ollama Model: llama3.3:70b-instruct-q4_K_S**
   - More capable for conversational responses and tool calling
   - Quantized version (q4_K_S) keeps reasonable performance
   - Better for POC demonstrations
   - Fallback option: llama3.2:latest if performance issues

2. **Mock User Profiles: 3 profiles**
   - Sufficient to demonstrate variety without complexity
   - Each profile will have distinct insurance plan and coverage scenario
   - Good balance for POC purposes

3. **Mock Data Detail Level: Simple but realistic**
   - 5-7 main coverage categories to keep manageable
   - Realistic dollar amounts and coverage percentages
   - Focus on clarity for learning and POC demonstration
   - Include 1-2 edge cases per profile for interest

4. **Project Location: app/ subdirectory**
   - Keeps code organized and separate from Cody framework files
   - All application code lives in app/ folder
   - Clear separation of concerns

5. **Platform: macOS**
   - All shell commands will use macOS/Unix conventions
   - Virtual environment activation: `source .venv/bin/activate`
