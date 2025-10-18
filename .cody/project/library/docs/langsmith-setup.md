# LangSmith Setup Guide

Complete guide for setting up and using LangSmith observability with CARE Assistant.

## Table of Contents
- [What is LangSmith?](#what-is-langsmith)
- [Why Use LangSmith?](#why-use-langsmith)
- [Setup Instructions](#setup-instructions)
- [Using LangSmith](#using-langsmith)
- [Troubleshooting](#troubleshooting)

---

## What is LangSmith?

**LangSmith** is LangChain's official observability and debugging platform for LLM applications. It provides:

- **Tracing** - Visual traces of every LLM call, tool execution, and agent step
- **Debugging** - Inspect inputs, outputs, and intermediate steps in detail
- **Monitoring** - Track performance, latency, and token usage
- **Evaluation** - Test and compare different prompts and models
- **Datasets** - Create test cases for your agent

LangSmith is a **cloud-based** service with a generous free tier, perfect for learning and development.

---

## Why Use LangSmith?

### For Learning LangGraph
- **Visual Understanding** - See exactly how your graph executes step-by-step
- **Tool Call Inspection** - Understand when and why tools are invoked
- **State Changes** - Track how conversation state evolves
- **Performance Analysis** - Identify slow nodes or bottlenecks

### Complements Local Observability
CARE Assistant has **two levels of observability**:

1. **Local** (Draggable Windows) - Great for quick debugging during development
2. **Cloud** (LangSmith) - Professional-grade tracing with persistent history

Both work together! Local windows show real-time execution, while LangSmith keeps a searchable history.

---

## Setup Instructions

### Step 1: Create LangSmith Account

1. Go to [https://smith.langchain.com/](https://smith.langchain.com/)
2. Click **"Sign Up"**
3. Create account (free tier available)

### Step 2: Create a Project

1. After logging in, click **"New Project"**
2. Name it: `care-assistant`
3. Click **"Create"**

### Step 3: Get API Key

1. Click on your profile icon (top right)
2. Select **"Settings"**
3. Navigate to **"API Keys"**
4. Click **"Create API Key"**
5. Copy the key (starts with `lsv2_pt_...`)
6. **⚠️ Important**: Save this key securely - you won't see it again!

### Step 4: Configure Environment Variables

The CARE Assistant project already has `.env.example` template. Create your `.env`:

```bash
# From the project root
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
# LangSmith Configuration

# Enable LangSmith tracing
LANGCHAIN_TRACING_V2=true

# Your LangSmith API key (replace with your actual key)
LANGCHAIN_API_KEY=lsv2_pt_your_actual_key_here

# Project name (must match your project in LangSmith)
LANGCHAIN_PROJECT=care-assistant

# LangSmith API endpoint (default)
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# Optional: Environment tag
ENVIRONMENT=development
```

### Step 5: Verify Setup

Start the application:

```bash
uv run uvicorn app.main:app --port 8000
```

You should see:
```
✅ LangSmith tracing enabled
📊 Project: care-assistant
🌐 Dashboard: https://smith.langchain.com/
```

If you see `⚪ LangSmith tracing disabled`, check your `.env` file.

---

## Using LangSmith

### Viewing Traces

1. Open [https://smith.langchain.com/](https://smith.langchain.com/)
2. Select your **"care-assistant"** project
3. You'll see a list of all traces (conversations)

### Understanding a Trace

Click on any trace to see:

- **Inputs** - The user's message
- **Outputs** - The agent's response
- **Intermediate Steps** - Every node execution, tool call, and LLM invocation
- **Metadata** - Session ID, user ID, environment tag
- **Token Usage** - Input/output tokens for each LLM call
- **Latency** - Time taken for each step

### Trace Metadata

Every trace includes custom metadata:
- `session_id` - Unique conversation session
- `user_id` - Identified user (e.g., "user_001" for Sarah)
- `environment` - "development" or "production"

Use these to **filter traces** in the LangSmith UI.

### Inspecting Tool Calls

LangSmith shows exactly which tools were called:
- `coverage_lookup` - User's coverage details
- `benefit_verify` - Specific benefit verification
- `claims_status` - Claims history

You can see:
- Tool inputs (arguments)
- Tool outputs (results)
- Execution time

### Token Usage Tracking

While Ollama doesn't expose token counts in the response, **LangSmith tracks them automatically**:

1. Click on any LLM call in a trace
2. Look for **"Usage"** section
3. See: Input tokens, Output tokens, Total tokens

This helps you understand:
- How much context you're sending
- How long responses are
- Potential costs if using paid LLM providers

---

## Troubleshooting

### App Says "LangSmith tracing disabled"

**Check:**
1. `.env` file exists in project root
2. `LANGCHAIN_TRACING_V2=true` (not "false" or commented out)
3. Restart the app after changing `.env`

### No Traces Appearing in Dashboard

**Check:**
1. API key is correct in `.env`
2. Project name matches: `LANGCHAIN_PROJECT=care-assistant`
3. Internet connection is working
4. Check terminal for LangSmith errors

### "Authentication Failed" Error

**Solution:**
1. API key might be invalid or expired
2. Generate a new API key in LangSmith settings
3. Update `.env` with new key
4. Restart the app

### App Crashes When Offline

This shouldn't happen! The app includes **offline resilience**:
- If LangSmith can't connect, it logs a warning and continues
- Local traces still work in draggable windows
- No functionality is lost

If crashes occur, please report this as a bug.

### Seeing Duplicate Traces

This might happen if:
- Multiple browsers are open
- App restarted frequently during development

**Normal behavior** - LangSmith captures every execution.

---

## Disabling LangSmith

LangSmith is **optional**. To disable:

### Option 1: Edit .env
```bash
LANGCHAIN_TRACING_V2=false
```

### Option 2: Delete .env
```bash
rm .env
```

### Option 3: Comment out in .env
```bash
# LANGCHAIN_TRACING_V2=true
```

The app works perfectly without LangSmith - local observability windows continue functioning!

---

## Best Practices

### During Development
- ✅ Keep LangSmith enabled for detailed debugging
- ✅ Use metadata to filter your sessions
- ✅ Review traces to understand agent behavior

### For Learning
- ✅ Compare local traces vs. LangSmith traces
- ✅ Study token usage patterns
- ✅ Analyze tool call sequences
- ✅ Experiment with different prompts

### Security
- ❌ **Never** commit `.env` to git (already in `.gitignore`)
- ❌ **Never** share your API key publicly
- ❌ **Never** hardcode API keys in source code
- ✅ **Always** use environment variables for secrets

---

## Resources

- **LangSmith Docs**: https://docs.smith.langchain.com/
- **LangSmith Dashboard**: https://smith.langchain.com/
- **LangChain Docs**: https://python.langchain.com/docs/langsmith/
- **CARE Assistant**: Local draggable observability windows

---

## Summary

LangSmith adds **professional-grade observability** to CARE Assistant:

| Feature | Local Windows | LangSmith |
|---------|---------------|-----------|
| Real-time | ✅ | ✅ |
| Persistent History | ❌ | ✅ |
| Token Tracking | ❌ | ✅ |
| Search/Filter | ❌ | ✅ |
| Multi-Session View | ❌ | ✅ |
| Cost Analysis | ❌ | ✅ |
| Setup Required | None | Free account |

**Use both for best results!** 🚀
