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

## Version 0.2.0 - Core Agent - 🟢 Completed
Build the core LangGraph agent with state management, tools, and basic conversation flow.

| ID  | Feature                 | Description                              | Priority | Status |
|-----|-------------------------|------------------------------------------|----------|--------|
| V2-1 | LangGraph State Schema | Define ConversationState with messages, user context, tool results, and execution trace | High | 🟢 Completed |
| V2-2 | Coverage Lookup Tool | Implement tool to query user's coverage details from mock data | High | 🟢 Completed |
| V2-3 | Benefit Verification Tool | Implement tool to check if specific services are covered | High | 🟢 Completed |
| V2-4 | Claims Status Tool | Implement tool to retrieve claims history and status | Medium | 🟢 Completed |
| V2-5 | Identify User Node | Create node that identifies or confirms user identity by name (conversational) | High | 🟢 Completed |
| V2-6 | LLM-Based Orchestrator Node | Create node that uses LLM to intelligently select and call multiple tools | High | 🟢 Completed |
| V2-7 | Generate Response Node | Create node that generates conversational response using LLM and tool results | High | 🟢 Completed |
| V2-8 | Connect Graph Edges | Define edges connecting nodes, including conditional routing for user identification | High | 🟢 Completed |
| V2-9 | Ollama Integration | Integrate LangChain's Ollama LLM for node operations | High | 🟢 Completed |
| V2-10 | Interactive CLI Testing | Build interactive CLI with trace/state commands for testing | High | 🟢 Completed |
| V2-11 | Execution Trace System | Implement detailed execution tracking for learning and debugging | High | 🟢 Completed |

## Version 0.3.0 - Web Interface - 🟢 Completed
Create a modern web-based user interface for interacting with the agent using shadcn/ui components. Maintains all v0.2.0 functionality (LLM-based orchestration, multi-tool handling, conversational user identification, execution traces) with polished UX.

**Completion Date:** October 15, 2025
**Tech Stack:** React + Next.js 15 + TypeScript + shadcn/ui + Tailwind CSS
**UI Design:** Main chat window + collapsible developer panel (VS Code terminal style) for trace/state visualization
**Total Tasks:** 58 tasks completed (see tasklist.md for full breakdown)

| ID  | Feature                 | Description                              | Priority | Status |
|-----|-------------------------|------------------------------------------|----------|--------|
| V3-1 | Next.js Project Setup | Initialize Next.js project with TypeScript, install shadcn/ui components and dependencies | High | 🟢 Completed |
| V3-2 | Chat UI with shadcn/ui | Build chat interface using shadcn/ui components (Card, ScrollArea, Input, Button) | High | 🟢 Completed |
| V3-3 | Conversational User Identification | AI greets with "What's your name?" - user types name (matching CLI behavior from v0.2.0) | High | 🟢 Completed |
| V3-4 | Message Send/Receive | Implement message submission and real-time response display with streaming support | High | 🟢 Completed |
| V3-5 | Developer Panel UI | Create VS Code-style bottom panel for trace + state visualization (collapsible) | High | 🟢 Completed |
| V3-6 | Execution Trace Display | Display execution trace in developer panel using shadcn/ui components (Tabs, Collapsible, Badge) | Medium | 🟢 Completed |
| V3-7 | State Visualization | Show current conversation state in developer panel (user profile, tool results, context) | Medium | 🟢 Completed |
| V3-8 | POST /chat Endpoint | Create FastAPI endpoint that accepts messages, invokes agent, returns response + trace + state | High | 🟢 Completed |
| V3-9 | WebSocket Streaming (Optional) | Implement WebSocket for streaming LLM responses token-by-token | Medium | ⚪ Skipped (not needed) |
| V3-10 | Session Management | Maintain conversation state across HTTP requests using session IDs | High | 🟢 Completed |
| V3-11 | Static Frontend Serving | Configure FastAPI to serve Next.js build output | High | 🟢 Completed |
| V3-12 | Multi-Tool Response Display | Properly display responses from multiple tool calls in single turn | High | 🟢 Completed |
| V3-13 | Error Handling UI | User-friendly error messages when Ollama fails or tools error | Medium | 🟢 Completed |
| V3-14 | Loading States | Show loading indicators during LLM processing and tool execution | Medium | 🟢 Completed |
| V3-15 | End-to-End Web Test | Test complete flow: name entry → conversation → tool calls → trace visibility | High | 🟢 Completed |
| V3-16 | LLM Name Extraction | Use LLM with structured output to extract names from natural language ("I'm Marcelo, your patient") | High | 🟢 Completed |
| V3-17 | Personalized Welcome | Include member-since date in welcome message | High | 🟢 Completed |
| V3-18 | CARE Assistant Branding | Add ❤️ emoji to branding | Medium | 🟢 Completed |
| V3-19 | First Greeting Flag | Prevent LLM from overriding welcome message | High | 🟢 Completed |

