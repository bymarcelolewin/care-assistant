# Version Tasklist – v0.8.0 - Add LangSmith Observability

This document outlines all the tasks to work on to deliver this version, grouped by phases.

| Status |      |
|--------|------|
| 🔴 | Not Started |
| 🟡 | In Progress |
| 🟢 | Completed |


## Phase 1: Environment Setup & Dependencies

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 1.1 | Install LangSmith Package | Install langsmith via uv: `uv pip install langsmith` | None | � Completed | USER |
| 1.2 | Install python-dotenv | Install python-dotenv via uv: `uv pip install python-dotenv` | None | � Completed | USER |
| 1.3 | Verify Dependencies | Run `uv pip list | grep -E "(langsmith|dotenv)"` to confirm installation | 1.1, 1.2 | � Completed | USER |


## Phase 2: LangSmith Account Setup

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 2.1 | Create LangSmith Account | Sign up at https://smith.langchain.com/ (free tier) | None | � Completed | USER |
| 2.2 | Create Project | Create new project named "care-assistant" in LangSmith dashboard | 2.1 | � Completed | USER |
| 2.3 | Generate API Key | Get API key from Settings → API Keys in LangSmith dashboard | 2.1 | � Completed | USER |


## Phase 3: Environment Configuration Files

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 3.1 | Create .env.example | Create template file with dummy values for all LangSmith env vars | None | � Completed | AGENT |
| 3.2 | Update .gitignore | Add .env to .gitignore to prevent committing secrets | None | � Completed | AGENT |
| 3.3 | Create .env File | Copy .env.example to .env and add real API key | 2.3, 3.1 | � Completed | AGENT |
| 3.4 | Verify .gitignore | Run `git status` to ensure .env is not tracked | 3.2, 3.3 | 🟢 Completed | USER |


## Phase 4: Code Integration

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 4.1 | Import dotenv in main.py | Add `from dotenv import load_dotenv` at top of app/main.py | 1.2 | � Completed | AGENT |
| 4.2 | Load Environment Variables | Call `load_dotenv()` early in startup (before FastAPI app creation) | 4.1 | � Completed | AGENT |
| 4.3 | Add LangSmith Status Logging | Print LangSmith status (enabled/disabled, project name) in lifespan startup | 4.2 | � Completed | AGENT |
| 4.4 | Test Without .env | Remove .env temporarily and verify app still starts normally | 4.3 | 🟢 Completed | USER |
| 4.5 | Test With .env | Restore .env and verify LangSmith status shows "enabled" | 4.3, 3.3 | 🟢 Completed | USER |


## Phase 5: Add Trace Metadata & Error Handling

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 5.1 | Add Session Metadata | Include session_id in LANGCHAIN_METADATA env var for filtering | 4.2 | � Completed | AGENT |
| 5.2 | Add User Metadata | Include user_id (if identified) in trace metadata | 5.1 | � Completed | AGENT |
| 5.3 | Add Environment Tag | Tag traces with environment (dev/prod) for organization | 5.1 | � Completed | AGENT |
| 5.4 | Add Error Handling | Wrap agent invocation in try/except to catch LangSmith network errors | 4.2 | � Completed | AGENT |
| 5.5 | Add Token Tracking | Capture and log input/output token counts from LLM responses | 5.4 | � Completed | AGENT |


## Phase 6: Testing & Verification

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 6.1 | Test Basic Conversation | Start app with LangSmith enabled, send "Hello" message | 4.5 | � Completed | USER |
| 6.2 | Verify Trace in Dashboard | Check LangSmith dashboard for trace of test conversation | 6.1 | � Completed | USER |
| 6.3 | Test Multi-Tool Query | Ask complex question requiring multiple tools, verify all tool calls traced | 6.1 | � Completed | USER |
| 6.4 | Test User Identification | Test name extraction flow, verify trace shows LLM extraction step | 6.1 | � Completed | USER |
| 6.5 | Test Graceful Degradation | Disable LangSmith (LANGCHAIN_TRACING_V2=false), verify app works normally | 4.4 | 🟢 Completed | USER |
| 6.6 | Test Invalid API Key | Set invalid API key, verify app logs warning but continues | 6.5 | ⚪ Skipped | USER |
| 6.7 | Test Offline Mode | Disconnect internet, verify app continues working (LangSmith silently fails) | 6.5 | ⚪ Skipped | USER |
| 6.8 | Verify Local Traces Still Work | Confirm draggable observability windows still function correctly | 6.1 | � Completed | USER |
| 6.9 | Verify Token Tracking | Check logs for token counts after multi-turn conversation | 6.1 | � Completed | USER |


