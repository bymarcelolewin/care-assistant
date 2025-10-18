# Product Implementation Plan
This document defines how the product will be built and when.

## Section Explanations
| Section                  | Overview |
|--------------------------|--------------------------|
| Overview                 | A brief recap of what we're building and the current state of the PRD. |
| Architecture             | High-level technical decisions and structure (e.g., frontend/backend split, frameworks, storage). |
| Components               | Major parts of the system and their roles. Think modular: what pieces are needed to make it work. |
| Data Model               | What data structures or models are needed. Keep it conceptual unless structure is critical. |
| Major Technical Steps    | High-level implementation tasks that guide development. Not detailed coding steps. |
| Tools & Services         | External tools, APIs, libraries, or platforms this app will depend on. |
| Risks & Unknowns         | Technical or project-related risks, open questions, or blockers that need attention. |
| Milestones    | Key implementation checkpoints or phases to show progress. |
| Environment Setup | Prerequisites or steps to get the app running in a local/dev environment. |

## Overview

This plan implements CARE (Coverage Analysis and Recommendation Engine) Assistant, a LangGraph learning application that demonstrates core LangGraph concepts through hands-on practice. The application will run entirely locally using Python, Ollama, and a simple web interface. It's designed as an educational tool that prioritizes code clarity and concept demonstration over production features.

## Architecture

**Architecture Pattern**: Monolithic local application with clear separation of concerns

**Visual Diagram**: See [workflow_diagram.mmd](workflow_diagram.mmd) for a detailed visual representation of the system architecture and flow.

**Tech Stack**:
- **Backend**: Python 3.10+ with FastAPI for serving REST API and static files
- **LLM Framework**: LangGraph + LangChain for agent orchestration
- **LLM**: Ollama (local inference, no external API calls)
- **Frontend**: React + Next.js 15 + TypeScript + shadcn/ui + react-draggable (static export)
- **Package Management**: uv for Python virtual environment and dependencies
- **Data Storage**: In-memory (JSON mock data loaded at startup)
- **State Management**: LangGraph's built-in state management + FastAPI session management (in-memory)

**System Flow**:
1. User opens web interface in browser (served from FastAPI static files)
2. Frontend sends messages to FastAPI backend via REST API (POST /api/chat)
3. Backend routes messages to LangGraph agent using session-based state management
4. Agent executes through graph nodes (identify user → orchestrator → generate response), calling tools as needed
5. Backend returns response with conversation, execution trace, and state
6. Frontend displays conversation in chat UI and execution details in collapsible developer panel

## Components

- **LangGraph Agent**: Core conversational agent built with nodes, edges, and state management. Demonstrates graph structure, LLM-based tool orchestration (eliminating manual intent classification), and multi-tool integration.

- **Tools Module**: Collection of callable functions for insurance operations (coverage lookup, benefit verification, claims status). Shows how to integrate external functionality with LangGraph.

- **Mock Data Service**: Provides simulated insurance plans, user profiles, and claims data. Demonstrates stateful data retrieval in conversational context.

- **State Manager**: Handles conversation state including user identity, conversation history, retrieved data, and execution trace. Core demonstration of LangGraph state management.

- **FastAPI Backend**: REST API server that handles HTTP requests (POST /api/chat), manages sessions, invokes the LangGraph agent, and serves the Next.js static build.

- **Web Interface**: Modern React + Next.js 15 + shadcn/ui frontend with chat UI and three independent draggable observability windows (Memory, Graph, Execution Steps). Shows conversation and execution trace with state visualization.

- **Session Manager**: Maintains conversation state across HTTP requests using in-memory sessions with unique session IDs.

- **Execution Trace System**: Captures and formats the agent's execution path through nodes and edges, including tool calls and state changes, for display in draggable observability windows.

## Data Model

**ConversationState** (LangGraph State):
- `messages`: List of conversation messages (user and assistant)
- `user_id`: Currently selected user profile (identified via natural language)
- `user_profile`: Full user insurance profile data
- `conversation_context`: Extracted entities and topics from conversation
- `tool_results`: Results from tool calls in current turn
- `execution_trace`: List of nodes visited and decisions made
- `first_greeting`: Boolean flag to prevent LLM from overriding welcome message

**UserProfile** (Mock Data):
- `user_id`: Unique identifier
- `name`: User's full name
- `insurance_plan`: Plan type (e.g., "PPO Gold", "HMO Silver")
- `coverage_details`: Dict of coverage types and limits
- `deductible`: Annual deductible amount
- `out_of_pocket_max`: Maximum out-of-pocket spending
- `claims_history`: List of past claims