## Version 0.4.0 - Observability Enhancements - 🟢 Completed
Improve the developer panel with better terminology and enhanced trace visibility by showing user prompts alongside execution steps.

| ID  | Feature                 | Description                              | Priority | Status |
|-----|-------------------------|------------------------------------------|----------|--------|
| V4-1 | Rename Developer Panel | Change panel title from "🔧 Developer Panel" to "🔍 Observability" | High | 🟢 Completed |
| V4-2 | Rename State Tab | Change "State" tab label to "Memory" | High | 🟢 Completed |
| V4-3 | Rename Execution Trace Tab | Change "Execution Trace" tab label to "Execution Steps" | High | 🟢 Completed |
| V4-4 | Add User Prompt Display | Show user messages that triggered execution steps in trace view | High | 🟢 Completed |
| V4-5 | Group Trace by Message | Group execution steps by the user message that triggered them | High | 🟢 Completed |
| V4-6 | Visual Prompt Styling | Use darker background color to distinguish prompts from execution steps | Medium | 🟢 Completed |
| V4-7 | Tab Styling Improvements | Make active tabs more visually distinct with darker background and white text, subtle rounded corners | High | 🟢 Completed |
| V4-8 | Fix Tool Results Display | Investigate and fix why tool results are not showing in Memory (State) tab | High | 🟢 Completed |

## Version 0.5.0 - UI Improvements AI Chatbot - 🟢 Completed
Redesign the chat window UI for a more cohesive and polished user experience with better spacing, contained layout, and modernized input design.

**Completion Date:** October 16, 2025
**Reference Design:** `.cody/project/library/assets/Chat Window UX.png`
**Scope:** Chat window only (Observability panel updates deferred to future version)
**Total Tasks:** 21 tasks completed across 5 phases (see tasklist.md for full breakdown)

| ID  | Feature                 | Description                              | Priority | Status |
|-----|-------------------------|------------------------------------------|----------|--------|
| V5-1 | Outer Container Border | Add gray rounded border around entire chat window for cohesive contained experience | High | 🟢 Completed |
| V5-2 | Inner Padding | Add buffer/padding between chat content and outer border on all sides | High | 🟢 Completed |
| V5-3 | Message Bubble Spacing | Increase left/right margins so messages don't go edge-to-edge within chat area | High | 🟢 Completed |
| V5-4 | Input Field Redesign | Redesign input field with background color and stroke/border matching design | High | 🟢 Completed |
| V5-5 | Send Button Inside Input | Move send button inside the input field on the right side | High | 🟢 Completed |
| V5-6 | Remove Input Separator | Remove border-top line between messages area and input area | High | 🟢 Completed |
| V5-7 | Thinking Indicator | Add animated "thinking" indicator when AI is processing user messages | High | 🟢 Completed |
| V5-8 | Message Bubble Styling | Custom rounded corners and lighter colors for message bubbles | High | 🟢 Completed |
| V5-9 | Header Alignment | Align header elements with input box edges | High | 🟢 Completed |

## Version 0.6.0 - Move Data Folder to Root - 🔴 Not Started
Reorganize project structure by moving JSON data files to a root-level data folder for easier maintenance and clearer separation between data files and data-handling code.

**Scope:** Move `*.json` files from `/app/data/` to new `/data/` folder at root level, update all code references, and update documentation.

| ID  | Feature                 | Description                              | Priority | Status |
|-----|-------------------------|------------------------------------------|----------|--------|
| V6-1 | Create Root Data Folder | Create new `/data` folder at project root level | High | 🔴 Not Started |
| V6-2 | Move JSON Files | Move users.json, plans.json, and claims.json from `/app/data/` to `/data/` | High | 🔴 Not Started |
| V6-3 | Update Data Loader Code | Update code in `/app/data/` that loads JSON files to reference new location | High | 🔴 Not Started |
| V6-4 | Update Import Paths | Update all import statements and file path references throughout codebase | High | 🔴 Not Started |
| V6-5 | Test Data Loading | Verify all JSON files load correctly from new location | High | 🔴 Not Started |
| V6-6 | Update Documentation | Update README and any other docs to reflect new project structure | Medium | 🔴 Not Started |
| V6-7 | End-to-End Testing | Test complete application flow to ensure no broken references | High | 🔴 Not Started |

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
