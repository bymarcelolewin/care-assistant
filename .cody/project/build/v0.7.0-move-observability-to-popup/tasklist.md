# Version Tasklist – v0.7.0 - Move Observability to Pop-up Window
This document outlines all the tasks to work on to deliver this particular version, grouped by phases.

| Status |      |
|--------|------|
| 🔴 | Not Started |
| 🟡 | In Progress |
| 🟢 | Completed |


## Phase 1: Setup & Dependencies

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 1.1 | Install react-draggable | Run `npm install react-draggable @types/react-draggable` | None | 🔴 Not Started | AGENT |
| 1.2 | Verify current graph implementation | Check how graph is currently rendered (LangGraph built-in vs custom) | None | 🔴 Not Started | AGENT |
| 1.3 | Review current observability panel code | Understand current implementation of Memory and Execution Steps tabs | None | 🔴 Not Started | AGENT |


## Phase 2: Extract Content Components

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 2.1 | Create MemoryContent.tsx | Extract Memory tab JSX into standalone component | 1.3 | 🔴 Not Started | AGENT |
| 2.2 | Create ExecutionStepsContent.tsx | Extract Execution Steps tab JSX into standalone component | 1.3 | 🔴 Not Started | AGENT |
| 2.3 | Create GraphContent.tsx | Extract/move graph visualization from /graph route into component | 1.2 | 🔴 Not Started | AGENT |
| 2.4 | Test extracted components | Verify each content component renders correctly with mock data | 2.1, 2.2, 2.3 | 🔴 Not Started | AGENT |


## Phase 3: Build Draggable Window Components

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 3.1 | Create DraggableMemoryWindow.tsx | Build draggable window wrapper with header "Memory" and close button | 1.1, 2.1 | 🔴 Not Started | AGENT |
| 3.2 | Create DraggableGraphWindow.tsx | Build draggable window wrapper with header "Graph" and close button | 1.1, 2.3 | 🔴 Not Started | AGENT |
| 3.3 | Create DraggableStepsWindow.tsx | Build draggable window wrapper with header "Steps" and close button | 1.1, 2.2 | 🔴 Not Started | AGENT |
| 3.4 | Implement staggered initial positions | Set default positions (staggered cascade: top-left with offsets) | 3.1, 3.2, 3.3 | 🔴 Not Started | AGENT |
| 3.5 | Add bounds to draggable windows | Ensure windows stay within viewport using bounds="parent" | 3.1, 3.2, 3.3 | 🔴 Not Started | AGENT |
| 3.6 | Implement z-index management | Add click-to-bring-to-front functionality for overlapping windows | 3.1, 3.2, 3.3 | 🔴 Not Started | AGENT |


## Phase 4: Update Main Chat Page

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 4.1 | Remove bottom observability panel | Delete entire bottom panel component from main chat page | None | 🔴 Not Started | AGENT |
| 4.2 | Add state management for three windows | Add useState for showMemory, showGraph, showSteps | 4.1 | 🔴 Not Started | AGENT |
| 4.3 | Add checkbox controls to header | Create three checkboxes (Memory, Graph, Steps) in chat header | 4.2 | 🔴 Not Started | AGENT |
| 4.4 | Replace "View Graph" button | Remove existing button, position checkboxes in its place | 4.3 | 🔴 Not Started | AGENT |
| 4.5 | Conditionally render draggable windows | Show/hide windows based on checkbox state | 3.1, 3.2, 3.3, 4.2 | 🔴 Not Started | AGENT |
| 4.6 | Pass data props to windows | Connect observability data (memory, graph, trace) to window components | 4.5 | 🔴 Not Started | AGENT |


