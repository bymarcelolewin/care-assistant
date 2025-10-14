# Version Tasklist – v0.1.0 - Environment & Foundation
This document outlines all the tasks to work on to deliver this particular version, grouped by phases.

| Status |      |
|--------|------|
| 🔴 | Not Started |
| 🟡 | In Progress |
| 🟢 | Completed |


## Phase 1: Environment Setup

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| T1.1 | Create Virtual Environment | Use `uv venv` to create isolated Python environment | None | 🟢 Completed | AGENT |
| T1.2 | Activate Virtual Environment | Activate venv with `source .venv/bin/activate` | T1.1 | 🟢 Completed | USER |
| T1.3 | Install Core Dependencies | Install LangGraph, LangChain, LangChain-Community via uv | T1.2 | 🟢 Completed | AGENT |
| T1.4 | Install Web Dependencies | Install FastAPI, Uvicorn, Pydantic via uv | T1.2 | 🟢 Completed | AGENT |
| T1.5 | Verify Dependencies | Test imports for all installed packages | T1.3, T1.4 | 🟢 Completed | AGENT |


## Phase 2: Project Structure

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| T2.1 | Create app/ Directory | Create main application directory | None | 🟢 Completed | AGENT |
| T2.2 | Create Subdirectories | Create app/data/, app/tools/, app/graph/, app/api/, app/static/ | T2.1 | 🟢 Completed | AGENT |
| T2.3 | Create __init__.py Files | Add __init__.py to make directories Python packages | T2.2 | 🟢 Completed | AGENT |
| T2.4 | Create main.py | Create application entry point at app/main.py | T2.2 | 🟢 Completed | AGENT |


## Phase 3: Mock Data Creation

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| T3.1 | Design User Profile Schema | Define structure for user profiles (id, name, plan, coverage, etc.) | T2.2 | 🟢 Completed | AGENT |
| T3.2 | Create User Profiles JSON | Generate 3 diverse user profiles with realistic data | T3.1 | 🟢 Completed | AGENT |
| T3.3 | Design Insurance Plan Schema | Define structure for insurance plans (plan_id, type, coverage details) | T2.2 | 🟢 Completed | AGENT |
| T3.4 | Create Insurance Plans JSON | Generate 3 plan types (PPO, HMO, EPO) with coverage details | T3.3 | 🟢 Completed | AGENT |
| T3.5 | Design Claims Schema | Define structure for claims (claim_id, user_id, status, amounts) | T2.2 | 🟢 Completed | AGENT |
| T3.6 | Create Claims Data JSON | Generate sample claims for all 3 users (mix of statuses) | T3.5, T3.2 | 🟢 Completed | AGENT |
| T3.7 | Create Data Loader Module | Write Python module to load JSON files into memory | T3.2, T3.4, T3.6 | 🟢 Completed | AGENT |


## Phase 4: Basic FastAPI Server

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| T4.1 | Initialize FastAPI App | Create basic FastAPI application instance in main.py | T2.4 | 🟢 Completed | AGENT |
| T4.2 | Add Health Check Endpoint | Create GET /health endpoint returning status | T4.1 | 🟢 Completed | AGENT |
| T4.3 | Add Data Load on Startup | Load mock data when server starts | T3.7, T4.1 | 🟢 Completed | AGENT |
| T4.4 | Configure CORS | Set up CORS middleware for local development | T4.1 | 🟢 Completed | AGENT |
| T4.5 | Test Server Locally | Run uvicorn and verify server starts without errors | T4.2, T4.3, T4.4 | 🟢 Completed | USER/AGENT |


## Phase 5: Ollama Integration Verification

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| T5.1 | Check Ollama Service | Verify Ollama is running with `ollama list` | None | 🟢 Completed | AGENT |
| T5.2 | Verify Model Available | Confirm llama3.3:70b-instruct-q4_K_S is installed | T5.1 | 🟢 Completed | AGENT |
| T5.3 | Create Ollama Test Script | Write Python script to test LangChain Ollama integration | T1.5 | 🟢 Completed | AGENT |
| T5.4 | Test LLM Connection | Run test script and verify successful connection | T5.2, T5.3 | 🟢 Completed | AGENT |
| T5.5 | Test Simple Prompt | Send test prompt to Ollama and verify response | T5.4 | 🟢 Completed | AGENT |


## Phase 6: Documentation & Testing

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| T6.1 | Add Code Comments | Add explanatory comments throughout all code files | T3.7, T4.4, T5.5 | 🟢 Completed | AGENT |
| T6.2 | Create README for app/ | Write setup and usage instructions for the application | T4.5 | 🟢 Completed | AGENT |
| T6.3 | Document Mock Data Structure | Add comments in JSON files explaining the schema | T3.2, T3.4, T3.6 | 🟢 Completed | AGENT |
| T6.4 | End-to-End Verification | Test complete setup: venv, deps, server, data, Ollama | All previous | 🟢 Completed | USER/AGENT |
| T6.5 | Create .gitignore | Add .gitignore to exclude .venv/, __pycache__, etc. | None | 🟢 Completed | AGENT |
