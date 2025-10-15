# Version Design Document: v0.3.0 - Web Interface
Technical implementation and design guide for the upcoming version.

## 1. Features Summary
_Overview of features included in this version._

This version builds a modern web-based user interface for the CARE Assistant, bringing all v0.2.0 CLI functionality to a polished web experience. It includes:

1. **Next.js Project Setup** - Initialize Next.js with TypeScript, shadcn/ui components, and Tailwind CSS
2. **Chat UI with shadcn/ui** - Build chat interface using shadcn/ui components (Card, ScrollArea, Input, Button)
3. **Conversational User Identification** - AI greets with "What's your name?" - user types name (matching v0.2.0 CLI behavior)
4. **Message Send/Receive** - Implement message submission and real-time response display
5. **Developer Panel UI** - Create VS Code-style bottom panel for trace + state visualization (collapsible)
6. **Execution Trace Display** - Display execution trace in developer panel using shadcn/ui components
7. **State Visualization** - Show current conversation state in developer panel (user profile, tool results, context)
8. **POST /chat Endpoint** - Create FastAPI endpoint that accepts messages, invokes agent, returns response + trace + state
9. **WebSocket Streaming (Optional)** - Implement WebSocket for streaming LLM responses token-by-token
10. **Session Management** - Maintain conversation state across HTTP requests using session IDs
11. **Static Frontend Serving** - Configure FastAPI to serve Next.js build output
12. **Multi-Tool Response Display** - Properly display responses from multiple tool calls in single turn
13. **Error Handling UI** - User-friendly error messages when Ollama fails or tools error
14. **Loading States** - Show loading indicators during LLM processing and tool execution
15. **End-to-End Web Test** - Test complete flow: name entry → conversation → tool calls → trace visibility

**Success Criteria:**
- User can open browser, see chat interface, and interact with agent
- Conversational user identification works (AI asks "What's your name?")
- All v0.2.0 functionality works: LLM-based orchestration, multi-tool handling, state management
- Developer panel shows execution trace and state in real-time
- Session persists across page refreshes
- Clean, professional UI using shadcn/ui components
- Desktop-optimized (no mobile/responsive requirements)

## 2. Technical Architecture Overview
_High-level technical structure that supports all features in this version._

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser (Desktop)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Next.js Frontend (React + TypeScript)          │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │      Main Chat Window (shadcn/ui Components)     │  │ │
│  │  │  - Card (message containers)                     │  │ │
│  │  │  - ScrollArea (auto-scroll container)            │  │ │
│  │  │  - Input (user input field)                      │  │ │
│  │  │  - Button (send button)                          │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │   Developer Panel (Collapsible, bottom)          │  │ │
│  │  │  - Tabs (trace/state switcher)                   │  │ │
│  │  │  - Collapsible (execution details)               │  │ │
│  │  │  - Badge (node status indicators)                │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Python)                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  API Endpoints:                                        │ │
│  │  - POST /api/chat (send message, get response)        │ │
│  │  - WS /api/chat/stream (optional streaming)           │ │
│  │  - GET /api/session/:id (retrieve session state)      │ │
│  │  - GET / (serve Next.js static files)                 │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Session Manager (In-Memory Store)                     │ │
│  │  - session_id → ConversationState mapping             │ │
│  │  - TTL-based cleanup (30 min inactivity)              │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  LangGraph Agent (from v0.2.0)                         │ │
│  │  - identify_user → orchestrator → generate_response   │ │
│  │  - Tools: coverage_lookup, benefit_verify, claims     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

**Frontend:**
- **Next.js 14+** - React framework with App Router
- **TypeScript** - Type safety throughout
- **shadcn/ui** - Beautifully designed, customizable React components
- **Tailwind CSS** - Utility-first styling (required by shadcn/ui)
- **React Hooks** - State management (useState, useEffect, useContext)
- **Fetch API** - HTTP communication with FastAPI

**Backend:**
- **FastAPI** - Existing Python web framework
- **Session Management** - In-memory dict with session_id keys
- **LangGraph Agent** - Reuse existing v0.2.0 implementation (no changes)
- **Static File Serving** - Serve Next.js build output from `/out` or `/dist`

**Development:**
- **Next.js Dev Server** - `npm run dev` (port 3000)
- **FastAPI Dev Server** - `uvicorn app.main:app --reload` (port 8000)
- **CORS** - Enable cross-origin requests during development

