# Version Design Document: v0.4.0 - Observability Enhancements
Technical implementation and design guide for the upcoming version.

## 1. Features Summary
_Overview of features included in this version._

This version enhances the developer panel (now rebranded as "Observability") with improved terminology and better trace visibility. The key improvements include:

1. **Rebranding**: Change "🔧 Developer Panel" to "🔍 Observability"
2. **Better Terminology**:
   - "State" → "Memory" (more intuitive for users)
   - "Execution Trace" → "Execution Steps" (clearer language)
3. **Enhanced Trace Display**: Show user prompts alongside execution steps with visual distinction
4. **Improved Context**: Group execution steps by the user message that triggered them
5. **Visual Hierarchy**: Use darker background for user prompts to distinguish them from system steps
6. **Tab Styling Improvements**: Make active tabs more visually distinct with darker background and white text, remove rounded corners
7. **Fix Tool Results Display**: Investigate and fix why tool results are not showing in the Memory (State) tab

**Expected Outcome**: Users will have a clearer understanding of the execution flow by seeing their prompts in context with the resulting system steps.

## 2. Technical Architecture Overview
_High-level technical structure that supports all features in this version. May include information about the frontend stack, backend / api, authentication, database, deployment, etc._

**Frontend Stack**:
- React + Next.js 15 + TypeScript
- shadcn/ui components (Tabs, Collapsible, Badge)
- Tailwind CSS for styling

**Components to Modify**:
1. `frontend/components/developer/DeveloperPanel.tsx` - Panel header and tab labels
2. `frontend/components/developer/TraceView.tsx` - Trace display logic and UI
3. `frontend/lib/types.ts` - TypeScript interfaces (if needed)

**No Backend Changes Required**: The backend already provides all necessary data (trace entries with timestamps and user messages). All changes are purely frontend presentation layer.

## 3. Implementation Notes
_Shared technical considerations across all features in this version._

### DeveloperPanel.tsx Changes
- Update line 27: Change emoji from 🔧 to 🔍
- Update line 27: Change text from "Developer Panel" to "Observability"
- Update line 46: Change "Execution Trace" to "Execution Steps"
- Update line 47: Change "State" to "Memory"
- Update TabsList styling:
  - Remove rounded corners (`rounded-none` already applied, verify it's working)
  - Enhance active tab styling with darker background and white text
  - Current: subtle white background with shadow
  - Proposed: `data-[state=active]:bg-zinc-800 data-[state=active]:text-white` for stronger contrast

### TraceView.tsx Changes
- **Challenge**: The current `TraceView` component receives only `entries: TraceEntry[]` as props
- **Solution**: We need to also receive the messages array to display user prompts
- **Implementation**:
  1. Update `TraceViewProps` interface to accept `messages: Message[]`
  2. Create a new component `UserPromptDisplay` to show user messages with darker background
  3. Implement grouping logic to associate trace entries with the message that triggered them
  4. Render pattern: User Prompt → Trace Entries → User Prompt → Trace Entries...

### Data Flow Consideration
- The parent component that renders `<TraceView>` will need to pass both `trace` and `messages`
- Check `page.tsx` or `ChatWindow.tsx` to see where `DeveloperPanel` is rendered
- The messages array is already available in the parent component's state

### Styling Approach
- User prompts: `bg-slate-800` or `bg-zinc-900` (darker background)
- Execution steps: Keep current `bg-background` (lighter)
- Maintain existing collapsible functionality for trace entries
- Use consistent spacing and borders for visual hierarchy

### Tool Results Display Issue
- **Current Behavior**: The "Memory" (State) tab shows tool_results as empty `{}`
- **Investigation Needed**:
  1. Check if backend is properly populating `state.tool_results` in the response
  2. Verify that tool results are being included in the state after tool execution
  3. Check if tool results are being cleared too early (before frontend displays them)
- **Potential Causes**:
  - Tool results might be stored temporarily and cleared after response generation
  - Backend might not be including tool results in the returned state
  - State serialization might be dropping tool results
- **Solution**: Ensure tool results persist in state and are included in API response for frontend display

## 4. Other Technical Considerations
_Share any other technical information that might be relevant to building this version._

### TypeScript Type Safety
- Ensure all prop interfaces are updated correctly
- The `Message` interface already exists in `frontend/lib/types.ts`
- May need to import `Message` type into `TraceView.tsx`

### Grouping Algorithm
The trace entries don't explicitly reference which message triggered them, but we can infer this by:
- Sorting by timestamp (already sorted)
- Grouping consecutive trace entries that occur after a user message
- Using timestamp comparison to determine boundaries

### Backward Compatibility
- Changes are purely cosmetic/UX improvements
- No breaking changes to data structures
- No impact on backend API

### Testing Considerations
- Test with multiple user messages to ensure grouping works correctly
- Verify empty states (no messages, no trace entries)
- Check responsive behavior (if panel is narrow)
- Ensure collapsible trace entries still work

## 5. Open Questions
_Unresolved technical or product questions affecting this version._

1. **Grouping Strategy**: Should we show the user prompt above each group of trace entries, or inline? (Decision: Show above each group with darker background)
2. **Empty States**: What should we show if there's a user message but no trace entries? (Decision: Don't show the message if there are no associated trace entries)
3. **Timestamp Display**: Should we show the timestamp for user prompts? (Decision: Yes, keep consistent with trace entries)
4. **Message Filtering**: Should we show all messages or only user messages? (Decision: Only show user messages, not assistant responses)
5. **Tab Corner Styling**: shadcn/ui tabs component may have default rounded styling - need to verify override approach
6. **Tool Results Persistence**: Need to investigate backend to understand when/why tool results are cleared from state
