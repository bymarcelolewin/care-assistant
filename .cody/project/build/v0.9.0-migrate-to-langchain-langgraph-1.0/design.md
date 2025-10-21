# Migration Plan: v0.9.0 - Upgrade to LangChain 1.0 & LangGraph 1.0

**Version**: 0.9.0
**Date**: 2025-10-21
**Python Version**: 3.13 (Compatible ✓)

## Overview

Upgrade CARE Assistant from LangChain 0.3.27 and LangGraph 0.6.10 to the new stable 1.0 releases:
- **LangChain**: 0.3.27 → 1.0.2
- **LangGraph**: 0.6.10 → 1.0.1

## Migration Guide References

- **LangChain v1**: https://docs.langchain.com/oss/python/migrate/langchain-v1
- **LangGraph v1**: https://docs.langchain.com/oss/python/migrate/langgraph-v1

## Current State Analysis

### What We're Using (Current Versions)

```bash
langchain                0.3.27
langchain-community      0.3.31
langchain-core           0.3.79
langchain-ollama         0.3.10
langchain-text-splitters 0.3.11
langgraph                0.6.10
langgraph-checkpoint     2.1.2
langgraph-prebuilt       0.6.4
langgraph-sdk            0.2.9
```

### Target Versions

```bash
langchain                1.0.2   (latest)
langgraph                1.0.1   (latest)
langchain-core           1.x     (auto-updated)
langchain-community      1.x     (auto-updated)
langchain-ollama         1.x     (auto-updated)
```

## Compatibility Assessment

### ✅ Already Compatible

Our codebase is already following v1.0 best practices:

1. **TypedDict State** - `ConversationState` in [app/graph/state.py](../../app/graph/state.py) uses `TypedDict` ✓
2. **Custom StateGraph** - We build our own graph with custom nodes (not using deprecated prebuilt agents) ✓
3. **Modern Imports** - Already using `langchain_core` for messages and tools ✓
4. **No Legacy Chains** - Not using `LLMChain`, `ConversationChain`, or other deprecated chains ✓
5. **Python 3.13** - Exceeds the 3.10+ requirement ✓

### ⚠️ Potential Breaking Changes

Based on migration guides, watch for:

1. **Message API Changes**
   - `.text()` method → `.text` property
   - Need to search codebase for `.text()` usage

2. **Return Type Changes**
   - Chat model methods now return more specific types (`AIMessage` vs `BaseMessage`)
   - Should not affect us since we're already using proper types

3. **Content Blocks API**
   - New `.content_blocks` property for standardized access
   - We may want to use this for future enhancements

4. **langchain-ollama Compatibility**
   - Need to verify `ChatOllama` works with v1.0
   - This is our only external model integration

### 🚫 Not Affected By

These breaking changes **don't affect us**:

