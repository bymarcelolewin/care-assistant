# Release Notes

This document lists new features, bug fixes, and other changes implemented during a particular build, also known as a version.

## Table of Contents
- [v0.7.0 - Move Observability to Pop-up Window](#v070---move-observability-to-pop-up-window---october-17-2025)
- [v0.6.0 - Move Data Folder to Root](#v060---move-data-folder-to-root---october-16-2025)
- [v0.5.0 - UI Improvements AI Chatbot](#v050---ui-improvements-ai-chatbot---october-16-2025)
- [v0.4.0 - Observability Enhancements](#v040---observability-enhancements---october-16-2025)
- [v0.3.0 - Web Interface](#v030---web-interface---october-15-2025)
- [v0.2.0 - Core Agent](#v020---core-agent)
- [v0.1.0 - Environment & Foundation](#v010---environment--foundation)

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
