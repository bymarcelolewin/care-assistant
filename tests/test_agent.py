"""
CLI Test Script for CARE Assistant Agent.

This script provides an interactive command-line interface to test the LangGraph agent.
It demonstrates:
- Agent invocation with state management
- Multi-turn conversation handling
- Execution trace visualization
- State persistence across turns

Usage:
    python tests/test_agent.py

Commands:
    - Type messages to chat with the agent
    - Type 'trace' to see the execution trace
    - Type 'state' to see the current state
    - Type 'clear' to start a new conversation
    - Type 'quit' or 'exit' to exit

This is a learning tool - examine the code to understand how to:
1. Initialize and invoke the compiled agent
2. Maintain state across conversation turns
3. Handle user input and agent responses
4. Visualize execution traces
"""

import asyncio
import json
from pathlib import Path
import sys

# Add the project root to the path so we can import app modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langchain_core.messages import HumanMessage
from app.graph.graph import compile_agent
from app.data.loader import initialize_data


def print_separator(char="=", length=80):
    """Print a separator line."""
    print(char * length)


def print_message(message, role=""):
    """Pretty print a message."""
    if role:
        print(f"\n{role}:")
    print(f"{message.content}")


def print_execution_trace(trace, last_turn_only=False, previous_count=0):
    """
    Pretty print the execution trace.

    Args:
        trace: List of trace entries
        last_turn_only: If True, only show entries from the last turn
        previous_count: Number of trace entries before the last turn
    """
    print("\n" + "=" * 80)
    if last_turn_only:
        print(f"EXECUTION TRACE - LAST TURN ONLY ({len(trace) - previous_count} entries)")
        print(f"(Total trace entries: {len(trace)} | Use 'trace full' to see all)")
    else:
        print(f"EXECUTION TRACE - FULL ({len(trace)} entries)")
    print("=" * 80)

    # If showing last turn only, start from previous_count
    start_idx = previous_count if last_turn_only else 0
    entries_to_show = trace[start_idx:]

    for i, entry in enumerate(entries_to_show, start_idx + 1):
        print(f"\n[{i}] Node: {entry.get('node')}")
        print(f"    Time: {entry.get('timestamp')}")
        print(f"    Action: {entry.get('action')}")

        # Show additional details if present
        if 'llm_response' in entry:
            print(f"    LLM Response: {entry.get('llm_response')}")
        if 'user_message' in entry:
            print(f"    User Message: {entry.get('user_message')[:50]}...")
        if 'service_type' in entry:
            print(f"    Service Type: {entry.get('service_type')}")
        if 'status_filter' in entry:
            print(f"    Status Filter: {entry.get('status_filter')}")

    print("=" * 80)


def print_state_summary(state):
    """Print a summary of the current state."""
    print("\n" + "=" * 80)
    print("STATE SUMMARY")
    print("=" * 80)

    print(f"\nUser ID: {state.get('user_id', 'Not identified')}")

    if state.get('user_profile'):
        profile = state['user_profile']
        print(f"User Name: {profile.get('name')}")
        print(f"Plan: {profile.get('plan_id')}")
        print(f"Deductible Met: ${profile.get('deductible_met')} / ${profile.get('deductible_annual')}")

    print(f"\nIntent: {state.get('intent', 'None')}")
    print(f"Message Count: {len(state.get('messages', []))}")
    print(f"Trace Entries: {len(state.get('execution_trace', []))}")

    print("=" * 80)


async def run_interactive_session():
    """
    Run an interactive CLI session with the CARE Assistant agent.

    This demonstrates how to:
    1. Initialize the data and compile the agent
    2. Maintain state across multiple conversation turns
    3. Handle user input and agent responses
    4. Use special commands for debugging
    """
    print_separator()
    print("CARE ASSISTANT - Interactive CLI Test")
    print_separator()
    print("\nInitializing agent...")

    # Initialize mock data (must be done before agent invocation)
    initialize_data()
    print("✓ Mock data loaded")

    # Compile the agent
    agent = compile_agent()
    print("✓ Agent compiled")

    # Initialize state for the conversation
    # This state will be passed through and updated with each turn
    state = {
        "messages": [],
        "execution_trace": [],
        "conversation_context": {}
    }

    print("\nAgent ready! Type your messages below.")
    print("Commands: 'trace' (last turn), 'trace full' (all), 'state' (show state), 'clear' (new conversation), 'quit' (exit)")
    print_separator()

    # Track trace count before each turn to show only new entries
    previous_trace_count = 0

    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            # Handle special commands
            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye! 👋")
                break

            elif user_input.lower() == 'trace':
                # Show only the last turn's trace entries
                print_execution_trace(
                    state.get('execution_trace', []),
                    last_turn_only=True,
                    previous_count=previous_trace_count
                )
                continue

            elif user_input.lower() == 'trace full':
                # Show full trace from the beginning
                print_execution_trace(state.get('execution_trace', []), last_turn_only=False)
                continue

            elif user_input.lower() == 'state':
                print_state_summary(state)
                continue

            elif user_input.lower() == 'clear':
                state = {
                    "messages": [],
                    "execution_trace": [],
                    "conversation_context": {}
                }
                previous_trace_count = 0
                print("\n✓ Conversation cleared. Starting fresh!")
                continue

            # Track trace count BEFORE this turn
            previous_trace_count = len(state.get('execution_trace', []))

            # Add user message to state
            state["messages"].append(HumanMessage(content=user_input))

            # Invoke the agent
            # The agent will process the message and return updated state
            print("\n🤖 Agent: ", end="", flush=True)

            # Run the agent (it's async, so we await it)
            result = await agent.ainvoke(state)

            # Update our state with the result
            state = result

            # Print the agent's response (last message in the list)
            if state.get('messages'):
                last_message = state['messages'][-1]
                print(last_message.content)

            # Show a quick trace summary for this turn only
            current_trace_count = len(state.get('execution_trace', []))
            new_entries = current_trace_count - previous_trace_count
            print(f"\n   (This turn: {new_entries} trace entries | Type 'trace' to see details)")

        except KeyboardInterrupt:
            print("\n\nInterrupted! Type 'quit' to exit or continue chatting.")
            continue

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nTip: Make sure Ollama is running and the model is available.")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point."""
    # Run the async interactive session
    asyncio.run(run_interactive_session())


if __name__ == "__main__":
    main()
