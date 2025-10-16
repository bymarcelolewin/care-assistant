/**
 * API Client for CARE Assistant Backend
 *
 * Handles all HTTP communication with the FastAPI backend.
 */

import { ChatRequest, ChatResponse } from "./types"

// API base URL - in development, this will be proxied by Next.js
// In production, use relative paths (same origin as the static files)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== 'undefined' && window.location.hostname !== 'localhost'
    ? ''
    : 'http://localhost:8000')

/**
 * Send a message to the chat API and get a response.
 *
 * @param message - User's message text
 * @param sessionId - Optional session ID for continuing conversations
 * @returns ChatResponse with AI response, trace, and state
 * @throws Error if the API request fails
 */
export async function sendMessage(
  message: string,
  sessionId?: string | null
): Promise<ChatResponse> {
  try {
    const request: ChatRequest = {
      session_id: sessionId || null,
      message: message
    }

    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      // Try to parse error response
      const errorData = await response.json().catch(() => ({
        detail: `HTTP ${response.status}: ${response.statusText}`
      }))

      throw new Error(errorData.detail || "Failed to send message")
    }

    const data: ChatResponse = await response.json()
    return data
  } catch (error) {
    console.error("API Error:", error)
    throw error
  }
}

/**
 * Get or create a session ID from localStorage.
 *
 * @returns Session ID string or null if not found
 */
export function getSessionId(): string | null {
  if (typeof window === "undefined") return null
  return localStorage.getItem("sessionId")
}

/**
 * Save session ID to localStorage.
 *
 * @param sessionId - Session ID to save
 */
export function saveSessionId(sessionId: string): void {
  if (typeof window === "undefined") return
  localStorage.setItem("sessionId", sessionId)
}

/**
 * Clear session ID from localStorage (for new conversations).
 */
export function clearSessionId(): void {
  if (typeof window === "undefined") return
  localStorage.removeItem("sessionId")
}

/**
 * Check if Ollama/Backend is available.
 *
 * @returns true if backend is healthy, false otherwise
 */
export async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
    })
    return response.ok
  } catch (error) {
    console.error("Backend health check failed:", error)
    return false
  }
}
