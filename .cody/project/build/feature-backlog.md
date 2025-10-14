# Feature Backlog

This document lists features and enhancements derived from the plan. It is a living document that will evolve throughout the project. It is grouped by version, with the Backlog tracking all features not added to a version yet. It is used to create versions to work on.

| Status |  | Priority |  |
|--------|-------------|---------|-------------|
| 🔴 | Not Started | High | High priority items |
| 🟡 | In Progress | Medium | Medium priority items |
| 🟢 | Completed | Low | Low priority items |


## Backlog

| ID  | Feature             | Description                               | Priority | Status |
|-----|---------------------|-------------------------------------------|----------|--------|
| BL-1 | Advanced Graph Patterns | Add parallel execution, sub-graphs, or complex conditional branching for advanced learners | Low | 🔴 Not Started |
| BL-2 | Multi-Model Support | Support for OpenAI, Anthropic, or other LLM providers beyond Ollama | Low | 🔴 Not Started |
| BL-3 | Persistent Storage | Save conversation history to disk for session recovery | Low | 🔴 Not Started |
| BL-4 | Unit Tests | Add pytest tests for tools, nodes, and state management | Medium | 🔴 Not Started |
| BL-5 | Graph Visualization Diagram | Visual diagram showing the agent's graph structure | Medium | 🔴 Not Started |

## Version 0.1.0 - Environment & Foundation - 🟢 Completed
Set up the development environment, dependencies, and foundational data structures.

| ID  | Feature                 | Description                              | Priority | Status |
|-----|-------------------------|------------------------------------------|----------|--------|
| V1-1 | Virtual Environment Setup | Create virtual environment using uv and activate it | High | 🟢 Completed |
| V1-2 | Dependency Installation | Install LangGraph, LangChain, FastAPI, Uvicorn, Pydantic, and other required packages | High | 🟢 Completed |
| V1-3 | Project Structure | Create project folder structure (app/, data/, tools/, graph/, api/, static/) | High | 🟢 Completed |
| V1-4 | Mock User Profiles | Create JSON file with 3 diverse user profiles with different insurance plans | High | 🟢 Completed |
| V1-5 | Mock Insurance Plans | Create JSON file with various insurance plan types (PPO, HMO, etc.) and coverage details | High | 🟢 Completed |
| V1-6 | Mock Claims Data | Create JSON file with sample claims records for different users | High | 🟢 Completed |
| V1-7 | Basic FastAPI Server | Set up minimal FastAPI application with health check endpoint | High | 🟢 Completed |
| V1-8 | Verify Ollama Connection | Test connection to local Ollama instance and list available models | High | 🟢 Completed |

## Version 0.2.0 - Core Agent - 🔴 Not Started
Build the core LangGraph agent with state management, tools, and basic conversation flow.

| ID  | Feature                 | Description                              | Priority | Status |
|-----|-------------------------|------------------------------------------|----------|--------|
| V2-1 | LangGraph State Schema | Define ConversationState with messages, user context, tool results, and execution trace | High | 🔴 Not Started |
| V2-2 | Coverage Lookup Tool | Implement tool to query user's coverage details from mock data | High | 🔴 Not Started |
| V2-3 | Benefit Verification Tool | Implement tool to check if specific services are covered | High | 🔴 Not Started |
| V2-4 | Claims Status Tool | Implement tool to retrieve claims history and status | Medium | 🔴 Not Started |
| V2-5 | Identify User Node | Create node that identifies or confirms user identity | High | 🔴 Not Started |
| V2-6 | Classify Intent Node | Create node that determines user's intent using LLM | High | 🔴 Not Started |
| V2-7 | Route to Tool Node | Create node that routes to appropriate tool based on intent | High | 🔴 Not Started |
| V2-8 | Generate Response Node | Create node that generates conversational response using LLM | High | 🔴 Not Started |
| V2-9 | Connect Graph Edges | Define edges connecting nodes, including conditional routing | High | 🔴 Not Started |
| V2-10 | Ollama Integration | Integrate LangChain's Ollama LLM for node operations | High | 🔴 Not Started |
| V2-11 | Basic Conversation Test | Test agent with simple conversation flow in CLI or script | High | 🔴 Not Started |

## Version 0.3.0 - Web Interface - 🔴 Not Started
Create the web-based user interface for interacting with the agent.

| ID  | Feature                 | Description                              | Priority | Status |
|-----|-------------------------|------------------------------------------|----------|--------|
| V3-1 | Chat UI Layout | Build HTML/CSS layout with message display and input field | High | 🔴 Not Started |
| V3-2 | User Selection Dropdown | Add UI element to select which mock user profile to use | High | 🔴 Not Started |
| V3-3 | Message Send/Receive | Implement JavaScript to send messages and display responses | High | 🔴 Not Started |
| V3-4 | POST /chat Endpoint | Create FastAPI endpoint that accepts messages and invokes agent | High | 🔴 Not Started |
| V3-5 | GET /users Endpoint | Create endpoint to retrieve list of available user profiles | Medium | 🔴 Not Started |
| V3-6 | Static File Serving | Configure FastAPI to serve HTML/CSS/JS files | High | 🔴 Not Started |
| V3-7 | Basic Execution Tracking | Capture and return basic execution trace (nodes visited) | Medium | 🔴 Not Started |
| V3-8 | Collapsible Thinking View | Add collapsible section to display execution trace | Medium | 🔴 Not Started |
| V3-9 | End-to-End Web Test | Test complete flow from browser through agent and back | High | 🔴 Not Started |

## Version 1.0.0 - Enhanced Learning Features - 🔴 Not Started
Polish the application with enhanced visibility, documentation, and learning features.

| ID  | Feature                 | Description                              | Priority | Status |
|-----|-------------------------|------------------------------------------|----------|--------|
| V4-1 | Enhanced Execution Trace | Show detailed node transitions, tool calls, and state changes | High | 🔴 Not Started |
| V4-2 | State Visualization | Display current conversation state in thinking process view | High | 🔴 Not Started |
| V4-3 | Conditional Routing Demo | Ensure different intents trigger different execution paths visibly | High | 🔴 Not Started |
| V4-4 | Code Comments & Documentation | Add extensive inline comments explaining LangGraph concepts | High | 🔴 Not Started |
| V4-5 | README with Instructions | Write comprehensive README with setup, usage, and learning guide | High | 🔴 Not Started |
| V4-6 | Tool Call Visibility | Highlight when and why tools are called in the execution trace | High | �4 Not Started |
| V4-7 | Conversation History Display | Show full conversation history with state context | Medium | 🔴 Not Started |
| V4-8 | Error Handling | Add basic error handling and user-friendly error messages | Medium | 🔴 Not Started |
| V4-9 | Extension Guide | Add comments or documentation on how to add new tools or nodes | Medium | 🔴 Not Started |
| V4-10 | Final Testing | Comprehensive test of all learning objectives and success criteria | High | 🔴 Not Started |