**InsurancePlan** (Mock Data):
- `plan_id`: Unique identifier
- `plan_name`: Display name
- `plan_type`: PPO, HMO, EPO, etc.
- `monthly_premium`: Cost per month
- `coverage_details`: Detailed coverage information by category
- `network_info`: In-network vs out-of-network details

**ClaimRecord** (Mock Data):
- `claim_id`: Unique identifier
- `user_id`: Associated user
- `service_date`: When service was provided
- `service_type`: Type of medical service
- `claim_status`: Pending, Approved, Denied, etc.
- `billed_amount`: Provider's charge
- `covered_amount`: Insurance payment
- `patient_responsibility`: What user owes

## Major Technical Steps

1. **Environment Setup**: Initialize uv virtual environment, install dependencies (LangGraph, LangChain, FastAPI, etc.)

2. **Create Mock Data**: Design and implement JSON files with 3-5 user profiles, insurance plans, and claims records

3. **Build Core Tools**: Implement tools for coverage lookup, benefit verification, and claims status checking

4. **Define LangGraph State**: Create state schema with messages, user context, and execution tracking

5. **Build Graph Nodes**: Implement nodes for user identification, tool orchestration (LLM-based multi-tool coordinator), and response generation

6. **Connect Graph with Edges**: Define conditional edges for user identification; orchestrator uses LLM with tool binding to intelligently call multiple tools

7. **Integrate Ollama**: Set up LangChain's Ollama integration for local LLM calls

8. **Build FastAPI Backend**: Create REST endpoints for chat and user selection

9. **Implement Execution Tracking**: Capture node transitions and tool calls for visualization

10. **Create Web Interface**: Build simple HTML/CSS/JS chat UI with collapsible thinking process

11. **Add Code Documentation**: Write extensive inline comments explaining LangGraph concepts

12. **Test End-to-End**: Verify state persistence, multi-tool orchestration, LLM-based tool selection, and visualization

## Tools & Services

**Required**:

**Core LangGraph Packages**:
- **LangGraph**: The main framework we're learning. It provides the tools to build stateful, multi-step agent workflows using nodes, edges, and state management. This is the core of the entire application.
- **LangChain**: The foundational library that LangGraph is built on top of. It provides abstractions for working with LLMs (language models), prompts, and chains. LangGraph requires this as a dependency.
- **LangChain-Community**: Contains community-contributed integrations, including the Ollama integration we need to connect to the local LLM. Without this, we couldn't use Ollama with LangChain/LangGraph.

**Web Framework**:
- **FastAPI**: A modern, fast Python web framework for building APIs. We use this to create REST endpoints (POST /chat, GET /users) that the browser can call, and to serve our HTML/CSS/JS files. It's chosen for its simplicity and automatic API documentation.
- **Uvicorn**: An ASGI server that actually runs the FastAPI application. Think of FastAPI as the "recipe" and Uvicorn as the "kitchen" that executes it. You need both to run a web server.

**Data Validation**:
- **Pydantic**: Provides data validation and settings management using Python type annotations. LangGraph uses Pydantic models (or TypedDict) to define the state schema, ensuring our conversation state has the right structure and types. Unlike TypedDict which only provides type hints for static checkers, Pydantic validates data at runtime and catches errors early.

