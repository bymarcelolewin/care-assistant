# Version Design Document: v0.7.0 - Move Observability to Pop-up Window

Technical implementation and design guide for the upcoming version.

## 1. Features Summary
_Overview of features included in this version._

This version transforms the observability experience by:

1. **Removing the bottom panel** - Eliminate the collapsible observability panel from the main chat page, giving full height to chat messages
2. **Creating three independent draggable windows** - Separate windows for Memory, Graph, and Execution Steps that users can:
   - Show/hide individually via checkboxes
   - Position anywhere on screen
   - Arrange to suit their workflow
3. **Checkbox controls** - Add three checkboxes in the chat header:
   - ☐ Memory
   - ☐ Graph
   - ☐ Steps
4. **Individual window features**:
   - **Memory Window**: User profile, tool results, conversation context
   - **Graph Window**: LangGraph node visualization
   - **Steps Window**: Execution trace (auto-scrolling, latest on top)
5. **Real-time updates** - All windows update live as user chats
6. **Professional styling** - Match rounded borders and design aesthetic of chat window
7. **Default state** - All windows closed by default; users opt-in to what they need

**Design Evolution:** Originally based on `.cody/project/library/assets/Observability UX Update.png`, evolved to three independent draggable windows for maximum flexibility.

## 2. Technical Architecture Overview
_High-level technical structure that supports all features in this version._

### Frontend Architecture

**Technology Stack:**
- React + Next.js 15 + TypeScript
- shadcn/ui components (Card, Checkbox)
- Tailwind CSS for styling
- react-draggable library for drag functionality

**Component Structure:**
```
/frontend/app/
├── page.tsx (main chat page)
│   ├── Remove: Observability bottom panel (entire panel component)
│   ├── Add: Three checkboxes in header (Memory, Graph, Steps)
│   └── Add: State management for three windows
├── components/
│   ├── DraggableMemoryWindow.tsx (NEW)
│   │   ├── Draggable container
│   │   ├── Header: "Memory" + close button
│   │   └── Content: Memory section (extracted from current tab)
│   ├── DraggableGraphWindow.tsx (NEW)
│   │   ├── Draggable container
│   │   ├── Header: "Graph" + close button
│   │   └── Content: Graph visualization (from /graph route)
│   ├── DraggableStepsWindow.tsx (NEW)
│   │   ├── Draggable container
│   │   ├── Header: "Steps" + close button
│   │   └── Content: Execution steps (extracted from current tab)
│   ├── MemoryContent.tsx (extracted from current Memory tab)
│   ├── GraphContent.tsx (move from /graph route)
│   └── ExecutionStepsContent.tsx (extracted from current Execution Steps tab)
```

### State Management

**Current State (to be removed):**
- Bottom panel collapsed/expanded state
- Active tab selection (Memory vs Execution Steps)

**New State:**
```typescript
const [showMemory, setShowMemory] = useState(false);
const [showGraph, setShowGraph] = useState(false);
const [showSteps, setShowSteps] = useState(false);
```

**No Position Persistence:**
- Window positions reset on page refresh
- Users reposition as needed each session

### Data Flow

```
Chat Page Component
    ↓ (observability data from API)
    ├→ DraggableMemoryWindow (when showMemory === true)
    │   └→ MemoryContent (receives memoryData)
    ├→ DraggableGraphWindow (when showGraph === true)
    │   └→ GraphContent (receives graphData)
    └→ DraggableStepsWindow (when showSteps === true)
        └→ ExecutionStepsContent (receives traceData)
```

## 3. Implementation Notes
_Shared technical considerations across all features in this version._

### Draggable Window Implementation

**Library:** `react-draggable`
- Install: `npm install react-draggable @types/react-draggable`
- Each window is an independent draggable component
- Set bounds to keep windows within viewport
- Each window has its own drag handle (header)

**Example Structure:**
```tsx
import Draggable from 'react-draggable';

function DraggableMemoryWindow({ onClose, data }) {
  return (
    <Draggable bounds="parent" handle=".drag-handle">
      <div className="draggable-window">
        <div className="drag-handle">
          <span>Memory</span>
          <button onClick={onClose}>✕</button>
        </div>
        <div className="window-content">
          <MemoryContent data={data} />
        </div>
      </div>
    </Draggable>
  );
}
```

