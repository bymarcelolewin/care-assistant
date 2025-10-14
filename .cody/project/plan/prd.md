# Product Requirements Document (PRD)
This document formalizes the idea and defines the what and the why of the product the USER is building.

## Section Explanations
| Section           | Overview |
|-------------------|--------------------------|
| Summary           | Sets the high-level context for the product. |
| Goals             | Articulates the product's purpose — core to the "why". |
| Target Users      | Clarifies the audience, essential for shaping features and priorities. |
| Key Features      | Describes what needs to be built to meet the goals — part of the "what". |
| Success Criteria  | Defines what outcomes validate the goals. |
| Out of Scope      | Prevents scope creep and sets boundaries. |
| User Stories      | High-level stories keep focus on user needs (why) and guide what to build. |
| Assumptions       | Makes the context and unknowns explicit — essential for product clarity. |
| Dependencies      | Identifies blockers and critical integrations — valuable for planning dependencies and realism. |

## Summary
CARE (Coverage Analysis and Recommendation Engine) Assistant is a hands-on LangGraph learning application that demonstrates core concepts (state management, nodes, edges, tools, and conditional logic) through a practical example: an AI-powered insurance coverage assistant that helps users understand their healthcare benefits using mock data.

## Goals
_What are we trying to achieve? List the key objectives or outcomes._

- **Teach LangGraph Fundamentals**: Provide clear, working examples of state management, graph structure (nodes/edges), tool integration, and conditional routing
- **Enable Hands-On Learning**: Create a modifiable codebase that learners can extend and experiment with
- **Demonstrate Practical Patterns**: Show real-world LangGraph patterns through a realistic use case (insurance navigation)
- **Provide Visibility**: Make the agent's thinking process transparent so learners can see how LangGraph executes
- **Local Development Experience**: Ensure everything runs locally without external dependencies or cloud services

## Target Users
_Who is this for? Briefly describe the audience._

Developers who want to learn LangGraph through hands-on practice. The primary user is someone with Python experience who wants to understand how to build stateful, tool-using conversational agents with LangGraph. They prefer learning by doing and want to see concepts in action rather than just reading documentation.

## Key Features
_What core features are required to meet the goals?_

- **Conversational Agent**: Insurance coverage assistant that answers questions about benefits and coverage
- **Mock User Data**: Multiple simulated user profiles with different insurance plans and coverage details
- **Tool Integration**: Demonstrates LangGraph tools through coverage lookup, benefit verification, and claims status functions
- **State Management**: Maintains conversation context across multiple turns (user identity, conversation history, retrieved data)
- **Graph Visualization**: Shows the agent's execution path through nodes and edges
- **Thinking Process Display**: Collapsible view showing internal reasoning, tool calls, and state transitions
- **Web Interface**: Simple browser-based UI for interacting with the agent locally
- **Local LLM Integration**: Uses Ollama for running the language model entirely on the user's machine
- **Virtual Environment Setup**: Uses `uv` for isolated Python environment management
- **Well-Commented Code**: Extensive inline documentation explaining LangGraph concepts as they appear

## Success Criteria
_How do we know it worked?_

- **State Persistence**: Learner can observe conversation state carrying over between turns
- **Tool Usage Clarity**: Tool calls are visible and their integration pattern is clear
- **Graph Structure Understanding**: Learner can explain how nodes and edges define the conversation flow
- **Conditional Logic Visibility**: Different execution paths based on user input are observable
- **Modification Capability**: Learner can successfully add a new tool or modify existing behavior
- **Local Execution**: Application runs entirely locally without external API calls
- **Clear Learning Path**: Code comments and structure guide the learner through LangGraph concepts

## Out of Scope (Optional)
_What won't be included in the first version?_

- **Real Insurance APIs**: No integration with actual insurance providers or data sources
- **User Authentication**: No login system or persistent user accounts
- **Database Storage**: Conversation history stored in memory only, not persisted to disk
- **Production Features**: No error recovery, logging, monitoring, or production-grade security
- **Advanced Graph Patterns**: No parallel execution, sub-graphs, or complex conditional branching
- **Mobile Interface**: Web UI designed for desktop browsers only
- **Multi-Model Support**: Ollama only; no OpenAI, Anthropic, or other provider integrations
- **Deployment**: No containerization, cloud deployment, or hosting instructions

## User Stories (Optional)
_What does the user want to accomplish? Keep these high-level to focus on user goals, not implementation details._

- **As a learner**, I want to see how conversation state persists across turns so I understand LangGraph's state management
- **As a learner**, I want to observe tool calls in action so I understand how to integrate external functions
- **As a learner**, I want to view the graph execution path so I understand how nodes and edges define flow
- **As a learner**, I want to modify the agent's behavior so I can practice extending LangGraph applications
- **As a learner**, I want to see conditional routing in action so I understand how to create dynamic conversation flows
- **As a learner**, I want clear code comments so I understand what each LangGraph component does
- **As a developer**, I want everything running locally so I can experiment without external dependencies

## Assumptions
_What are we assuming to be true when building this?_

- User has Python 3.10+ installed
- User has `uv` package manager already installed
- User has Ollama installed and running locally with at least one model available
- User has basic Python programming knowledge
- User is comfortable running commands in a terminal
- User has a modern web browser (Chrome, Firefox, Safari, Edge)
- Mock insurance data is sufficient for learning purposes (no real data needed)
- Learner wants to understand concepts through code exploration rather than step-by-step tutorials

## Dependencies
_What systems, tools, or teams does this depend on?_

- **Python**: 3.10 or higher
- **uv**: For virtual environment and package management
- **Ollama**: For local LLM inference
- **LangGraph**: Core framework being taught
- **LangChain**: Required by LangGraph for LLM abstractions
- **Web Framework**: Flask or FastAPI for serving the web interface
- **Mock Data**: JSON files containing simulated insurance plans and user profiles
