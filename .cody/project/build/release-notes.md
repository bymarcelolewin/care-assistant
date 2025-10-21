# Release Notes

This document lists new features, bug fixes, and other changes implemented during a particular build, also known as a version.

## Table of Contents
- [v0.9.0 - Migrate to LangChain 1.0 & LangGraph 1.0](#v090---migrate-to-langchain-10--langgraph-10---october-21-2025)
- [v0.8.0 - Add LangSmith Observability](#v080---add-langsmith-observability---october-18-2025)
- [v0.7.0 - Move Observability to Pop-up Window](#v070---move-observability-to-pop-up-window---october-17-2025)
- [v0.6.1 - Code Cleanup and Graph View](#v061---code-cleanup-and-graph-view---october-16-2025)
- [v0.6.0 - Move Data Folder to Root](#v060---move-data-folder-to-root---october-16-2025)
- [v0.5.0 - UI Improvements AI Chatbot](#v050---ui-improvements-ai-chatbot---october-16-2025)
- [v0.4.0 - Observability Enhancements](#v040---observability-enhancements---october-16-2025)
- [v0.3.0 - Web Interface](#v030---web-interface---october-15-2025)
- [v0.2.0 - Core Agent](#v020---core-agent)
- [v0.1.0 - Environment & Foundation](#v010---environment--foundation)

---

# v0.9.0 - Migrate to LangChain 1.0 & LangGraph 1.0 - October 21, 2025

## Overview
This version upgrades the CARE Assistant to use the new stable 1.0 releases of LangChain and LangGraph. The migration was remarkably smooth with **zero breaking changes** required in our codebase, demonstrating that we were already following v1.0 best practices.

## Upgrade Details
- **LangChain**: 0.3.27 → 1.0.2 (stable)
- **LangGraph**: 0.6.10 → 1.0.1 (stable)
- **langchain-core**: 0.3.79 → 1.0.0
- **langchain-community**: 0.3.31 → 0.4
- **langchain-ollama**: 0.3.10 → 1.0.0
- **langchain-text-splitters**: 0.3.11 → 1.0.0
- **langgraph-checkpoint**: 2.1.2 → 3.0.0
- **langgraph-prebuilt**: 0.6.4 → 1.0.1

## Key Features
- **Stable 1.0 Release**: Now using production-stable versions with stability promise (no breaking changes until 2.0)
- **Backward Compatibility Package**: `langchain-classic` 1.0.0 automatically installed for legacy support
- **Zero Code Changes**: No modifications required to existing codebase - only version number updates in documentation
- **Python 3.13 Compatible**: Exceeds minimum requirement (3.10+)

## Enhancements
- **Future-Proof Architecture**: Built on stable foundation with long-term support commitment
- **New Features Available**: v1.0 introduces Content Blocks API, enhanced middleware, and improved structured output (available for future exploration)
- **Automatic Dependency Updates**: Related packages (langsmith, pydantic, numpy) automatically updated to compatible versions

## Technical Changes
- **Dependencies Updated**:
  - All langchain packages upgraded to 1.x
  - All langgraph packages upgraded to 1.x/3.x
  - Companion packages automatically updated (langsmith 0.4.34 → 0.4.37, pydantic 2.12.2 → 2.12.3, numpy 2.3.3 → 2.3.4)

- **Files Modified**:
  - `README.md` - Updated version badge (0.8.0 → 0.9.0), architecture section (added v1.0.x versions), installation notes
  - `.cody/project/build/feature-backlog.md` - Added v0.9.0 entry with migration tasks

- **No Code Changes**:
  - ✅ All imports still work (langchain_core, langchain_ollama, langgraph)
  - ✅ StateGraph compilation successful
  - ✅ TypedDict state definition compatible
  - ✅ No `.text()` method usage to fix
  - ✅ No deprecated features in use

## Compatibility Verification
- ✅ **Python Version**: 3.13.3 confirmed (exceeds 3.10+ requirement)
- ✅ **Virtual Environment**: All packages correctly installed in `.venv`
- ✅ **Import Tests**: All langchain/langgraph imports successful
- ✅ **Agent Compilation**: LangGraph agent compiles without errors
- ✅ **Backend Initialization**: Data loading and FastAPI startup working
- ✅ **No Breaking Changes**: Zero code modifications required

## Testing
- ✓ Phase 1: Preparation completed (Python version, breaking change search)
- ✓ Phase 2: All 5 packages upgraded successfully
- ✓ Phase 3: Code compatibility verified (imports, state, no .text() usage)
- ✓ Phase 4: Backend tests passed (agent compilation, data loading)
- ✓ Phase 5: Documentation updated (README, release notes, retrospective)
- ✓ Phase 6: Final verification pending user manual testing

## Migration Notes
- **Zero Breaking Changes**: Codebase was already v1.0-compatible
- **No Rollback Needed**: Migration completed successfully on first attempt
- **UV Package Manager**: Automatically detected and used `.venv` virtual environment
- **Total Duration**: ~45 minutes from start to completion
- **Risk Level**: Low (as predicted) - actually zero issues encountered

## Known Items
- **Deprecation Warning**: `tests/test_ollama.py` uses deprecated `Ollama` class - update to `from langchain_ollama import OllamaLLM` in future version
- **Ollama Server**: Tests requiring live Ollama connection skipped (expected)

## Why This Migration Was Smooth
Our proactive architecture decisions made this migration seamless:
1. **TypedDict State**: Already using recommended state pattern
2. **Custom StateGraph**: Building custom graph instead of using prebuilt agents
3. **Modern Imports**: Using `langchain_core` imports from the start
4. **No Legacy Features**: Avoided deprecated chains and hub functionality
5. **Best Practices**: Following LangChain/LangGraph documentation from day one

## Future Enhancements
v1.0 introduces new features for exploration in future versions:
- **Content Blocks API**: Standardized access to reasoning and content
- **Enhanced Middleware**: Better reusability across agents
- **New Structured Output**: `ToolStrategy` and `ProviderStrategy` classes
- **Stability Promise**: No breaking changes until 2.0 release

## Other Notes
- Comprehensive planning documentation created (`.cody/project/build/v0.9.0-migrate-to-langchain-langgraph-1.0/`)
- Detailed retrospective captures lessons learned for future migrations
- 24 tasks completed across 6 phases (21 by AGENT, 3 by USER)
- Feature backlog updated with v0.9.0 status

---

# v0.8.0 - Add LangSmith Observability - October 18, 2025

## Overview
This version integrates **LangSmith**, LangChain's official cloud-based observability platform, providing professional-grade tracing, debugging, and monitoring for the LangGraph agent. LangSmith is completely optional - the app works perfectly without it, making it ideal for learning production-ready patterns without requiring external dependencies.

## Key Features
- **Cloud-Based Tracing**: All LangGraph executions, LLM calls, and tool invocations automatically traced to LangSmith dashboard
- **Custom Metadata**: Traces include session_id, user_id, and environment tags for easy filtering
- **Offline Resilience**: App continues working normally if LangSmith is unreachable (network down, invalid key, etc.)
- **Token Tracking**: LangSmith automatically tracks input/output tokens via callbacks
- **Optional Feature**: Complete graceful degradation - works with or without LangSmith account
- **Secure Configuration**: API keys stored in `.env` file (git-ignored)

## Enhancements
- **Dual Observability**: Students can compare local draggable windows with cloud-based LangSmith traces
- **Startup Status Logging**: Clear messages indicate if LangSmith is enabled/disabled
- **Comprehensive Documentation**: 
  - Complete setup guide (`.cody/project/library/docs/langsmith-setup.md`)
  - README updates with prerequisites, installation, and troubleshooting
  - Security best practices emphasized throughout
- **Environment Template**: `.env.example` provides clear template with comments

## Technical Changes
- **Dependencies Added**:
  - `langsmith` - LangSmith SDK for Python
  - `python-dotenv` - Environment variable management

- **Files Modified**:
  - `app/main.py` - Added environment loading and LangSmith status logging
  - `app/api/chat.py` - Added trace metadata and offline error handling
  - `.gitignore` - Refined to allow `.env.example` while ignoring `.env`
  - `README.md` - Added LangSmith sections (prerequisites, installation, troubleshooting)

- **Files Created**:
  - `.env.example` - Environment variable template (safe to commit)
  - `.env` - Actual configuration with API key (git-ignored)
  - `.cody/project/library/docs/langsmith-setup.md` - Complete setup guide

## Implementation Details
- **Metadata System**: Uses `LANGCHAIN_METADATA` environment variable to pass custom metadata
- **Error Handling**: Try/except wrapper detects LangSmith network errors and falls back gracefully
- **Auto-Instrumentation**: LangChain automatically traces all operations when `LANGCHAIN_TRACING_V2=true`
- **Token Tracking**: While Ollama doesn't expose tokens in responses, LangSmith captures them via callbacks

## Testing
- ✓ All 8 phases completed (45 tasks total)
- ✓ Basic conversation flow with LangSmith enabled
- ✓ Multi-tool queries traced correctly
- ✓ User identification flow captured
- ✓ Traces visible in LangSmith dashboard
- ✓ Custom metadata (session_id, user_id) present
- ✓ Graceful degradation (works when disabled)
- ✓ Local observability windows still functional
- ✓ Token usage visible in dashboard

## Security
- ✅ `.env` file properly git-ignored
- ✅ `.env.example` safe to commit (no secrets)
- ✅ Documentation emphasizes never committing API keys
- ✅ Environment variables loaded before imports

## Learning Value
- **Production Patterns**: Demonstrates proper API key management with environment variables
- **Optional Features**: Shows how to add features without breaking core functionality
- **Error Handling**: Teaches resilience and graceful degradation
- **Dual Observability**: Provides comparison between local and cloud-based tracing
- **Security**: Emphasizes best practices for handling secrets

## Known Limitations
- Token counts not visible in terminal (Ollama limitation) - available in LangSmith dashboard only
- Requires internet connection for cloud tracing (gracefully degrades when offline)
- Free tier has usage limits (generous for learning purposes)

## Migration Notes
- No breaking changes - completely backward compatible
- App works identically with or without LangSmith
- To enable: Create `.env` file with LangSmith API key
- To disable: Set `LANGCHAIN_TRACING_V2=false` or delete `.env`

## Future Enhancements
- Consider adding 4th draggable window showing LangSmith status
- Potential for custom metrics tracking (tools per turn, response times)
- Could add trace annotations for richer debugging context

---

# v0.7.0 - Move Observability to Pop-up Window - October 17, 2025

## Overview
This version transforms the observability experience from a fixed bottom panel into three independent draggable windows (Memory, Graph, Steps) that users can toggle via checkboxes in the header. Windows open centered over the chat and are fully draggable with no restrictions, giving users complete control over their workspace layout.

## Key Features
- **Three Independent Draggable Windows**: Memory (400×500px), Graph (400×600px), and Steps (400×700px)
- **Checkbox Controls**: Toggle windows on/off via checkboxes in chat header (Observability section)
- **Centered Opening**: All windows open centered over the chat for optimal visibility
- **Fully Draggable**: No bounds restrictions - drag windows anywhere on screen
- **Z-Index Management**: Click any window to bring it to front
- **Default Closed**: All windows closed by default for clean initial interface

## Enhancements
- **Unified Window Width**: Standardized all windows to 400px width for visual consistency
- **Improved Header Styling**: Removed white space above headers, increased title font size (text-base)
- **Clean Architecture**: Extracted content components (MemoryContent, GraphContent, ExecutionStepsContent) for reusability
- **React 18+ Compatibility**: Used nodeRef with react-draggable to eliminate deprecation warnings
- **Real-time Updates**: All windows update live as conversation progresses

## Technical Changes
- **New Components**:
  - `/frontend/components/observability/DraggableMemoryWindow.tsx`
  - `/frontend/components/observability/DraggableGraphWindow.tsx`
  - `/frontend/components/observability/DraggableStepsWindow.tsx`
  - `/frontend/components/observability/MemoryContent.tsx`
  - `/frontend/components/observability/GraphContent.tsx`
  - `/frontend/components/observability/ExecutionStepsContent.tsx`
  - `/frontend/components/ui/checkbox.tsx` (shadcn/ui)
  - `/frontend/components/ui/label.tsx` (shadcn/ui)

- **Components Modified**:
  - `frontend/app/page.tsx` - Added window state management and z-index handling
  - `frontend/components/chat/ChatHeader.tsx` - Added checkbox controls
  - `frontend/components/developer/StateView.tsx` - Now uses MemoryContent
  - `frontend/components/developer/TraceView.tsx` - Now uses ExecutionStepsContent

- **Components Removed**:
  - `frontend/components/developer/DeveloperPanel.tsx` - Old bottom panel (no longer needed)
  - `frontend/app/graph/page.tsx` - Standalone graph route (now in window)

- **Dependencies Added**:
  - `react-draggable` - Enables window dragging functionality

## Bug Fixes
- Fixed white space above window headers (added `p-0` to Card component)
- Fixed deprecation warning by using `nodeRef` with react-draggable
- Fixed inconsistent window widths by standardizing to 400px

## Testing
- ✓ All 8 phases completed (47 tasks total)
- ✓ Phase 5: Styling & Polish verified
- ✓ Phase 6: Real-time updates tested
- ✓ Phase 7: Integration testing completed
- ✓ Phase 8: Cleanup & documentation finished
- ✓ Build successful with no errors
- ✓ All windows draggable with free movement
- ✓ Checkbox toggles working correctly
- ✓ Z-index layering functional

## Known Limitations
- Windows do not persist positions across page refreshes
- Windows are not resizable (fixed sizes only)
- Desktop-only (not optimized for mobile)

## Migration Notes
- No breaking changes - windows simply replace the bottom panel
- Users can continue using the app without opening any windows
- `/graph` route no longer exists (use Graph checkbox to open window)

---

# v0.6.1 - Code Cleanup and Graph View - October 16, 2025

## Overview
This version adds a graph visualization feature to the web interface and removes legacy unused code, making the codebase cleaner and more maintainable. Users can now view the LangGraph conversation flow structure directly in the browser.

## Key Features
- **Graph Visualization Page**: New `/graph` route displays LangGraph structure as PNG image (Note: This route was later replaced by the Graph window in v0.7.0)
- **"View Graph" Button**: Added to chat header for easy navigation (Note: Replaced by checkbox in v0.7.0)
- **Code Cleanup**: Removed 3 legacy node implementations (163 lines of unused code)
- **Improved Static File Routing**: Fixed routing to properly serve Next.js static export HTML files

## Enhancements
- **Educational Node Descriptions**: Graph page includes explanations of each node's purpose
- **Loading and Error States**: Proper UI feedback during graph loading
- **"Back to Chat" Navigation**: Easy return to main interface
- **Refresh Button**: Reload graph visualization on demand

## Technical Changes
- **New Files**:
  - `app/api/graph.py` - REST API endpoint `GET /api/graph` returns PNG image
  - `frontend/app/graph/page.tsx` - Graph visualization page component
- **Modified Files**:
  - `app/main.py` - Added graph router, fixed static file routing for Next.js export
  - `app/graph/nodes.py` - Removed legacy nodes (640 lines vs 803 lines, -20%)
  - `frontend/components/chat/ChatHeader.tsx` - Added "View Graph" button with GitBranch icon

## Bug Fixes
- Fixed static file routing to serve correct HTML files (graph.html vs always serving index.html)

## Code Quality
- **Before**: 6 node functions (3 unused), 803 lines in nodes.py
- **After**: 3 node functions (all active), 640 lines in nodes.py
- **Removed Legacy Nodes**:
  - `coverage_lookup_node` (42 lines)
  - `benefit_verify_node` (73 lines)
  - `claims_status_node` (48 lines)

## Testing
- ✓ Backend API endpoint returns valid PNG image
- ✓ Frontend page loads and displays graph correctly
- ✓ Navigation buttons work properly
- ✓ Static file routing serves correct HTML files
- ✓ Error handling for loading states verified
- ✓ All existing functionality preserved

## Migration Notes
- No breaking changes to existing API endpoints or frontend chat interface
- Legacy nodes (`coverage_lookup_node`, `benefit_verify_node`, `claims_status_node`) removed - use `orchestrate_tools` node instead
- No new dependencies added

## Other Notes
- Graph visualization uses LangGraph's built-in `get_graph().draw_mermaid_png()` method
- Caching headers added for performance (1-hour cache)
- Future enhancements could include interactive graphs, real-time updates, and zoom/pan functionality

---

# v0.6.0 - Move Data Folder to Root - October 16, 2025

## Overview
This version reorganizes the project structure by moving JSON data files from `/app/data/` to a new root-level `/data/` folder. This refactoring improves maintainability by providing clearer separation between data files (JSON) and data-handling code (Python modules), making it easier to manage and add new data files in the future.

## Key Features
- **Root-Level Data Folder**: Created new `/data` folder at project root for all JSON files
- **Cleaner Project Structure**: Clear separation between code (`/app/data/`) and data files (`/data/`)
- **Updated Path Resolution**: Modified `loader.py` to use `Path(__file__).parent.parent.parent / "data"` for cleaner path navigation
- **Zero Breaking Changes**: Public API of loader module remains unchanged - all existing code works without modification

## Enhancements
- **Improved Code Comments**: Added clear explanation of path navigation in loader.py
- **Updated Documentation**: README.md project structure diagram now accurately reflects new organization
- **Better Docstrings**: Module docstring in loader.py now specifies data location at root level

## Technical Changes
- **File Moves**:
  - `app/data/user_profiles.json` → `data/user_profiles.json`
  - `app/data/insurance_plans.json` → `data/insurance_plans.json`
  - `app/data/claims_data.json` → `data/claims_data.json`
- **Code Updates**:
  - Modified `DATA_DIR` constant in `app/data/loader.py` (line 30)
  - Updated module docstring to reflect new location
- **Documentation Updates**:
  - Updated README.md project structure section
  - Verified no other documentation needed updates

## Bug Fixes
None - this was a pure refactoring with no bug fixes

## Testing
- ✓ Data loading test passed - all 3 JSON files loaded successfully
- ✓ User lookup test passed
- ✓ Plan lookup test passed
- ✓ Claims lookup test passed
- ✓ Web interface test passed
- ✓ Full conversation flow test passed
- ✓ No file not found errors detected

## Other Notes
- Total of 21 tasks completed across 6 phases (Preparation, Create Structure, Update Code, Testing, Documentation, Final Verification)
- Implementation was smoother than expected - only one line of code needed changing
- Phase 1 analysis saved significant time by identifying minimal scope early
- Comprehensive retrospective document created for lessons learned
- This refactoring sets up better organization for future data additions

---

# v0.5.0 - UI Improvements AI Chatbot - October 16, 2025

## Overview
This version delivers a comprehensive redesign of the chat window UI, transforming it into a modern, polished messaging interface with improved visual hierarchy, better spacing, and enhanced user experience. The update focuses on creating a cohesive, contained design that matches modern chat applications while maintaining all existing functionality.

## Key Features
- **Contained Chat Layout**: Gray rounded border wraps entire chat window (header, messages, input) for cohesive experience
- **Modernized Input Field**: Redesigned input with light gray background, border, and send button integrated inside (matching design reference)
- **Enhanced Message Bubbles**: Custom rounded corners (straight bottom-left for AI, straight top-right for user) with no borders for cleaner appearance
- **Thinking Indicator**: Animated three-dot "thinking" bubble appears when AI is processing, disappears on response
- **Optimized Spacing**: Proper padding throughout (header alignment, message margins, scroll buffers) for balanced layout
- **Improved Colors**: Lighter slate-500 for user messages, better contrast and readability

## Enhancements
- **Header Alignment**: Title and "Clear Conversation" button now align perfectly with input box edges (px-10 padding)
- **Scroll Buffer**: Added extra bottom padding (pb-5) to prevent last message from touching input area
- **Placeholder Text**: Changed to "Ask anything you like..." for friendlier tone
- **No Page Scroll**: Added `overflow-hidden` to body to prevent unwanted scrollbar on input focus
- **Vertical Input Spacing**: Added py-2 to input container for breathing room around send button
- **Clean Input Styling**: Removed shadows, outlines, and borders from inner input element for seamless appearance

## Design Implementation
- **Reference Design**: Based on `Chat Window UX.png` mockup provided in assets
- **Components Modified**:
  - `ChatWindow.tsx` - Outer container structure and padding
  - `ChatHeader.tsx` - Header alignment (px-10)
  - `MessageList.tsx` - Message spacing (px-6), scroll buffer (pt-4 pb-5), bubble corners
  - `MessageInput.tsx` - Input redesign with embedded button, vertical padding
  - `ThinkingIndicator.tsx` - New component with animated dots
  - `layout.tsx` - Overflow hidden on body
  - `page.tsx` - Outer border and container structure

## Bug Fixes
None - purely visual/UX improvements

## Other Notes
- Total of 21 tasks completed across 5 phases
- All planned features delivered plus 3 bonus features (thinking indicator, bubble styling, header alignment)
- Design changes are CSS-only, no breaking changes to functionality
- Successfully maintained all v0.4.0 features (observability panel, state management, tool execution)
- Comprehensive retrospective document captures lessons learned for future UI work

---

# v0.4.0 - Observability Enhancements - October 16, 2025

## Overview
This version significantly improves the developer experience by transforming the "Developer Panel" into a comprehensive "Observability" panel with enhanced trace visibility, better terminology, and improved debugging capabilities. The update includes visual design improvements, smart grouping of execution steps with user prompts, and a critical bug fix for tool results display.

## Key Features
- **Rebranded Panel**: Changed "🔧 Developer Panel" to "🔍 Observability" for clearer purpose
- **Better Terminology**: "State" → "Memory", "Execution Trace" → "Execution Steps" for more intuitive navigation
- **User Prompt Display**: User messages now appear alongside execution steps with darker background (slate-800) for clear visual distinction
- **Smart Grouping**: Execution steps are grouped by the user message that triggered them, displayed latest-first for better visibility
- **System Initialization Header**: Clear visual indicator for initial startup traces, preventing confusion with user-triggered traces
- **Enhanced Tab Styling**: Active tabs feature dark gray background (slate-600) with white text and subtle rounded corners (2px)

## Enhancements
- **Improved Trace Organization**: Latest prompts and their execution steps appear first, making recent activity immediately visible
- **Visual Hierarchy**: Distinct backgrounds for user prompts vs system initialization vs execution steps
- **Better Developer Experience**: Observability panel now provides clearer insights into graph execution flow

## Bug Fixes
- **Tool Results Display**: Fixed critical bug where tool_results were always showing as empty `{}` in Memory tab
  - Root cause: `generate_response` node was clearing tool_results before API response was sent to frontend
  - Solution: Removed premature state clearing to persist tool results for frontend display
  - Impact: Memory tab now properly displays actual tool execution results for debugging

## Other Notes
- Total of 26 tasks completed across 5 phases
- All 8 planned features delivered successfully
- Updated README.md with v0.4.0 changes and new Observability features
- Comprehensive retrospective document captures lessons learned
- No breaking changes—fully backward compatible with v0.3.0

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
