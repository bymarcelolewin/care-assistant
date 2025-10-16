# Release Notes

This document lists new features, bug fixes, and other changes implemented during a particular build, also known as a version.

## Table of Contents
- [v0.3.0 - Web Interface](#v030---web-interface---october-15-2025)
- [v0.2.0 - Core Agent](#v020---core-agent)
- [v0.1.0 - Environment & Foundation](#v010---environment--foundation)

---

# v0.3.0 - Web Interface - October 15, 2025

## Overview
This version transforms the CARE Assistant from a CLI-only application into a modern, production-ready web application with a professional UI built using React, Next.js 15, TypeScript, and shadcn/ui components. All v0.2.0 functionality (LLM-based orchestration, multi-tool handling, conversational user identification) is maintained while adding a polished web interface with developer tooling.

## Key Features
- **Modern Web Interface**: React + Next.js 15 + TypeScript + shadcn/ui chat interface with professional design
- **Developer Panel**: VS Code-style collapsible panel showing execution trace and state visualization
- **Conversational User Identification**: LLM-powered natural language name extraction (e.g., "I'm Marcelo, your patient")
- **Personalized Welcome**: Welcome messages include member-since date and ❤️ CARE Assistant branding
- **Session Management**: Maintains conversation state across HTTP requests using in-memory sessions
- **Static Export Deployment**: Single FastAPI server serves Next.js static build (production-ready)
- **REST API**: POST /api/chat endpoint for chat interactions with execution trace and state

## Enhancements
- **First Greeting Flag**: Prevents LLM from overriding personalized welcome messages
- **Error Handling UI**: User-friendly error messages when Ollama fails or tools error
- **Loading States**: Loading indicators during LLM processing and tool execution
- **Multi-Tool Response Display**: Properly displays responses from multiple tool calls in single turn
- **Hot-Reload Development**: Separate development and production modes for better DX

## Bug Fixes
- Fixed TypeScript type mismatches between frontend and backend (`UserProfile` interface)
- Fixed async/await issues by using `ainvoke` instead of `invoke`
- Fixed welcome message being overridden by LLM responses
- Replaced `any` types with `unknown` for better type safety
- Removed unused imports and variables

## Other Notes
- Total of 58 tasks completed across 8 phases
- Updated README with production vs dev instructions
- Comprehensive retrospective document created for lessons learned
- Application is now production-ready for local deployment

---

# v0.2.0 - Core Agent

## Overview
This version implements the core LangGraph agent with state management, tools, and conversational flow. It demonstrates key LangGraph concepts including nodes, edges, conditional routing, and LLM-based tool orchestration.

## Key Features
- **LangGraph State Schema**: ConversationState with messages, user context, tool results, and execution trace
- **Tool Integration**: Three tools implemented (coverage lookup, benefit verification, claims status)
- **LLM-Based Orchestrator**: Intelligent multi-tool coordinator that uses LLM to decide which tools to call
- **Graph Structure**: 4 nodes (identify user, orchestrator, generate response) with conditional routing
- **Ollama Integration**: Local LLM integration using LangChain's Ollama connector
- **Interactive CLI Testing**: CLI tool with trace/state commands for testing and debugging
- **Execution Trace System**: Detailed execution tracking for learning and debugging

## Enhancements
- Conversational user identification by name (no dropdown menus)
- State persistence across conversation turns
- Conditional edge routing based on user identification status
- Extensive code comments explaining LangGraph concepts

## Bug Fixes
None

## Other Notes
- Successfully eliminated manual intent classification in favor of LLM-based tool selection
- CLI provides excellent visibility into agent execution for learning purposes

---

# v0.1.0 - Environment & Foundation

## Overview
This version establishes the development environment, dependencies, and foundational data structures for the CARE Assistant application.

## Key Features
- **Virtual Environment**: Created and configured using uv package manager
- **Dependency Installation**: LangGraph, LangChain, LangChain-Community, FastAPI, Uvicorn, Pydantic installed
- **Project Structure**: Created app/, data/, tools/, graph/, api/ folder structure
- **Mock Data**: Created JSON files with diverse user profiles, insurance plans, and claims data
  - users.json: 3 user profiles with different insurance plans
  - plans.json: Various insurance plan types (PPO, HMO, etc.)
  - claims.json: Sample claims records
- **Basic FastAPI Server**: Minimal FastAPI application with health check endpoint
- **Ollama Verification**: Confirmed connection to local Ollama instance

## Enhancements
None (initial version)

## Bug Fixes
None (initial version)

## Other Notes
- All prerequisites verified (Python 3.10+, uv, Ollama)
- Foundation ready for core agent development
