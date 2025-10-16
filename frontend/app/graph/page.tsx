"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import Link from "next/link"
import { ArrowLeft, RefreshCw } from "lucide-react"

export default function GraphPage() {
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

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/">
              <Button variant="outline" size="sm">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Chat
              </Button>
            </Link>
            <h1 className="text-2xl font-bold text-gray-900">
              Conversation Graph Structure
            </h1>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={loadGraph}
            disabled={isLoading}
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? "animate-spin" : ""}`} />
            Refresh
          </Button>
        </div>

        {/* Graph Visualization Card */}
        <Card className="p-6">
          {isLoading && (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <RefreshCw className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-4" />
                <p className="text-gray-600">Loading graph visualization...</p>
              </div>
            </div>
          )}

          {error && (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <p className="text-red-600 mb-4">{error}</p>
                <Button onClick={loadGraph} variant="outline">
                  Try Again
                </Button>
              </div>
            </div>
          )}

          {!isLoading && !error && imageUrl && (
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
                <h2 className="text-lg font-semibold text-blue-900 mb-2">
                  About This Graph
                </h2>
                <p className="text-blue-800 text-sm mb-3">
                  This visualization shows the LangGraph conversation flow for the CARE Assistant.
                  The graph illustrates how messages are processed through different nodes:
                </p>
                <ul className="space-y-2 text-sm text-blue-800">
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
        </Card>
      </div>
    </div>
  )
}
