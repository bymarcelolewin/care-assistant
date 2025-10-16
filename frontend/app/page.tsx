"use client"

import { useState, useEffect } from "react"
import { ChatHeader } from "@/components/chat/ChatHeader"
import { ChatWindow } from "@/components/chat/ChatWindow"
import { DeveloperPanel } from "@/components/developer/DeveloperPanel"
import { Message, TraceEntry, ConversationState } from "@/lib/types"
import { sendMessage, getSessionId, saveSessionId, clearSessionId } from "@/lib/api"

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [loadingMessage, setLoadingMessage] = useState("AI is thinking...")
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [trace, setTrace] = useState<TraceEntry[]>([])
  const [state, setState] = useState<ConversationState | null>(null)

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
    <div className="flex flex-col h-screen max-w-[1200px] mx-auto">
      <ChatHeader onClearConversation={handleClearConversation} />
      <div className="flex-1 overflow-hidden">
        <ChatWindow
          messages={messages}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          loadingMessage={loadingMessage}
        />
      </div>
      <DeveloperPanel trace={trace} state={state} messages={messages} />
    </div>
  )
}