## Phase 5: Styling & Polish

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 5.1 | Style window containers | Apply rounded borders, shadows, white background matching chat window | 3.1, 3.2, 3.3 | 🔴 Not Started | AGENT |
| 5.2 | Style window headers | Add drag handle styling with slightly darker background | 5.1 | 🔴 Not Started | AGENT |
| 5.3 | Style close buttons | Add hover effects and proper positioning for close buttons | 5.1 | 🔴 Not Started | AGENT |
| 5.4 | Set window sizes | Apply fixed sizes (Memory: 400x500, Graph: 500x600, Steps: 600x700) | 5.1 | 🔴 Not Started | AGENT |
| 5.5 | Add minimum size constraints | Set min-width and min-height to prevent collapsing | 5.4 | 🔴 Not Started | AGENT |
| 5.6 | Style checkbox controls | Ensure checkboxes align properly in header with labels | 4.3 | 🔴 Not Started | AGENT |


## Phase 6: Real-time Updates & Functionality

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 6.1 | Verify Memory updates in real-time | Test that Memory window updates as conversation progresses | 4.6 | 🔴 Not Started | AGENT |
| 6.2 | Verify Graph updates in real-time | Test that Graph window shows current execution path | 4.6 | 🔴 Not Started | AGENT |
| 6.3 | Verify Steps updates in real-time | Test that Execution Steps window updates with latest traces | 4.6 | 🔴 Not Started | AGENT |
| 6.4 | Test auto-scroll in Steps window | Ensure latest prompt appears on top with auto-scroll behavior | 6.3 | 🔴 Not Started | AGENT |
| 6.5 | Test window close functionality | Verify close buttons properly hide windows and update checkbox state | 4.5 | 🔴 Not Started | AGENT |
| 6.6 | Test checkbox toggle functionality | Verify checking/unchecking shows/hides corresponding windows | 4.5 | 🔴 Not Started | AGENT |


## Phase 7: Integration & Testing

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 7.1 | Test single window workflow | Open/close/drag each window individually | All previous | 🔴 Not Started | AGENT |
| 7.2 | Test multiple windows workflow | Open all three windows, arrange, interact with chat | All previous | 🔴 Not Started | AGENT |
| 7.3 | Test dragging behavior | Verify windows drag smoothly and stay within bounds | All previous | 🔴 Not Started | AGENT |
| 7.4 | Test z-index (window layering) | Click different windows to bring to front, verify stacking | All previous | 🔴 Not Started | AGENT |
| 7.5 | Test with actual conversation flow | Have full conversation, verify all observability data displays correctly | All previous | 🔴 Not Started | USER |
| 7.6 | Chrome Desktop compatibility check | Test in Chrome Desktop (latest) to ensure everything works | All previous | 🔴 Not Started | USER |
| 7.7 | Edge case testing | Test rapid window open/close, drag while chat is updating, etc. | All previous | 🔴 Not Started | AGENT |


## Phase 8: Cleanup & Documentation

| ID  | Task             | Description                             | Dependencies | Status | Assigned To |
|-----|------------------|-----------------------------------------|-------------|----------|--------|
| 8.1 | Remove /graph route | Delete or redirect /graph route since graph is now in window | 2.3 | 🔴 Not Started | AGENT |
| 8.2 | Remove old observability panel code | Clean up unused bottom panel components and related code | 4.1 | 🔴 Not Started | AGENT |
| 8.3 | Update code comments | Add comments explaining new draggable window architecture | All previous | 🔴 Not Started | AGENT |
| 8.4 | Verify no console errors | Check browser console for any warnings or errors | All previous | 🔴 Not Started | AGENT |
| 8.5 | Final code review | Review all changes for code quality and consistency | All previous | 🔴 Not Started | AGENT |


## Summary

**Total Tasks:** 47 tasks across 8 phases

**Phase Breakdown:**
- Phase 1: Setup & Dependencies (3 tasks)
- Phase 2: Extract Content Components (4 tasks)
- Phase 3: Build Draggable Window Components (6 tasks)
- Phase 4: Update Main Chat Page (6 tasks)
- Phase 5: Styling & Polish (6 tasks)
- Phase 6: Real-time Updates & Functionality (6 tasks)
- Phase 7: Integration & Testing (7 tasks)
- Phase 8: Cleanup & Documentation (5 tasks)

**Critical Path:**
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8

**Estimated Complexity:** Medium-High
- Involves extracting existing components
- Implementing new draggable window system
- Maintaining all real-time update functionality
- Ensuring smooth UX with multiple windows
