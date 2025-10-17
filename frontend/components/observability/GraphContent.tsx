"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { RefreshCw } from "lucide-react"

interface GraphContentProps {
  /** Optional: Provide external control over loading state */
  externalLoading?: boolean
  /** Optional: Callback when graph is refreshed */
  onRefresh?: () => void
}

/**
 * GraphContent - Displays the LangGraph structure visualization
 *
 * This component was extracted from the /graph route page to be reusable in draggable windows.
 * It fetches and displays the PNG visualization of the LangGraph conversation flow.
 */
export function GraphContent({ externalLoading, onRefresh }: GraphContentProps) {
  const [imageUrl, setImageUrl] = useState<string>("")
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadGraph = async () => {
    setIsLoading(true)
    setError(null)

    try {
      // Add timestamp to prevent caching
      const timestamp = new Date().getTime()
      const url = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/graph?t=${timestamp}`

      // Verify the image loads
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error("Failed to load graph visualization")
      }

      setImageUrl(url)

      // Call external refresh callback if provided
      if (onRefresh) {
        onRefresh()
      }
    } catch (err) {
      console.error("Error loading graph:", err)
      setError(err instanceof Error ? err.message : "Failed to load graph visualization")
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadGraph()
  }, [])

  const loading = externalLoading !== undefined ? externalLoading : isLoading

  return (
    <div className="space-y-4">
      {/* Refresh Button */}
      <div className="flex justify-end">
        <Button
          variant="outline"
          size="sm"
          onClick={loadGraph}
          disabled={loading}
        >
          <RefreshCw className={`w-4 h-4 mr-2 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </Button>
      </div>

      {/* Graph Visualization */}
      {loading && (
        <div className="flex items-center justify-center py-20">
          <div className="text-center">
            <RefreshCw className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-4" />
            <p className="text-gray-600 text-sm">Loading graph visualization...</p>
          </div>
        </div>
      )}

      {error && (
        <div className="flex items-center justify-center py-20">
          <div className="text-center">
            <p className="text-red-600 mb-4 text-sm">{error}</p>
            <Button onClick={loadGraph} variant="outline" size="sm">
              Try Again
            </Button>
          </div>
        </div>
      )}

      {!loading && !error && imageUrl && (
        <div className="space-y-4">
          <div className="bg-white rounded-lg border border-gray-200 p-4 overflow-auto">
            <img
              src={imageUrl}
              alt="LangGraph Conversation Flow"
              className="max-w-full h-auto mx-auto"
            />
          </div>

          {/* Graph Description */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h2 className="text-sm font-semibold text-blue-900 mb-2">
              About This Graph
            </h2>
            <p className="text-blue-800 text-xs mb-3">
              This visualization shows the LangGraph conversation flow for the CARE Assistant.
              The graph illustrates how messages are processed through different nodes:
            </p>
            <ul className="space-y-2 text-xs text-blue-800">
              <li className="flex items-start">
                <span className="font-semibold mr-2">1.</span>
                <span>
                  <strong>identify_user:</strong> Identifies the user and retrieves their profile
                </span>
              </li>
              <li className="flex items-start">
                <span className="font-semibold mr-2">2.</span>
                <span>
                  <strong>orchestrate_tools:</strong> Uses LLM to intelligently call the appropriate tools
                  (coverage lookup, benefit verification, claims status)
                </span>
              </li>
              <li className="flex items-start">
                <span className="font-semibold mr-2">3.</span>
                <span>
                  <strong>generate_response:</strong> Synthesizes tool results into a natural language response
                </span>
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