## Phase 7: Documentation

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 7.1 | Create LangSmith Setup Guide | Write detailed guide in .cody/project/library/docs/langsmith-setup.md | None | � Completed | AGENT |
| 7.2 | Update README - Prerequisites | Add LangSmith as optional prerequisite with link to signup | None | � Completed | AGENT |
| 7.3 | Update README - Installation | Add steps for creating .env file from .env.example | 3.1 | � Completed | AGENT |
| 7.4 | Update README - Benefits Section | Add section explaining LangSmith benefits for learning | None | � Completed | AGENT |
| 7.5 | Update README - Troubleshooting | Add LangSmith-specific troubleshooting (API key errors, etc.) | None | � Completed | AGENT |
| 7.6 | Add Screenshots to Guide | Capture screenshots of LangSmith dashboard showing traces (optional) | 7.1, 6.2 | ⚪ Skipped | USER |
| 7.7 | Update Dependencies Section | Document langsmith and python-dotenv in README tech stack | 1.3 | � Completed | AGENT |


## Phase 8: Final Review & Polish

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 8.1 | Review .env.example | Ensure all env vars have clear comments explaining purpose | 3.1 | � Completed | AGENT |
| 8.2 | Review Security | Double-check .env is in .gitignore and not committed | 3.4 | � Completed | AGENT |
| 8.3 | Test End-to-End | Full conversation flow with LangSmith enabled, review traces | 6.7 | 🟢 Completed | USER |
| 8.4 | Update Feature Backlog | Mark v0.8.0 as completed in feature-backlog.md | 8.3 | 🟢 Completed | AGENT |
| 8.5 | Update Plan.md | Add v0.8.0 milestone to plan.md with completion date | 8.3 | � Completed | AGENT |
| 8.6 | Create Retrospective | Document learnings and potential improvements | 8.3 | � Completed | AGENT |
| 8.7 | Update Release Notes | Add v0.8.0 entry to release-notes.md | 8.3 | � Completed | AGENT |


## Summary

**Total Tasks:** 45 tasks across 8 phases

**Phase Breakdown:**
- Phase 1: Environment Setup & Dependencies (3 tasks)
- Phase 2: LangSmith Account Setup (3 tasks)
- Phase 3: Environment Configuration Files (4 tasks)
- Phase 4: Code Integration (5 tasks)
- Phase 5: Add Trace Metadata & Error Handling (5 tasks) - **Required** (includes offline resilience)
- Phase 6: Testing & Verification (9 tasks)
- Phase 7: Documentation (7 tasks)
- Phase 8: Final Review & Polish (7 tasks)

**Estimated Completion Time:** 2-3 hours

**Key Decisions:**
- ✅ Custom metadata (session_id, user_id, environment)
- ✅ Token tracking (input/output counts)
- ✅ Offline resilience (try/except for network failures)
- ❌ No LangSmith UI documentation (focus on setup only)
- ⏭️  LangSmith observability window (deferred to v0.9.0)

**Critical Path:**
1. Install dependencies (Phase 1)
2. Create LangSmith account and get API key (Phase 2)
3. Configure environment files (Phase 3)
4. Integrate code (Phase 4)
5. Test thoroughly (Phase 6)
6. Document (Phase 7)
7. Final review (Phase 8)

**Optional Enhancements:**
- Phase 5 (Trace Metadata) can be skipped for basic integration
- Screenshots in Phase 7.6 are nice-to-have but not required
