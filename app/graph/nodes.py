"""
LangGraph Node Implementations for CARE Assistant.

This module contains all node functions that make up the conversation graph.
Each node is an async function that:
1. Receives the current state
2. Performs some operation (LLM call, tool call, data lookup, etc.)
3. Returns a dict with state updates

Nodes are the building blocks of LangGraph. They define the logic at each step
of the conversation flow.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from .state import ConversationState
from app.data.loader import get_data
from app.tools import coverage_lookup, benefit_verify, claims_status


# ============================================================================
# LLM Instance (Shared across nodes)
# ============================================================================

# Initialize ChatOllama once and reuse across all nodes
# This is more efficient than creating a new instance for each LLM call
llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,  # Moderate creativity for conversational responses
)


# ============================================================================
# Structured Output Models
# ============================================================================

class NameExtraction(BaseModel):
    """
    Structured output model for extracting a person's name from natural language.

    This is used to handle various ways users might introduce themselves:
    - "John"
    - "I'm John"
    - "My name is John Smith"
    - "Call me John"
    - "John, your patient"
    """
    name: Optional[str] = Field(
        description="The person's first name or full name extracted from the message. Just the name, nothing else."
    )
    confidence: str = Field(
        description="Confidence level: 'high' if clearly stated, 'low' if uncertain"
    )


# ============================================================================
# Helper Functions
# ============================================================================

def add_trace_entry(trace: list, node_name: str, action: str, details: Dict[str, Any] = None) -> list:
    """
    Helper function to add an entry to the execution trace.

    The execution trace provides visibility into how the graph executes,
    which is essential for learning and debugging LangGraph applications.

    Args:
        trace: Current execution trace list from state
        node_name: Name of the node being executed
        action: Description of what the node is doing
        details: Optional additional information (LLM prompts, tool results, etc.)

    Returns:
        list: Updated trace with new entry appended
    """
    entry = {
        "node": node_name,
        "timestamp": datetime.now().isoformat(),
        "action": action,
    }

    if details:
        entry.update(details)

    return trace + [entry]


# ============================================================================
# Node 1: Identify User
# ============================================================================

async def identify_user(state: ConversationState) -> Dict[str, Any]:
    """
    Identify or confirm the user's identity through conversational name lookup.

    This node implements the conversational user identification flow:
    1. Check if user_id already exists in state (already identified)
    2. If not, check if the latest message contains a name
    3. Search user_profiles.json by name (case-insensitive)
    4. If found: Load user profile into state
    5. If not found: Return "not in system" message

    This demonstrates LangGraph concepts:
    - Reading from state (checking user_id, messages)
    - Data lookup using external functions
    - Returning state updates (user_id, user_profile, messages)
    - Execution tracing for visibility

    Args:
        state: Current conversation state

    Returns:
        dict: State updates containing user_id, user_profile, messages, and execution_trace
    """
    # Add trace entry to track node execution
    trace = add_trace_entry(
        state.get("execution_trace", []),
        "identify_user",
        "Starting user identification process"
    )

    # Check if user is already identified
    if state.get("user_id"):
        # User already identified, no action needed
        trace = add_trace_entry(
            trace,
            "identify_user",
            f"User already identified: {state.get('user_id')}",
            {"user_name": state.get("user_profile", {}).get("name")}
        )
        return {"execution_trace": trace}

    # Get the latest message from the user
    messages = state.get("messages", [])

    # If this is the very first interaction (no messages yet), prompt for name
    if len(messages) == 0:
        greeting = AIMessage(
            content="Hello! I'm your ❤️ CARE Assistant. What's your name?"
        )
        trace = add_trace_entry(
            trace,
            "identify_user",
            "First interaction - requesting user name"
        )
        return {
            "messages": [greeting],
            "execution_trace": trace
        }

    # Get the last user message
    last_message = messages[-1]

    # Check if we've already asked for their name
    # Look for our greeting in the message history
    has_greeted = any(
        isinstance(msg, AIMessage) and "What's your name?" in msg.content
        for msg in messages
    )

    if not has_greeted:
        # Haven't asked yet, ask now
        greeting = AIMessage(
            content="Hello! I'm your ❤️ CARE Assistant. What's your name?"
        )
        trace = add_trace_entry(
            trace,
            "identify_user",
            "Requesting user name"
        )
        return {
            "messages": [greeting],
            "execution_trace": trace
        }

    # User has responded after we asked for their name
    # Use LLM to extract the name from their natural language message
    user_input = last_message.content.strip()

    trace = add_trace_entry(
        trace,
        "identify_user",
        f"Extracting name from user message: '{user_input}'"
    )

    # Create an LLM with structured output to extract the name
    llm_with_structure = llm.with_structured_output(NameExtraction)

    # Prompt the LLM to extract just the name
    extraction_prompt = f"""Extract the person's name from this message: "{user_input}"