- ❌ `create_react_agent` deprecation (we don't use it)
- ❌ Pydantic state → TypedDict (already using TypedDict)
- ❌ Hooks → Middleware (we don't use hooks)
- ❌ Legacy chains (we don't use them)
- ❌ Hub functionality (we don't use it)

## Migration Steps

### Phase 1: Preparation

- [ ] **1.1** Verify Python version (3.10+)
  ```bash
  python --version  # Should show 3.13.x
  ```

- [ ] **1.2** Create git backup
  ```bash
  git add .
  git commit -m "Pre-migration checkpoint - v0.8.0 stable"
  git tag v0.8.0-pre-migration
  ```

- [ ] **1.3** Search for potential breaking changes
  ```bash
  # Search for .text() method usage
  grep -r "\.text()" app/ tests/

  # Search for deprecated imports
  grep -r "from langchain.chains" app/ tests/
  grep -r "create_react_agent" app/ tests/
  ```

### Phase 2: Package Upgrade

- [ ] **2.1** Upgrade langchain-core first (foundation)
  ```bash
  uv pip install -U langchain-core
  ```

- [ ] **2.2** Upgrade langgraph (depends on langchain-core)
  ```bash
  uv pip install -U langgraph
  ```

- [ ] **2.3** Upgrade langchain (main package)
  ```bash
  uv pip install -U langchain
  ```

- [ ] **2.4** Upgrade companion packages
  ```bash
  uv pip install -U langchain-community langchain-ollama
  ```

- [ ] **2.5** Verify installed versions
  ```bash
  uv pip list | grep -E "langchain|langgraph"
  ```

### Phase 3: Code Updates

- [ ] **3.1** Check for `.text()` method usage
  - **Files to check**: [app/graph/nodes.py](../../app/graph/nodes.py), [app/api/chat.py](../../app/api/chat.py)
  - **Change**: `message.text()` → `message.text`

- [ ] **3.2** Verify import statements still work
  ```bash
  python -c "
  from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
  from langchain_core.tools import tool
  from langchain_ollama import ChatOllama
  from langgraph.graph import StateGraph, END
  from langgraph.graph.message import add_messages
  print('✅ All imports successful!')
  "
  ```

- [ ] **3.3** Check TypedDict state definition (should be fine)
  - Review [app/graph/state.py](../../app/graph/state.py)
  - Ensure `ConversationState` still inherits from `TypedDict`

### Phase 4: Testing

- [ ] **4.1** Run Ollama integration test
  ```bash
  python tests/test_ollama.py
  ```

- [ ] **4.2** Run interactive CLI test
  ```bash
  python tests/test_agent.py
  ```
  - Test: User identification
  - Test: Single tool call (coverage lookup)
  - Test: Multi-tool call (complex question)
  - Test: General conversation

- [ ] **4.3** Start backend server
  ```bash
  uv run uvicorn app.main:app --port 8000
  ```
  - Verify: Server starts without errors
  - Verify: Data loads successfully (3 users, 3 plans, 9 claims)
  - Check: `/health` endpoint responds

- [ ] **4.4** Test API endpoints
  ```bash
  # Health check
  curl http://localhost:8000/health

  # Chat endpoint
  curl -X POST http://localhost:8000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"session_id": null, "message": "Hello"}'
  ```

- [ ] **4.5** Test frontend (full application)
  - Open: http://localhost:8000/
  - Test: User greeting and identification
  - Test: Single question (claims status)
  - Test: Complex multi-tool question
  - Test: Observability windows (Memory, Graph, Steps)
  - Test: Session persistence (refresh browser)

- [ ] **4.6** Test LangSmith integration (if configured)
  - Verify: Traces appear in LangSmith dashboard
  - Check: No connection errors in console

### Phase 5: Documentation

- [ ] **5.1** Update [README.md](../../README.md) version badge
  - Change: `version-0.8.0` → `version-0.9.0`

- [ ] **5.2** Update [README.md](../../README.md) architecture section
  - Update LangChain version: 0.3.x → 1.0.2
  - Update LangGraph version: 0.6.x → 1.0.1

- [ ] **5.3** Update installation instructions in README
  ```bash
  # Update these lines:
  uv pip install langgraph langchain langchain-ollama langchain-community
  # (versions will auto-install latest 1.x)
  ```

- [ ] **5.4** Create retrospective document
  - File: `.cody/project/build/v0.9.0-migrate-to-langchain-langgraph-1.0/retrospective.md`
  - Document: Issues encountered, solutions, lessons learned

- [ ] **5.5** Update release notes
  - File: `.cody/project/library/docs/release-notes.md`
  - Add v0.9.0 entry with migration details

### Phase 6: Final Verification

- [ ] **6.1** Run all tests one more time
  ```bash
  python tests/test_ollama.py
  python tests/test_agent.py
  ```

- [ ] **6.2** Full application smoke test
  - Start server
  - Test complete user journey
  - Verify all features work

- [ ] **6.3** Commit changes
  ```bash
  git add .
  git commit -m "v0.9.0 - Migrate to LangChain 1.0.2 & LangGraph 1.0.1"
  git tag v0.9.0
  ```

## Risk Assessment

### Low Risk ✅

- **Python 3.13**: Exceeds minimum requirement (3.10+)
- **Modern API usage**: Already using recommended patterns
- **No deprecated features**: Not using chains, prebuilt agents, or legacy APIs
- **LangGraph backwards compatibility**: Guide states "largely backwards compatible"

### Medium Risk ⚠️

- **langchain-ollama**: Integration with local Ollama might have changes
- **Message API**: Subtle changes in message object behavior
- **Dependency conflicts**: Multiple packages need to upgrade together

### Mitigation Strategies

1. **Git backup before starting**: Easy rollback if needed
2. **Upgrade in phases**: Core packages first, then dependencies
3. **Test after each phase**: Catch issues early
4. **Keep test suite**: Verify functionality throughout

## Success Criteria

Migration is successful when:

- ✅ All packages upgraded to 1.0.x versions
- ✅ `python tests/test_ollama.py` passes
- ✅ `python tests/test_agent.py` works correctly
- ✅ Backend server starts without errors
- ✅ Frontend application works (all features)
- ✅ Observability windows display correctly
- ✅ LangSmith tracing works (if configured)
- ✅ No console errors or warnings

## Rollback Plan

If migration fails:

```bash
# Restore from git tag
git reset --hard v0.8.0-pre-migration

# Reinstall previous versions
uv pip install langchain==0.3.27 langgraph==0.6.10 langchain-core==0.3.79

# Verify rollback
uv pip list | grep -E "langchain|langgraph"
python tests/test_ollama.py
```

## New Features Available in v1.0

After successful migration, we can explore:

1. **Content Blocks API**: Standardized access to reasoning, text, and other content types
2. **Improved Middleware**: Better reusability across agents
3. **Enhanced Structured Output**: New `ToolStrategy` and `ProviderStrategy` classes
4. **Stability Promise**: No breaking changes until 2.0

## References

- [LangChain v1 Migration Guide](https://docs.langchain.com/oss/python/migrate/langchain-v1)
- [LangGraph v1 Migration Guide](https://docs.langchain.com/oss/python/migrate/langgraph-v1)
- [LangChain 1.0 Announcement](https://blog.langchain.com/langchain-langchain-1-0-alpha-releases/)
- [LangChain Changelog](https://changelog.langchain.com/)

---

**Status**: Ready to execute
**Estimated Time**: 1-2 hours
**Assigned To**: Migration Team
**Priority**: Medium (not urgent, but good to stay current)