**Production:**
- **Next.js Build** - `npm run build` → static export
- **FastAPI Serves Frontend** - Mount static files at root `/`
- **Single Server** - Port 8000 serves both API and frontend

### Component Architecture

**Frontend Structure:**
```
frontend/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Main chat page
│   └── api/                    # (optional) Next.js API routes
├── components/
│   ├── chat/
│   │   ├── ChatWindow.tsx      # Main chat container
│   │   ├── MessageList.tsx     # Message history display
│   │   ├── MessageInput.tsx    # User input field
│   │   └── LoadingIndicator.tsx
│   ├── developer/
│   │   ├── DeveloperPanel.tsx  # Collapsible panel
│   │   ├── TraceView.tsx       # Execution trace
│   │   └── StateView.tsx       # State visualization
│   └── ui/                     # shadcn/ui components
│       ├── card.tsx
│       ├── scroll-area.tsx
│       ├── input.tsx
│       ├── button.tsx
│       ├── tabs.tsx
│       ├── collapsible.tsx
│       └── badge.tsx
├── lib/
│   ├── api.ts                  # API client functions
│   └── types.ts                # TypeScript interfaces
└── public/                     # Static assets
```

**Backend Changes:**
```
app/
├── main.py                     # Update: add /api/chat endpoint + static serving
├── api/
│   ├── __init__.py
│   ├── chat.py                 # NEW: Chat endpoint logic
│   └── sessions.py             # NEW: Session management
├── graph/                      # UNCHANGED from v0.2.0
│   ├── state.py
│   ├── nodes.py
│   ├── edges.py
│   └── graph.py
└── tools/                      # UNCHANGED from v0.2.0
    ├── coverage.py
    ├── benefits.py
    └── claims.py
```

### Data Flow

**1. Initial Load:**
```
User → Browser → GET / → FastAPI → Serve Next.js HTML
                                  → Frontend loads
                                  → Create session_id (UUID)
                                  → Store in localStorage
```

**2. User Sends Message:**
```
User types message → MessageInput
                  → POST /api/chat {session_id, message}
                  → FastAPI receives request
                  → Lookup session state (or create new)
                  → Invoke LangGraph agent with state
                  → Agent executes (identify_user → orchestrator → generate_response)
                  → Return {response, trace, state, session_id}
                  → Frontend receives response
                  → Update MessageList with new message
                  → Update DeveloperPanel with trace/state
```

**3. Session Persistence:**
- `session_id` stored in browser localStorage
- Every request includes `session_id` in body
- Backend maintains `sessions: Dict[str, ConversationState]`
- TTL cleanup removes inactive sessions after 30 minutes

### UI Layout

```
┌────────────────────────────────────────────────────┐
│  CARE Assistant              [Clear Conversation]  │ <- Header
├────────────────────────────────────────────────────┤
│                                                    │
│  AI: Hello! I'm your CARE insurance assistant.    │
│      What's your name?                             │
│                                                    │
│  User: Sarah                                       │
│                                                    │
│  AI: Hi Sarah! I found your account. How can      │
│      I help you today?                             │
│                                                    │
│  User: What's my deductible and do I have any     │
│       outstanding claims?                          │
│                                                    │
│  AI: [Loading...]                                  │ <- Main Chat Window
│                                                    │
│                                                    │ (shadcn/ui: ScrollArea,
│                                                    │  Card, Input, Button)
│                                                    │
│                                                    │
│                                                    │
│                                                    │
├────────────────────────────────────────────────────┤
│  Type your message...                      [Send]  │ <- Input (ShadCN AI: Prompt Input)
├────────────────────────────────────────────────────┤
│  🔧 Developer Panel                    [▼ Collapse]│ <- Developer Panel Header
│  ┌────────────────────────────────────────────┐  │
│  │ Execution Trace │ State                    │  │ <- Tabs
│  ├────────────────────────────────────────────┤  │
│  │ ✓ identify_user (12:34:56)               │  │
│  │   → User identified: Sarah (user_003)     │  │
│  │                                            │  │
│  │ ✓ orchestrator (12:34:57)                 │  │ <- Developer Panel Content
│  │   → Tools selected: coverage_lookup,      │  │ (shadcn/ui: Tabs, Collapsible,
│  │     claims_status                          │  │  Badge)
│  │                                            │  │
│  │ ✓ generate_response (12:34:59)            │  │
│  │   → Response generated                     │  │
│  └────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

## 3. Implementation Notes
_Shared technical considerations across all features in this version._

### shadcn/ui Component Integration

**Installation:**
```bash
# Create Next.js project with TypeScript and Tailwind
npx create-next-app@latest frontend --typescript --tailwind --app