Examples:
- "I'm John" → name: "John"
- "My name is Sarah Smith" → name: "Sarah Smith"
- "Call me Mike" → name: "Mike"
- "Emily" → name: "Emily"
- "I'm Marcelo, your patient" → name: "Marcelo"

Only extract the actual name, nothing else. If you're not sure, set confidence to 'low'."""

    # Get the structured extraction
    extraction_result = await llm_with_structure.ainvoke(extraction_prompt)
    extracted_name = extraction_result.name

    trace = add_trace_entry(
        trace,
        "identify_user",
        f"LLM extracted name: '{extracted_name}' (confidence: {extraction_result.confidence})",
        {"original_input": user_input, "extracted_name": extracted_name}
    )

    # If no name was extracted, ask again
    if not extracted_name or extraction_result.confidence == "low":
        retry_message = AIMessage(
            content="I didn't quite catch your name. Could you please tell me your first name?"
        )
        return {
            "messages": [retry_message],
            "execution_trace": trace
        }

    # Search for the user by the extracted name
    trace = add_trace_entry(
        trace,
        "identify_user",
        f"Searching for user by extracted name: {extracted_name}"
    )

    # Load data and search for user by name (case-insensitive)
    data = get_data()
    found_user = None

    for user in data.get("users", []):
        # Check if the extracted name matches the user's first name or full name (case-insensitive)
        user_name = user.get("name", "")
        first_name = user_name.split()[0].lower() if user_name else ""

        if extracted_name.lower() == first_name or extracted_name.lower() == user_name.lower():
            found_user = user
            break

    if found_user:
        # User found! Load their profile
        user_id = found_user.get("user_id")
        user_name = found_user.get("name")
        first_name = user_name.split()[0] if user_name else "there"
        member_since = found_user.get("member_since", "")

        trace = add_trace_entry(
            trace,
            "identify_user",
            f"User found: {user_name} ({user_id})",
            {"user_profile": found_user}
        )

        # Format the member_since date to be more readable (e.g., "March 2022")
        if member_since:
            try:
                date_obj = datetime.strptime(member_since, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%B %Y")
                welcome_message = AIMessage(
                    content=f"Welcome {first_name}! ❤️ Thank you for being a member since {formatted_date}. Do you have any questions about your plan, benefits, or claims?"
                )
            except ValueError:
                # If date parsing fails, use a simpler welcome
                welcome_message = AIMessage(
                    content=f"Welcome {first_name}! ❤️ I found your account. Do you have any questions about your plan, benefits, or claims?"
                )
        else:
            welcome_message = AIMessage(
                content=f"Welcome {first_name}! ❤️ I found your account. Do you have any questions about your plan, benefits, or claims?"
            )

        return {
            "user_id": user_id,
            "user_profile": found_user,
            "messages": [welcome_message],
            "execution_trace": trace,
            "first_greeting": True  # Flag to skip orchestration and show welcome message only
        }
    else:
        # User not found
        trace = add_trace_entry(
            trace,
            "identify_user",
            f"User not found: {extracted_name}",
            {"searched_name": extracted_name}
        )

        not_found_message = AIMessage(
            content=f"Sorry {extracted_name}, you are not in our system. Please contact support for assistance."
        )

        return {
            "messages": [not_found_message],
            "execution_trace": trace
        }


# ============================================================================
# Node 2: Orchestrate Tools (Multi-tool coordinator)
# ============================================================================

async def orchestrate_tools(state: ConversationState) -> Dict[str, Any]:
    """
    Orchestrate multiple tool calls for complex requests.

    This node uses the LLM with tool binding to intelligently determine
    which tools to call (and in what order) to answer complex user questions.

    The flow:
    1. LLM sees the user question and available tools
    2. LLM decides which tools to call (can call multiple)
    3. Tools are executed and results stored
    4. Results are accumulated in tool_results dict
    5. Node sets needs_tool_call=False to signal completion

    This enables handling requests like:
    "What plan do I have, how long have I been a member, what does it offer,
    and do I have outstanding claims?"

    Which requires: coverage_lookup + benefit_verify + claims_status

    Args:
        state: Current conversation state

    Returns:
        dict: State updates with all tool_results, execution trace, and progress_messages
    """
    trace = state.get("execution_trace", [])
    user_id = state.get("user_id")
    messages = state.get("messages", [])
    user_profile = state.get("user_profile", {})
    progress_messages = []

    if not messages:
        return {
            "needs_tool_call": False,
            "execution_trace": trace
        }

    # Get the user's question
    user_message = messages[-1].content

    trace = add_trace_entry(
        trace,
        "orchestrate_tools",
        "Determining which tools to call for complex request"
    )

    # Create a prompt that tells the LLM which tools to call
    # Ollama doesn't support native tool binding, so we use text-based orchestration
    user_question_msg = HumanMessage(content=f"""Analyze this insurance question and determine which tools to call:

Question: "{user_message}"

Available tools:
- coverage_lookup: Returns plan details, deductibles, limits, member since date
- benefit_verify: Checks if specific medical services are covered
- claims_status: Returns claims history and pending/approved/denied claims

Instructions:
1. Read the question carefully
2. Identify what information is being asked for
3. List ONLY the tool names needed, one per line
4. Do not include any explanation or extra text

Examples:
Question: "What plan do I have and when did I become a member?"
Response:
coverage_lookup

Question: "Do I have any pending claims?"
Response:
claims_status

Question: "What plan do I have, what does it cover, and do I have outstanding claims?"
Response:
coverage_lookup
benefit_verify
claims_status

Now analyze the question above and respond with only the tool names:""")

    # Let the LLM decide which tools to call
    trace = add_trace_entry(
        trace,
        "orchestrate_tools",
        "Asking LLM to determine which tools are needed"
    )

    response = await llm.ainvoke([user_question_msg])

    trace = add_trace_entry(
        trace,
        "orchestrate_tools",
        f"LLM suggested tools: {response.content}"
    )

    # Parse the LLM's response to extract tool names
    tool_names = []
    for line in response.content.strip().split('\n'):
        line = line.strip().lower()
        if 'coverage_lookup' in line:
            tool_names.append('coverage_lookup')
        elif 'benefit_verify' in line:
            tool_names.append('benefit_verify')
        elif 'claims_status' in line:
            tool_names.append('claims_status')

    # Remove duplicates while preserving order
    tool_names = list(dict.fromkeys(tool_names))

    trace = add_trace_entry(
        trace,
        "orchestrate_tools",
        f"Extracted tool names: {tool_names}"
    )

    # Initialize or get existing tool_results dict
    all_tool_results = state.get("tool_results", {})
    if all_tool_results is None:
        all_tool_results = {}

    # Execute the tools the LLM selected
    if tool_names:
        # Execute each tool call
        for tool_name in tool_names:
            # Add friendly progress message for this tool
            tool_progress_messages = {
                "coverage_lookup": "Let me check your coverage details...",
                "benefit_verify": "Now let me verify what benefits are covered...",
                "claims_status": "Let me look up your claims history..."
            }

            if tool_name in tool_progress_messages:
                progress_messages.append(tool_progress_messages[tool_name])

            trace = add_trace_entry(
                trace,
                "orchestrate_tools",
                f"Executing tool: {tool_name}",
                {"tool_name": tool_name, "progress_message": tool_progress_messages.get(tool_name, "")}
            )

            # Call the appropriate tool with user_id and query
            tool_args = {
                "user_id": user_id,
                "query": user_message
            }

            if tool_name == "coverage_lookup":
                result = coverage_lookup.invoke(tool_args)
                all_tool_results["coverage_lookup"] = result
            elif tool_name == "benefit_verify":
                # benefit_verify needs service_type, extract from question or default
                tool_args["service_type"] = "general medical"  # Default for now
                result = benefit_verify.invoke(tool_args)
                all_tool_results["benefit_verify"] = result
            elif tool_name == "claims_status":
                result = claims_status.invoke(tool_args)
                all_tool_results["claims_status"] = result

            trace = add_trace_entry(
                trace,
                "orchestrate_tools",
                f"Tool {tool_name} completed",
                {"status": result.get('status') if isinstance(result, dict) else 'success'}
            )

        # All tools executed, ready to generate response
        return {
            "tool_results": all_tool_results,
            "needs_tool_call": False,
            "execution_trace": trace,
            "progress_messages": progress_messages
        }
    else:
        # LLM didn't call any tools - this is unusual but handle gracefully
        trace = add_trace_entry(
            trace,
            "orchestrate_tools",
            "No tool calls needed (unusual - LLM decided question doesn't need tools)"
        )

        return {
            "needs_tool_call": False,
            "execution_trace": trace
        }


# ============================================================================
# Node 3: Generate Response
# ============================================================================

async def generate_response(state: ConversationState) -> Dict[str, Any]:
    """
    Generate a natural language response using the LLM.

    This node synthesizes:
    - Conversation history from state
    - Tool results (if any) from previous nodes
    - User's original question

    Into a helpful, conversational response that answers the user's question.

    This demonstrates:
    - Using full conversation context
    - Incorporating tool results into prompts
    - Generating natural language responses
    - Clearing temporary state after response

    Args:
        state: Current conversation state

    Returns:
        dict: State updates with new message, cleared temporary data, and execution trace
    """
    trace = add_trace_entry(
        state.get("execution_trace", []),
        "generate_response",
        "Generating response with LLM"
    )

    # Get conversation history
    messages = state.get("messages", [])
    tool_results = state.get("tool_results")
    user_profile = state.get("user_profile", {})

    # Build context for the LLM
    # Format user profile details for the LLM
    user_details = ""
    if user_profile:
        user_details = f"""
Current User Profile:
- Name: {user_profile.get('name', 'Unknown')}
- Age: {user_profile.get('age', 'Unknown')}
- Plan ID: {user_profile.get('plan_id', 'Unknown')}
- Member Since: {user_profile.get('member_since', 'Unknown')}
- Annual Deductible: ${user_profile.get('deductible_annual', 0):,}
- Deductible Met: ${user_profile.get('deductible_met', 0):,}
- Out-of-Pocket Maximum: ${user_profile.get('out_of_pocket_max', 0):,}
- Out-of-Pocket Spent: ${user_profile.get('out_of_pocket_spent', 0):,}
- Dependents: {user_profile.get('dependents', 0)}
"""

    system_prompt = f"""You are a helpful insurance coverage assistant for CARE Insurance.
You help users understand their insurance coverage, benefits, and claims.

{user_details}

IMPORTANT INSTRUCTIONS:
1. Use ONLY the exact information provided above from the user profile. Do NOT make up or guess any data.
2. You are running locally with the user's consent. You MAY share personal information from their profile when asked (age, member date, deductible amounts, etc.).
3. If specific information is not provided in the user profile or tool results, say you don't have that information.
4. Be conversational, friendly, and helpful. Explain insurance terms in simple language.
5. If tool results are provided below, use them to give specific, accurate information."""

    # Add tool results to context if available
    # tool_results can now be a dict with multiple tool outputs
    if tool_results:
        tool_context = "\n\nTool Results:\n"

        # Check if it's the new multi-tool format (dict of tool_name: result)
        # or old single-tool format (single dict with 'status')
        if isinstance(tool_results, dict) and "status" in tool_results:
            # Old single-tool format
            tool_context += f"{tool_results}\n"
        elif isinstance(tool_results, dict):
            # New multi-tool format - iterate through each tool's results
            for tool_name, result in tool_results.items():
                tool_context += f"\n--- {tool_name.upper()} ---\n"
                tool_context += f"{result}\n"

        system_prompt += tool_context

    # Create prompt with full conversation context
    prompt_messages = [SystemMessage(content=system_prompt)] + messages

    try:
        # Generate response
        response = await llm.ainvoke(prompt_messages)

        trace = add_trace_entry(
            trace,
            "generate_response",
            "Response generated successfully",
            {
                "llm_prompt_length": len(system_prompt),
                "has_tool_results": tool_results is not None,
                "response_length": len(response.content)
            }
        )

        # Return the response
        # Note: We keep tool_results in state so the frontend can display them
        # They will be replaced when new tools are called in the next turn
        return {
            "messages": [AIMessage(content=response.content)],
            "execution_trace": trace
        }

    except Exception as e:
        trace = add_trace_entry(
            trace,
            "generate_response",
            f"Error generating response: {str(e)}",
            {"error": str(e)}
        )

        # Fallback response
        error_response = AIMessage(
            content="I'm sorry, I encountered an error generating a response. Could you please rephrase your question?"
        )

        return {
            "messages": [error_response],
            "execution_trace": trace
        }
