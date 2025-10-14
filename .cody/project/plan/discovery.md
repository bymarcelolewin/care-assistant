# Discovery
This document captures the raw, unfiltered idea or initial AI prompt that sparked the project.

## Starting Prompt
"I want to learn LangGraph. I need an example small app, using python. I want to make sure that whatever packages we install, they are local (not global). So virtual environment using uv. I have uv installed. Can you give me a small example app to learn LangGraph?"

## Questions

**AGENT Q1:** What specific aspect of LangGraph are you most interested in learning? For example, are you interested in building conversational agents, multi-step workflows, state management in AI applications, or something else?
**USER A1:** I want a simple conversational agent that teaches me about state management, nodes, edges and tools maybe.

**AGENT Q2:** What kind of conversational experience are you envisioning? For example, should this be a CLI-based chat interface, a simple script that demonstrates the concepts, or something interactive where you can see how state changes as the conversation progresses?
**USER A2:** I would like it to be web driven (browser), but run locally. If possible maybe use ollama? I have it installed locally as well already.

**AGENT Q3:** What would you like this conversational agent to actually do or help with? For example, should it be a teaching assistant that explains LangGraph concepts as you chat with it, a task helper (like a to-do manager or research assistant), or something else that demonstrates state management in action?
**USER A3:** How about an agent that helps people find out more about their healthcare?

**AGENT Q4:** Can you tell me more about what "find out more about their healthcare" means? For example, should this agent help users understand their symptoms and suggest when to see a doctor, explain medical terminology or conditions in simple terms, navigate insurance coverage and benefits, find healthcare providers or facilities, track medications or appointments, or something else entirely? And to clarify — is this meant to provide general health information and education, or would it need to work with actual user health data?
**USER A4:** Navigate insurance coverage and benefits.

**AGENT Q5:** Should this agent work with real insurance data (like parsing actual policy documents or connecting to insurance APIs), or should it be a learning example that uses mock/sample insurance data to demonstrate LangGraph concepts like state management and tool usage?
**USER A5:** Let's create mock data. We'll need multiple to simulate different users.

**AGENT Q6:** What would success look like for this learning project? For example: You understand how to structure LangGraph nodes, edges, and state management? You can see how tools are integrated and called within a graph? You can modify and extend the agent to add new capabilities? You feel confident enough to build your own LangGraph application after working through this example?
**USER A6:** #3 - Modify and extend.

**AGENT Q7:** Are there any specific constraints or preferences I should keep in mind? For example: Should the web interface be minimal (basic HTML/CSS) or would you prefer a specific framework (Flask, FastAPI, Streamlit, Gradio)? Any specific LangGraph features or patterns you want to make sure are demonstrated? Timeline or urgency for getting this set up? Any technologies you want to avoid?
**USER A7:** I want the web interface to be simple, but show the thinking process (collapsed by default) if need be.

**AGENT Q8:** How will you know this learning app is successful? What specific outcomes or capabilities should it demonstrate? For example: Successfully shows how conversation state persists across multiple turns? Demonstrates how the agent can call tools (like looking up coverage details)? Shows conditional logic (different paths based on user input)? Allows you to easily see and understand the graph structure and execution flow?
**USER A8:** All of what you listed.

## Discovery Summary

This is a learning-focused LangGraph example application designed to teach core LangGraph concepts through hands-on practice. The target user is a developer who wants to understand LangGraph fundamentals including state management, nodes, edges, tool integration, and conditional logic.

The application is a conversational agent that helps users navigate insurance coverage and benefits. It will use mock insurance data for multiple simulated users to demonstrate realistic scenarios without requiring real data or APIs.

**Technical Stack:**
- Python with LangGraph
- Virtual environment managed by `uv` (already installed)
- Local LLM via Ollama (already installed)
- Simple web interface (browser-based, minimal design)
- Runs entirely locally

**Key Learning Demonstrations:**
- State management: Conversation state persists across multiple turns
- Nodes and edges: Clear graph structure showing how conversation flows
- Tool usage: Agent can call tools (e.g., lookup coverage details from mock data)
- Conditional logic: Different execution paths based on user input
- Transparency: Visible "thinking process" (collapsed by default) to see graph execution

**Success Criteria:**
The learner should be able to:
- Understand how LangGraph structures nodes, edges, and state
- See how tools are integrated and called within the graph
- Observe state persistence across conversation turns
- View conditional logic and routing in action
- Easily modify and extend the agent with new capabilities

**Constraints:**
- Must use `uv` for virtual environment (local packages only)
- Must run entirely locally
- Mock data only (no real insurance APIs or data)
- Simple, clean web interface that exposes the learning aspects