**Environment & Runtime**:
- **Python 3.10+**: Programming language
- **uv**: Fast Python package installer and virtual environment manager (already installed on user's machine)
- **Ollama**: Local LLM runtime for running language models entirely on the local machine without external API calls (already installed on user's machine)

**Optional/Development**:
- **httpx**: For testing API endpoints
- **pytest**: If adding unit tests later

## Risks & Unknowns

**Technical Risks**:
- **Ollama Model Performance**: Local models may be slower or less capable than cloud LLMs. Mitigation: Use smaller, faster models for learning purposes; set clear expectations.
- **LangGraph Learning Curve**: If the graph structure is too complex, it may confuse rather than educate. Mitigation: Start with simple linear flow, add complexity gradually with comments.
- **State Management Complexity**: Demonstrating state persistence clearly may require careful UI design. Mitigation: Show state changes explicitly in the thinking process view.

**Project Risks**:
- **Scope Creep**: Adding too many features could obscure learning objectives. Mitigation: Stick to PRD's out-of-scope list; prioritize clarity over features.
- **Mock Data Realism**: If data is too simple, it won't demonstrate realistic scenarios. Mitigation: Create 3-5 diverse profiles with varied coverage scenarios.

**Open Questions**:
- Which Ollama model should be recommended? (Need to balance size, speed, and capability)
- Should we include a graph visualization diagram, or is the execution trace sufficient?
- How detailed should the thinking process be? (Balance between educational value and information overload)

## Milestones

**Milestone 1: Environment & Foundation** (Version 0.1.0) - ✅ COMPLETED
- Virtual environment set up with uv
- All dependencies installed (LangGraph, LangChain, FastAPI, Uvicorn, Pydantic)
- Mock data files created (users.json, plans.json, claims.json)
- Basic FastAPI server running with health check endpoint
- Ollama connection verified

**Milestone 2: Core Agent** (Version 0.2.0) - ✅ COMPLETED
- LangGraph state defined (ConversationState with TypedDict)
- All three tools implemented (coverage lookup, benefit verification, claims status)
- Graph with 4 nodes (identify user, orchestrator, generate response, conditional routing)
- LLM-based orchestrator for multi-tool scenarios
- Agent can execute conversational flow with state persistence
- Interactive CLI testing tool with trace/state commands

**Milestone 3: Web Interface** (Version 0.3.0) - ✅ COMPLETED
- React + Next.js 15 + TypeScript + shadcn/ui chat interface
- FastAPI serves static frontend and handles chat API (POST /api/chat)
- Session-based state management across HTTP requests
- Conversational user identification with LLM-powered name extraction
- Personalized welcome messages with member-since date
- VS Code-style developer panel with execution trace and state visualization
- Production build working with static export
- User can send messages and receive responses
- Full execution tracking visible in developer panel

**Milestone 4: Observability Enhancements** (Version 0.4.0) - ✅ COMPLETED
- Rebranded Developer Panel to "Observability"
- Improved terminology (State → Memory, Execution Trace → Execution Steps)
- User prompts displayed alongside execution steps
- Smart grouping of traces by triggering message
- Enhanced tab styling for better UX
- Fixed tool results display bug in Memory tab

**Milestone 5: UI Improvements** (Version 0.5.0) - ✅ COMPLETED
- Redesigned chat window with contained layout
- Modernized input field with integrated send button
- Enhanced message bubbles with custom styling
- Animated thinking indicator
- Improved spacing and visual hierarchy
- Better header alignment

**Milestone 6: Project Structure Reorganization** (Version 0.6.0) - ✅ COMPLETED
- Moved JSON data files to root-level /data folder
- Clear separation between data files and data-handling code
- Updated loader.py path resolution
- Comprehensive testing and documentation updates
- Zero breaking changes to public API

**Milestone 7: Observability Windows** (Version 0.7.0) - ✅ COMPLETED
- Removed bottom observability panel from chat window
- Created three independent draggable windows (Memory, Graph, Execution Steps)
- Added checkbox controls in header for showing/hiding windows
- Implemented centered default positioning
- Added z-index management for window layering
- Real-time updates for all three windows
- Improved observability UX with separate, movable panels

**Milestone 8: LangSmith Observability** (Version 0.8.0) - ✅ COMPLETED
- Integrated LangSmith for cloud-based tracing and monitoring
- Added environment variable configuration (.env file)
- Implemented custom trace metadata (session_id, user_id, environment)
- Added offline resilience and graceful degradation
- Token tracking via LangSmith callbacks
- Comprehensive documentation and setup guide
- Optional feature - app works perfectly without it

**Milestone 9: Enhanced Learning Features** (Version 1.0.0) - PLANNED
- Conditional routing working
- State persistence demonstrated across turns
- Thinking process fully visible in separate windows
- Code thoroughly commented
- README with usage instructions

## Environment Setup

**Prerequisites** (assumed already installed):
1. Python 3.10 or higher
2. uv package manager
3. Ollama with at least one model (recommended: llama3.2 or mistral)

**Setup Steps**:

1. **Create virtual environment with uv**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   uv pip install langgraph langchain langchain-community fastapi uvicorn pydantic
   ```

3. **Verify Ollama is running**:
   ```bash
   ollama list  # Should show installed models
   ```

4. **Create project structure**:
   ```
   /app
     /data          # Data loader module (Python code)
     /tools         # Tool implementations
     /graph         # LangGraph nodes and edges
     /api           # FastAPI endpoints
     main.py        # Entry point
   /data            # Mock JSON data files (root level)
   /frontend        # Next.js web interface
   ```

5. **Run the application**:
   ```bash
   python app/main.py
   # or
   uvicorn app.main:app --reload
   ```

6. **Access the interface**:
   Open browser to `http://localhost:8000`
