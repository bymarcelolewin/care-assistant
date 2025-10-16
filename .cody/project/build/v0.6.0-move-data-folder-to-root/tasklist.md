# Version Tasklist – v0.6.0-move-data-folder-to-root
This document outlines all the tasks to work on to delivery this particular version, grouped by phases.

| Status |      |
|--------|------|
| 🔴 | Not Started |
| 🟡 | In Progress |
| 🟢 | Completed |


## Phase 1: Preparation and Analysis

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| P1-1 | Verify Current Structure | Confirm all JSON files in /app/data/ and list Python files that will remain | None | 🟢 Completed | AGENT |
| P1-2 | Search for Hardcoded Paths | Search codebase for any hardcoded references to /app/data/*.json files | None | 🟢 Completed | AGENT |
| P1-3 | Review loader.py Logic | Understand current path resolution in loader.py | None | 🟢 Completed | AGENT |


## Phase 2: Create New Structure

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| P2-1 | Create Root Data Folder | Create new /data folder at project root level | None | 🟢 Completed | AGENT |
| P2-2 | Move user_profiles.json | Move user_profiles.json from /app/data/ to /data/ | P2-1 | 🟢 Completed | AGENT |
| P2-3 | Move insurance_plans.json | Move insurance_plans.json from /app/data/ to /data/ | P2-1 | 🟢 Completed | AGENT |
| P2-4 | Move claims_data.json | Move claims_data.json from /app/data/ to /data/ | P2-1 | 🟢 Completed | AGENT |


## Phase 3: Update Code References

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| P3-1 | Update DATA_DIR in loader.py | Change DATA_DIR from Path(__file__).parent to Path(__file__).parent.parent.parent / "data" | P2-2, P2-3, P2-4 | 🟢 Completed | AGENT |
| P3-2 | Update Docstring in loader.py | Update module docstring to reflect new data file locations if needed | P3-1 | 🟢 Completed | AGENT |
| P3-3 | Fix Any Hardcoded Paths | Update any other code locations that reference old data folder path | P1-2, P3-1 | 🟢 Completed | AGENT |


## Phase 4: Testing

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| P4-1 | Test Data Loading | Run application and verify all three JSON files load successfully | P3-1, P3-2, P3-3 | 🟢 Completed | AGENT |
| P4-2 | Test Web Interface | Start web interface and verify it loads without errors | P4-1 | 🟢 Completed | USER |
| P4-3 | Test Agent Interactions | Test full conversation flow with user identification and tool calls | P4-2 | 🟢 Completed | USER |
| P4-4 | Verify No File Not Found Errors | Check logs and console for any file not found errors | P4-1, P4-2, P4-3 | 🟢 Completed | AGENT |


## Phase 5: Documentation

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| P5-1 | Update README.md | Update project structure section in README to show new /data folder | P4-4 | 🟢 Completed | AGENT |
| P5-2 | Check for Other Docs | Search for and update any other documentation mentioning data folder location | P5-1 | 🟢 Completed | AGENT |
| P5-3 | Update Plan.md if Needed | Update plan.md Environment Setup section if it mentions data folder | P5-2 | 🟢 Completed | AGENT |


## Phase 6: Final Verification

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| P6-1 | Final End-to-End Test | Complete application test from startup to conversation | P5-1, P5-2, P5-3 | 🟢 Completed | USER |
| P6-2 | Code Review | Review all changes to ensure clean implementation | P6-1 | 🟢 Completed | AGENT |
| P6-3 | Commit to Git | Commit all changes with descriptive message | P6-2 | 🟢 Completed | USER |


## Summary
- **Total Tasks:** 21
- **Phases:** 6
- **Estimated Complexity:** Low (primarily file moves and path updates)
- **Risk Level:** Low (straightforward refactoring with clear testing path)