### Window Layout

**Individual Window Styling:**
- Each window is independently sized (not grid-based)
- Default positions: Staggered to avoid overlap
- Users can arrange as needed

**Suggested Default Sizes:**
- Memory Window: 400px × 500px
- Graph Window: 500px × 600px
- Steps Window: 600px × 700px (larger for execution trace)

**Z-Index Management:**
- Click any window to bring it to front
- Use state to track active window and apply higher z-index

### Component Extraction

**From Current Implementation:**
1. Extract Memory tab JSX → `MemoryContent.tsx`
2. Extract Execution Steps tab JSX → `ExecutionStepsContent.tsx`
3. Move Graph page (`/graph`) → `GraphContent.tsx`
4. Wrap each in draggable window component
5. Maintain all existing props and data structures

### Header Checkbox Controls

**Implementation:**
```tsx
<div className="observability-controls">
  <span>Observability:</span>
  <Checkbox
    checked={showMemory}
    onCheckedChange={setShowMemory}
    label="Memory"
  />
  <Checkbox
    checked={showGraph}
    onCheckedChange={setShowGraph}
    label="Graph"
  />
  <Checkbox
    checked={showSteps}
    onCheckedChange={setShowSteps}
    label="Steps"
  />
</div>
```

**Placement:**
- Position in chat window header
- Replace current "View Graph" button
- Align with existing header elements

### Styling Consistency

**Match Chat Window:**
- Border radius: `rounded-lg` (8px)
- Border color: `border-gray-200`
- Background: `bg-white`
- Shadow: `shadow-lg` for window elevation

**Window Specific:**
- Header: Slightly darker background for drag handle visibility
- Close button: Top-right corner, hover effect
- Minimum size: Set min-width/min-height to prevent collapsing
- No backdrop overlay (windows float freely)

### Real-time Updates

**No Changes Required:**
- Current polling/WebSocket mechanism continues to work
- Parent component receives updates and passes to pop-up
- Pop-up re-renders when props change (standard React behavior)

## 4. Other Technical Considerations
_Shared any other technical information that might be relevant to building this version._

### Performance

**Considerations:**
- Pop-up rendering should not block chat UI
- Graph visualization may be heavy (SVG rendering)
- Consider lazy loading graph only when pop-up opens
- Debounce drag events to avoid excessive re-renders

### Accessibility

**Requirements:**
- Keyboard navigation: ESC to close, Tab to navigate sections
- ARIA labels for pop-up, sections, and close button
- Focus management: Return focus to button when closed
- Screen reader announcements for pop-up state changes

### Browser Compatibility

**Target Browser:**
- Chrome Desktop (latest) - PRIMARY TARGET
- This is a POC/experimental learning tool
- No cross-browser testing required for v0.7.0

**Out of Scope:**
- Mobile devices (not testing)
- Firefox, Safari, Edge (future consideration)
- Touch device drag behavior

### Graph Integration

**Current State:**
- Graph exists at `/graph` route
- Uses Mermaid or D3.js for visualization (verify current implementation)

**Migration:**
- Extract graph rendering logic into component
- Remove `/graph` route (or redirect to main page with pop-up open)
- Ensure graph scales properly in smaller container

## 5. Open Questions
_Unresolved technical or product questions affecting this version._

**All Questions Resolved:**

✅ **Window persistence:** No - positions reset each session
✅ **Default state:** All windows closed by default
✅ **Window titles:** Simple text (Memory, Graph, Steps) - no emojis
✅ **Checkbox labels:** Short form (Memory, Graph, Steps)
✅ **Select all option:** Not needed
✅ **Browser compatibility:** Chrome Desktop only (POC/experimental)
✅ **Mobile support:** Not in scope
✅ **Initial window positions:** Option A - Staggered cascade (top-left, offset down-right)
✅ **Graph rendering library:** Using LangGraph's built-in image generation (to be verified during implementation)
✅ **Resize functionality:** Fixed size for v0.7.0 (simpler POC implementation)
✅ **Animation:** None - instant show/hide (keeps it simple)
✅ **Real-time updates:** Yes - all windows update in real-time as user chats
✅ **Window collision:** User manages manually - no auto-positioning logic
