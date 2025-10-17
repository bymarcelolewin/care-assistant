"use client"

import { Badge } from "@/components/ui/badge"
import { ConversationState } from "@/lib/types"

interface MemoryContentProps {
  state: ConversationState | null
}

/**
 * MemoryContent - Displays the conversation state (user profile, tool results, etc.)
 *
 * This component was extracted from StateView.tsx to be reusable in draggable windows.
 * It shows the "Memory" of the conversation - what the AI knows about the user and
 * the results from any tools that have been called.
 */
export function MemoryContent({ state }: MemoryContentProps) {
  if (!state) {
    return (
      <div className="text-sm text-muted-foreground text-center py-8">
        No state data yet. Send a message to see the conversation state.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* User ID */}
      <div>
        <h3 className="text-sm font-semibold mb-2 flex items-center gap-2">
          User ID
          {state.user_id ? (
            <Badge variant="secondary" className="bg-green-500 text-white">
              Identified
            </Badge>
          ) : (
            <Badge variant="secondary" className="bg-yellow-500 text-white">
              Not Identified
            </Badge>
          )}
        </h3>
        <pre className="text-xs bg-muted p-3 rounded overflow-x-auto">
          {state.user_id || "null"}
        </pre>
      </div>

      {/* User Profile */}
      <div>
        <h3 className="text-sm font-semibold mb-2">User Profile</h3>
        {state.user_profile ? (
          <div className="space-y-2">
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <span className="font-semibold">Name:</span>{" "}
                {state.user_profile.name}
              </div>
              <div>
                <span className="font-semibold">Age:</span>{" "}
                {state.user_profile.age}
              </div>
              <div>
                <span className="font-semibold">Plan ID:</span>{" "}
                {state.user_profile.plan_id}
              </div>
              <div>
                <span className="font-semibold">Member Since:</span>{" "}
                {state.user_profile.member_since}
              </div>
              <div>
                <span className="font-semibold">Deductible Annual:</span>{" "}
                ${state.user_profile.deductible_annual}
              </div>
              <div>
                <span className="font-semibold">Deductible Met:</span>{" "}
                ${state.user_profile.deductible_met}
              </div>
              <div>
                <span className="font-semibold">Out-of-Pocket Max:</span>{" "}
                ${state.user_profile.out_of_pocket_max}
              </div>
              <div>
                <span className="font-semibold">Out-of-Pocket Spent:</span>{" "}
                ${state.user_profile.out_of_pocket_spent}
              </div>
            </div>
            <details className="mt-2">
              <summary className="text-xs font-semibold cursor-pointer hover:text-primary">
                View Full Profile JSON
              </summary>
              <pre className="text-xs bg-muted p-3 rounded overflow-x-auto mt-2">
                {JSON.stringify(state.user_profile, null, 2)}
              </pre>
            </details>
          </div>
        ) : (
          <pre className="text-xs bg-muted p-3 rounded overflow-x-auto">null</pre>
        )}
      </div>

      {/* Tool Results */}
      <div>
        <h3 className="text-sm font-semibold mb-2">Tool Results</h3>
        {state.tool_results && Object.keys(state.tool_results).length > 0 ? (
          <pre className="text-xs bg-muted p-3 rounded overflow-x-auto max-h-[200px]">
            {JSON.stringify(state.tool_results, null, 2)}
          </pre>
        ) : (
          <pre className="text-xs bg-muted p-3 rounded overflow-x-auto">
            {"{}"} (no tool results in current state)
          </pre>
        )}
      </div>
    </div>
  )
}