cd frontend

# Initialize shadcn/ui (will prompt for configuration)
npx shadcn@latest init

# Add required components
npx shadcn@latest add card scroll-area input button tabs collapsible badge
```

**Usage Pattern:**
```tsx
import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

<ScrollArea className="h-[600px]">
  {messages.map(msg => (
    <Card key={msg.id} className={msg.role === 'user' ? 'user-message' : 'ai-message'}>
      <CardContent>
        <p>{msg.content}</p>
      </CardContent>
    </Card>
  ))}
</ScrollArea>

<div className="flex gap-2">
  <Input placeholder="Type your message..." value={input} onChange={e => setInput(e.target.value)} />
  <Button onClick={handleSend}>Send</Button>
</div>
```

### Session Management Implementation

**Backend (app/api/sessions.py):**
```python
from typing import Dict
from datetime import datetime, timedelta
from uuid import uuid4

# In-memory session store
sessions: Dict[str, Dict] = {}

def create_session() -> str:
    session_id = str(uuid4())
    sessions[session_id] = {
        "state": {
            "messages": [],
            "user_id": None,
            "user_profile": None,
            "conversation_context": {},
            "tool_results": {},
            "execution_trace": []
        },
        "last_activity": datetime.now()
    }
    return session_id

def get_session(session_id: str) -> Dict:
    if session_id in sessions:
        sessions[session_id]["last_activity"] = datetime.now()
        return sessions[session_id]["state"]
    else:
        # Create new session if not found
        return create_session()

def cleanup_sessions():
    # Remove sessions inactive for > 30 minutes
    cutoff = datetime.now() - timedelta(minutes=30)
    expired = [sid for sid, data in sessions.items()
               if data["last_activity"] < cutoff]
    for sid in expired:
        del sessions[sid]
```

**Frontend (lib/api.ts):**
```typescript
export async function sendMessage(message: string): Promise<ChatResponse> {
  const sessionId = localStorage.getItem('sessionId') || '';

  const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message })
  });

  const data = await response.json();

  // Store session ID from first response
  if (!sessionId && data.session_id) {
    localStorage.setItem('sessionId', data.session_id);
  }

  return data;
}
```

### FastAPI Integration

**POST /api/chat Endpoint:**
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.graph.graph import create_graph
from app.api.sessions import get_session, create_session

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    trace: List[Dict]
    state: Dict

@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Get or create session
    session_id = request.session_id or create_session()
    state = get_session(session_id)

    # Add user message to state
    state["messages"].append(HumanMessage(content=request.message))

    # Invoke LangGraph agent
    graph = create_graph()
    result = await graph.ainvoke(state)

    # Update session state
    sessions[session_id]["state"] = result

    # Extract response from last AI message
    ai_response = result["messages"][-1].content

    return ChatResponse(
        session_id=session_id,
        response=ai_response,
        trace=result["execution_trace"],
        state={
            "user_id": result.get("user_id"),
            "user_profile": result.get("user_profile"),
            "tool_results": result.get("tool_results", {})
        }
    )
```

**Static File Serving:**
```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Serve Next.js build output
app.mount("/assets", StaticFiles(directory="frontend/out/_next"), name="assets")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # Serve API routes normally
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404)

    # Serve index.html for all other routes
    return FileResponse("frontend/out/index.html")
```

### Developer Panel Implementation

**State Management:**
```typescript
// components/developer/DeveloperPanel.tsx
const [isOpen, setIsOpen] = useState(true);
const [activeTab, setActiveTab] = useState<'trace' | 'state'>('trace');
const [trace, setTrace] = useState<TraceEntry[]>([]);
const [state, setState] = useState<ConversationState | null>(null);

// Update when new response arrives
useEffect(() => {
  if (lastResponse) {
    setTrace(lastResponse.trace);
    setState(lastResponse.state);
  }
}, [lastResponse]);
```

**Collapsible Panel:**
```tsx
<div className={`developer-panel ${isOpen ? 'open' : 'closed'}`}>
  <div className="panel-header" onClick={() => setIsOpen(!isOpen)}>
    🔧 Developer Panel {isOpen ? '▼' : '▲'}
  </div>
  {isOpen && (
    <div className="panel-content">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="trace">Execution Trace</TabsTrigger>
          <TabsTrigger value="state">State</TabsTrigger>
        </TabsList>
        <TabsContent value="trace">
          <TraceView entries={trace} />
        </TabsContent>
        <TabsContent value="state">
          <StateView state={state} />
        </TabsContent>
      </Tabs>
    </div>
  )}
</div>
```

