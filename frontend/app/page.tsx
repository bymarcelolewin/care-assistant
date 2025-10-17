"use client"

import { useState, useEffect } from "react"
import { ChatHeader } from "@/components/chat/ChatHeader"
import { ChatWindow } from "@/components/chat/ChatWindow"
import { DraggableMemoryWindow } from "@/components/observability/DraggableMemoryWindow"
import { DraggableGraphWindow } from "@/components/observability/DraggableGraphWindow"
import { DraggableStepsWindow } from "@/components/observability/DraggableStepsWindow"
import { Message, TraceEntry, ConversationState } from "@/lib/types"
import { sendMessage, getSessionId, saveSessionId, clearSessionId } from "@/lib/api"

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [loadingMessage, setLoadingMessage] = useState("AI is thinking...")
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [trace, setTrace] = useState<TraceEntry[]>([])
  const [state, setState] = useState<ConversationState | null>(null)

  /**
   * Observability Window State Management (v0.7.0)
   *
   * Three independent draggable windows replace the bottom panel:
   * - Memory: Shows conversation state (user profile, tool results)
   * - Graph: Displays LangGraph structure visualization
   * - Steps: Shows execution trace (nodes visited, tools called)
   *
   * Each window can be toggled via checkboxes in the chat header.
   * Windows are draggable and open centered over the chat.
   * Windows support z-index layering (click to bring to front).
   *
   * Default: All windows closed on load
   */
  const [showMemory, setShowMemory] = useState(false)
  const [showGraph, setShowGraph] = useState(false)
  const [showSteps, setShowSteps] = useState(false)

  /**
   * Z-index Management for Window Layering
   *
   * When a window is clicked, it's brought to front by updating activeWindow.
   * Active window gets z-index 1000, others get 999.
   * This creates a simple click-to-front behavior for overlapping windows.
   */
  const [activeWindow, setActiveWindow] = useState<"memory" | "graph" | "steps" | null>(null)

  const getZIndex = (windowName: "memory" | "graph" | "steps") => {
    return activeWindow === windowName ? 1000 : 999
  }

  // Load session and get initial greeting on mount
  useEffect(() => {
    const storedSessionId = getSessionId()

    // Note: Backend session management is stateless (in-memory only)
    // We clear any stale session IDs and always start with a fresh greeting
    // Future enhancement: Implement session restoration from backend
    if (!storedSessionId) {
      handleInitialGreeting()
    } else {
      // Session exists in localStorage but messages aren't persisted
      // Clear the stale session and start fresh with greeting
      clearSessionId()
      setSessionId(null)
      handleInitialGreeting()
    }
  }, [])

  /**
   * Get initial greeting from the AI
   */
  const handleInitialGreeting = async () => {
    try {
      setIsLoading(true)
      const response = await sendMessage("Hello", null)

      // Save session ID
      saveSessionId(response.session_id)
      setSessionId(response.session_id)

      // Add AI greeting message
      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        role: "assistant",
        content: response.response,
        timestamp: new Date().toISOString(),
      }

      setMessages([aiMessage])

      // Update trace and state
      setTrace(response.trace)
      setState(response.state)
    } catch (error) {
      console.error("Failed to get initial greeting:", error)
      // Show error message
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: "assistant",
        content: "Sorry, I couldn't connect to the server. Please make sure the backend is running.",
        timestamp: new Date().toISOString(),
      }
      setMessages([errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Handle sending a message
   */
  const handleSendMessage = async (messageText: string) => {
    try {
      // Add user message to UI immediately
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        role: "user",
        content: messageText,
        timestamp: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, userMessage])
      setIsLoading(true)
      setLoadingMessage("AI is thinking...")

      // Send to backend
      const response = await sendMessage(messageText, sessionId)

      // Update session ID if it changed
      if (response.session_id !== sessionId) {
        saveSessionId(response.session_id)
        setSessionId(response.session_id)
      }

      // Show progress messages if available
      if (response.progress_messages && response.progress_messages.length > 0) {
        for (const progressMsg of response.progress_messages) {
          setLoadingMessage(progressMsg)
          // Small delay to show each progress message
          await new Promise((resolve) => setTimeout(resolve, 500))
        }
      }

      // Add AI response message
      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        role: "assistant",
        content: response.response,
        timestamp: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, aiMessage])

      // Update trace and state
      setTrace(response.trace)
      setState(response.state)
    } catch (error) {
      console.error("Failed to send message:", error)

      // Show error message
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: "assistant",
        content: error instanceof Error ? error.message : "Failed to send message. Please try again.",
        timestamp: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      setLoadingMessage("AI is thinking...")
    }
  }

  /**
   * Clear conversation and start fresh
   */
  const handleClearConversation = () => {
    clearSessionId()
    setSessionId(null)
    setMessages([])
    handleInitialGreeting()
  }

  return (
    <div className="flex flex-col h-screen max-w-[1200px] mx-auto p-6">
      <div className="flex-1 overflow-hidden border border-gray-300 rounded-2xl flex flex-col">
        <ChatHeader
          onClearConversation={handleClearConversation}
          showMemory={showMemory}
          showGraph={showGraph}
          showSteps={showSteps}
          onToggleMemory={() => setShowMemory(!showMemory)}
          onToggleGraph={() => setShowGraph(!showGraph)}
          onToggleSteps={() => setShowSteps(!showSteps)}
        />
        <div className="flex-1 overflow-hidden">
          <ChatWindow
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            loadingMessage={loadingMessage}
          />
        </div>
      </div>

      {/**
       * Draggable Observability Windows (v0.7.0)
       *
       * Three independent windows controlled by checkbox state:
       *
       * 1. Memory Window (400×500px at position 20, 100)
       *    - Displays conversation state (user profile, tool results)
       *    - Updates in real-time as conversation progresses
       *
       * 2. Graph Window (500×600px at position 440, 100)
       *    - Shows LangGraph structure visualization (Mermaid PNG)
       *    - Static display of agent's node/edge architecture
       *
       * 3. Steps Window (600×700px at position 960, 100)
       *    - Shows execution trace with nodes visited and tools called
       *    - Groups steps by triggering user message
       *    - Latest prompts appear on top (reverse chronological)
       *
       * All windows:
       * - Are draggable by header
       * - Stay within viewport bounds
       * - Support click-to-bring-to-front (z-index management)
       * - Have close buttons that update checkbox state
       * - Use react-draggable with nodeRef for React 18+ compatibility
       */}
      {showMemory && (
        <DraggableMemoryWindow
          state={state}
          onClose={() => setShowMemory(false)}
          onFocus={() => setActiveWindow("memory")}
          zIndex={getZIndex("memory")}
        />
      )}

      {showGraph && (
        <DraggableGraphWindow
          onClose={() => setShowGraph(false)}
          onFocus={() => setActiveWindow("graph")}
          zIndex={getZIndex("graph")}
        />
      )}

      {showSteps && (
        <DraggableStepsWindow
          entries={trace}
          messages={messages}
          onClose={() => setShowSteps(false)}
          onFocus={() => setActiveWindow("steps")}
          zIndex={getZIndex("steps")}
        />
      )}
    </div>
  )
}
