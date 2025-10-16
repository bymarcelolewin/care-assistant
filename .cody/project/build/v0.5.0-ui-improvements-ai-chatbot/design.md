# Version Design Document : v0.5.0-ui-improvements-ai-chatbot
Technical implementation and design guide for the upcoming version.

## 1. Features Summary
_Overview of features included in this version._

This version focuses on redesigning the chat window UI to create a more cohesive, polished, and modern user experience. The improvements include:

- **V5-1**: Outer container with gray rounded border for cohesive contained experience
- **V5-2**: Inner padding/buffer between chat content and outer border
- **V5-3**: Improved message bubble spacing with left/right margins
- **V5-4**: Redesigned input field with background color and stroke/border
- **V5-5**: Send button integrated inside the input field
- **V5-6**: Removal of separator line between messages and input area

**Reference Design:** `.cody/project/library/assets/Chat Window UX.png`

**Scope:** Chat window only. Observability panel updates are deferred to a future version.

## 2. Technical Architecture Overview
_High-level technical structure that supports all features in this version._

**Frontend Stack:**
- Next.js 15 with React and TypeScript
- Tailwind CSS for styling
- shadcn/ui components (Card, Input, Button, ScrollArea)

**Components to Modify:**
- `frontend/components/chat/ChatWindow.tsx` - Main chat container
- `frontend/components/chat/MessageList.tsx` - Message display and spacing
- `frontend/components/chat/MessageInput.tsx` - Input field and send button layout

**Styling Approach:**
- Use Tailwind utility classes for layout and spacing
- Maintain existing color scheme (slate-600 for user messages)
- Add rounded borders and proper padding throughout
- Ensure responsive design principles are maintained

## 3. Implementation Notes
_Shared technical considerations across all features in this version._

**ChatWindow.tsx Changes:**
- Wrap the entire chat window in a container div with rounded border and gray border color
- Add padding around the entire chat content area
- Remove the `border-t` class from the input area container

**MessageList.tsx Changes:**
- Add horizontal margins to the message container to prevent edge-to-edge display
- Adjust the ScrollArea padding to accommodate new spacing requirements
- Maintain existing message role-based styling (user vs assistant)

**MessageInput.tsx Changes:**
- Restructure component to place send button inside the input field
- Add border and background styling to input field container
- Use absolute/relative positioning or flexbox to position send button on the right inside the input
- Ensure input field placeholder text matches design: "Ask anything you like..."

**Design System Consistency:**
- Keep existing color variables and theme
- Maintain accessibility standards (contrast ratios, focus states)
- Preserve existing functionality (message sending, scrolling, loading states)

## 4. Other Technical Considerations
_Any other technical information that might be relevant to building this version._

**Browser Compatibility:**
- Test rounded borders and layout changes across major browsers
- Ensure flexbox/grid layouts work consistently

**Responsive Design:**
- Verify mobile/tablet layouts still work with new padding and margins
- Test that input field with embedded button works on smaller screens

**Performance:**
- No performance impact expected - only CSS/layout changes
- No new dependencies required

**Backward Compatibility:**
- No API changes required
- No data structure changes
- Purely presentational updates

## 5. Design Specifications
_Specific design values confirmed for implementation._

1. **User message bubble color**: `slate-600` with `text-white`

2. **Outer container border**: `border-gray-300` with `rounded-2xl`

3. **Spacing values**:
   - Inner padding (container): `p-6`
   - Message horizontal margins: `mx-6`
   - Standard Tailwind spacing scale throughout

4. **Input field styling**:
   - Background: `bg-gray-50`
   - Border: `border border-gray-300`
   - Rounded corners: `rounded-lg`
   - Send button (inside input): `bg-gray-400` or `bg-gray-500`
   - Placeholder text: "Ask anything you like..."