### Error Handling

**Frontend:**
```typescript
try {
  const response = await sendMessage(message);
  setMessages([...messages, response]);
} catch (error) {
  setError('Failed to send message. Is the server running?');
  // Show error toast/banner
}
```

**Backend:**
```python
@router.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # ... agent invocation
    except Exception as e:
        # Log error
        logger.error(f"Chat error: {str(e)}")

        # Return user-friendly error
        raise HTTPException(
            status_code=500,
            detail="Sorry, I encountered an error. Please try again."
        )
```

## 4. Other Technical Considerations
_Any other technical information that might be relevant to building this version._

### Development Workflow

**Two-Server Development:**
1. Terminal 1: `cd frontend && npm run dev` (Next.js on port 3000)
2. Terminal 2: `uvicorn app.main:app --reload` (FastAPI on port 8000)
3. Frontend proxies API requests to backend via `next.config.js`:
```javascript
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*'
      }
    ]
  }
}
```

**Production Build:**
1. `cd frontend && npm run build` → Creates optimized static export
2. `uvicorn app.main:app` → Serves both API and frontend on port 8000

### Performance Considerations

- **LLM Latency**: Ollama responses take 3-20 seconds. Show loading indicators.
- **Streaming (Optional)**: Implement WebSocket streaming for token-by-token display
- **Session Cleanup**: Run periodic cleanup every 5 minutes to remove expired sessions
- **Tool Results Caching**: Already implemented in v0.2.0 (tool_results in state)

### TypeScript Interfaces

```typescript
// lib/types.ts
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface TraceEntry {
  node: string;
  timestamp: string;
  action: string;
  details?: Record<string, any>;
}

export interface ConversationState {
  user_id: string | null;
  user_profile: UserProfile | null;
  tool_results: Record<string, any>;
}

export interface ChatResponse {
  session_id: string;
  response: string;
  trace: TraceEntry[];
  state: ConversationState;
}
```

### Styling Approach

- **shadcn/ui Components**: Pre-styled with Tailwind CSS, fully customizable
- **Custom Styles**: Minimal - only for layout (developer panel positioning, message alignment)
- **Theme**: Use shadcn/ui's default theme (can customize via `tailwind.config.ts`)
- **Desktop-Only**: Fixed width layout (1200px max-width), no mobile breakpoints
- **Component Customization**: shadcn/ui components are copied to your project, so you can modify them directly

## 5. Open Questions
_Unresolved technical or product questions affecting this version._

### ✅ Resolved Questions

**Q1: Should we use WebSocket streaming or simple HTTP?**
**A:** Start with HTTP POST (simpler). WebSocket streaming is optional (V3-9, Medium priority). Can add later if needed.

**Q2: How to handle session persistence across page refreshes?**
**A:** Use localStorage to store session_id. Backend maintains session state in memory. If session expires, user starts fresh conversation.

**Q3: What happens if user refreshes browser mid-conversation?**
**A:** Session_id persists in localStorage → backend retrieves existing state → conversation continues. If session expired (30 min), start new conversation.

**Q4: Should developer panel be open or closed by default?**
**A:** Closed by default. User can open when they want to see trace/state details.

**Q5: Should we show individual tool calls in the chat window, or only final response?**
**A:** Show friendly progress messages in conversational English while tools run. Examples: "Let me check your claims...", "Now let me check your coverage...". NOT technical messages like "tool_X called".

**Q6: How to display multi-tool responses clearly?**
**A:** Generate single cohesive response (LLM already does this in generate_response node). Keep v0.2.0 behavior.

**Q7: Should we add a "Clear conversation" button?**
**A:** Yes - add button that creates new session_id and clears localStorage to start fresh conversation.

**Q8: Error recovery - if tool fails, should agent continue or abort?**
**A:** Keep same behavior as v0.2.0 - agent continues with partial results, show error in developer panel trace.

**Q9: What does the Settings button in the header do?**
**A:** Removed for v0.3.0 (not needed yet). Header only includes "CARE Assistant" title and "Clear Conversation" button. Settings can be added in v1.0.0+ when we have actual settings to configure (model selection, theme, etc.).
