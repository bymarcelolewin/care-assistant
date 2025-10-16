"use client"

import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { Badge } from "@/components/ui/badge"
import { ChevronRight } from "lucide-react"
import { TraceEntry } from "@/lib/types"
import { useState } from "react"

interface TraceViewProps {
  entries: TraceEntry[]
}

export function TraceView({ entries }: TraceViewProps) {
  if (entries.length === 0) {
    return (
      <div className="text-sm text-muted-foreground text-center py-8">
        No trace entries yet. Send a message to see the execution flow.
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {entries.map((entry, index) => (
        <TraceEntryItem key={index} entry={entry} />
      ))}
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
