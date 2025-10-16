"use client"

import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { Badge } from "@/components/ui/badge"
import { ChevronRight } from "lucide-react"
import { TraceEntry, Message } from "@/lib/types"
import { useState } from "react"

interface TraceViewProps {
  entries: TraceEntry[]
  messages: Message[]
}

export function TraceView({ entries, messages }: TraceViewProps) {
  if (entries.length === 0) {
    return (
      <div className="text-sm text-muted-foreground text-center py-8">
        No trace entries yet. Send a message to see the execution flow.
      </div>
    )
  }

  // Group trace entries by the user message that triggered them
  const groupedTraces = groupTracesByMessage(entries, messages)

  return (
    <div className="space-y-4">
      {groupedTraces.map((group, groupIndex) => (
        <div key={groupIndex} className="space-y-2">
          {/* User Prompt Display or Initial System Message */}
          {group.userMessage ? (
            <UserPromptDisplay message={group.userMessage} />
          ) : (
            <InitialSystemDisplay />
          )}
          {/* Trace Entries */}
          {group.entries.map((entry, entryIndex) => (
            <TraceEntryItem key={`${groupIndex}-${entryIndex}`} entry={entry} />
          ))}
        </div>
      ))}
    </div>
  )
}

/**
 * Group trace entries by the user message that triggered them.
 * Uses timestamp comparison to associate traces with messages.
 */
function groupTracesByMessage(
  entries: TraceEntry[],
  messages: Message[]
): Array<{ userMessage: Message | null; entries: TraceEntry[] }> {
  const userMessages = messages.filter((m) => m.role === "user")

  if (userMessages.length === 0) {
    // No user messages, return all entries as one group (initial traces)
    return [{ userMessage: null, entries }]
  }

  const groups: Array<{ userMessage: Message | null; entries: TraceEntry[] }> = []

  // First, find trace entries BEFORE the first user message (initial traces)
  const firstUserMessageTime = new Date(userMessages[0].timestamp).getTime()
  const initialEntries = entries.filter((entry) => {
    const entryTime = new Date(entry.timestamp).getTime()
    return entryTime < firstUserMessageTime
  })

  if (initialEntries.length > 0) {
    groups.push({ userMessage: null, entries: initialEntries })
  }

  // Then, for each user message, find the trace entries that follow it
  for (let i = 0; i < userMessages.length; i++) {
    const userMessage = userMessages[i]
    const nextUserMessage = userMessages[i + 1]

    const messageTime = new Date(userMessage.timestamp).getTime()
    const nextMessageTime = nextUserMessage
      ? new Date(nextUserMessage.timestamp).getTime()
      : Infinity

    // Find trace entries between this message and the next
    const groupEntries = entries.filter((entry) => {
      const entryTime = new Date(entry.timestamp).getTime()
      return entryTime >= messageTime && entryTime < nextMessageTime
    })

    if (groupEntries.length > 0) {
      groups.push({ userMessage, entries: groupEntries })
    }
  }

  // Reverse the groups so latest appears first
  return groups.reverse()
}

/**
 * Component to display user prompts with darker background
 */
function UserPromptDisplay({ message }: { message: Message }) {
  return (
    <div className="bg-slate-600 text-white p-3 rounded-lg">
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1">
          <p className="text-sm font-medium">{message.content}</p>
          <p className="text-xs text-slate-400 mt-1">
            {new Date(message.timestamp).toLocaleTimeString()}
          </p>
        </div>
        <Badge variant="outline" className="bg-slate-700 border-slate-600 text-white flex-shrink-0">
          User Prompt
        </Badge>
      </div>
    </div>
  )
}

/**
 * Component to display initial system startup message
 */
function InitialSystemDisplay() {
  return (
    <div className="bg-slate-600 text-white p-3 rounded-lg">
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1">
          <p className="text-sm font-medium">System Initialization</p>
          <p className="text-xs text-slate-400 mt-1">
            Assistant startup and initial configuration
          </p>
        </div>
        <Badge variant="outline" className="bg-slate-700 border-slate-600 text-white flex-shrink-0">
          System
        </Badge>
      </div>
    </div>
  )
}

function TraceEntryItem({ entry }: { entry: TraceEntry }) {
  const [isOpen, setIsOpen] = useState(false)

  const nodeColor = {
    identify_user: "bg-blue-500",
    orchestrate_tools: "bg-purple-500",
    generate_response: "bg-green-500",
  }[entry.node] || "bg-gray-500"

  const hasDetails = entry.details && Object.keys(entry.details).length > 0

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen}>
      <div className="border rounded-lg p-3 bg-background">
        <CollapsibleTrigger className="w-full">
          <div className="flex items-start justify-between gap-2">
            <div className="flex items-start gap-3 flex-1 text-left">
              <div className="flex items-center gap-2 min-w-0">
                {hasDetails && (
                  <ChevronRight
                    className={`h-4 w-4 transition-transform flex-shrink-0 ${
                      isOpen ? "rotate-90" : ""
                    }`}
                  />
                )}
                <Badge variant="secondary" className={`${nodeColor} text-white flex-shrink-0`}>
                  {entry.node}
                </Badge>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium">{entry.action}</p>
                <p className="text-xs text-muted-foreground">
                  {new Date(entry.timestamp).toLocaleTimeString()}
                </p>
              </div>
            </div>
          </div>
        </CollapsibleTrigger>

        {hasDetails && (
          <CollapsibleContent className="mt-3 pt-3 border-t">
            <div className="space-y-2">
              <p className="text-xs font-semibold text-muted-foreground">Details:</p>
              <pre className="text-xs bg-muted p-3 rounded overflow-x-auto">
                {JSON.stringify(entry.details, null, 2)}
              </pre>
            </div>
          </CollapsibleContent>
        )}
      </div>
    </Collapsible>
  )
}
