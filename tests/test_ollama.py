"""
Ollama Integration Test Script

This script tests the connection between LangChain and Ollama.
It verifies that we can:
1. Import LangChain's Ollama integration
2. Initialize the LLM
3. Send a simple prompt and receive a response

Run with: python test_ollama.py
"""

from langchain_community.llms import Ollama


def test_ollama_connection():
    """
    Test basic connection to Ollama.
    """
    print("🔗 Testing Ollama Connection...")
    print("=" * 60)

    # Initialize Ollama with our chosen model
    # Using llama3.3:70b-instruct-q4_K_S as primary choice
    model_name = "llama3.3:70b-instruct-q4_K_S"

    print(f"\n1️⃣  Initializing Ollama with model: {model_name}")

    try:
        llm = Ollama(
            model=model_name,
            temperature=0.7,  # Controls randomness (0.0 = deterministic, 1.0 = creative)
        )
        print("   ✅ Ollama LLM initialized successfully")
    except Exception as e:
        print(f"   ❌ Failed to initialize Ollama: {e}")
        return False

    # Test with a simple prompt
    print("\n2️⃣  Sending test prompt...")
    test_prompt = "What is health insurance? Answer in one sentence."

    try:
        print(f"   Prompt: '{test_prompt}'")
        response = llm.invoke(test_prompt)
        print(f"   ✅ Response received!")
        print(f"\n   📝 LLM Response:\n   {response}\n")
    except Exception as e:
        print(f"   ❌ Failed to get response: {e}")
        return False

    print("=" * 60)
    print("✅ Ollama integration test PASSED!")
    print("\n💡 LangChain can successfully communicate with Ollama.")
    print(f"💡 Model '{model_name}' is working correctly.")

    return True


def test_structured_prompt():
    """
    Test a more structured prompt related to our insurance use case.
    """
    print("\n" + "=" * 60)
    print("🏥 Testing Insurance-Related Prompt...")
    print("=" * 60)

    model_name = "llama3.3:70b-instruct-q4_K_S"

    try:
        llm = Ollama(model=model_name, temperature=0.7)

        prompt = """You are an insurance coverage assistant.
A user asks: "What's the difference between a copay and a deductible?"
Provide a brief, helpful answer in 2-3 sentences."""

        print(f"\n📝 Prompt:\n{prompt}\n")
        print("⏳ Waiting for response...")

        response = llm.invoke(prompt)

        print(f"\n✅ Response:\n{response}\n")
        print("=" * 60)
        print("✅ Structured prompt test PASSED!")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "🧪 OLLAMA INTEGRATION TEST SUITE" + "\n")

    # Run basic connection test
    success = test_ollama_connection()

    if not success:
        print("\n⚠️  Basic test failed. Please check:")
        print("   - Ollama is running: `ollama list`")
        print("   - Model is available: `ollama pull llama3.3:70b-instruct-q4_K_S`")
        exit(1)

    # Run structured prompt test
    test_structured_prompt()

    print("\n🎉 All tests passed! Ready for LangGraph integration.")
