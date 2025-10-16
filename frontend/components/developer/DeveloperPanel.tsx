"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { ChevronDown, ChevronUp } from "lucide-react"
import { TraceView } from "./TraceView"
import { StateView } from "./StateView"
import { TraceEntry, ConversationState } from "@/lib/types"

interface DeveloperPanelProps {
  trace: TraceEntry[]
  state: ConversationState | null
}

export function DeveloperPanel({ trace, state }: DeveloperPanelProps) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="border-t bg-muted/50">
      {/* Panel Header / Toggle */}
      <div
        className="flex items-center justify-between px-4 py-2 cursor-pointer hover:bg-muted/80 transition-colors"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center gap-2">
          <span className="text-sm font-mono font-semibold">🔧 Developer Panel</span>
          <span className="text-xs text-muted-foreground">
            {trace.length > 0 ? `${trace.length} trace entries` : "No trace data"}
          </span>
        </div>
        <Button variant="ghost" size="sm">
          {isOpen ? (
            <ChevronDown className="h-4 w-4" />
          ) : (
            <ChevronUp className="h-4 w-4" />
          )}
        </Button>
      </div>

      {/* Panel Content */}
      {isOpen && (
        <div className="border-t">
          <Tabs defaultValue="trace" className="w-full">
            <TabsList className="w-full justify-start rounded-none border-b bg-background">
              <TabsTrigger value="trace">Execution Trace</TabsTrigger>
              <TabsTrigger value="state">State</TabsTrigger>
            </TabsList>

            <TabsContent value="trace" className="p-4 max-h-[400px] overflow-y-auto">
              <TraceView entries={trace} />
            </TabsContent>

            <TabsContent value="state" className="p-4 max-h-[400px] overflow-y-auto">
              <StateView state={state} />
            </TabsContent>
          </Tabs>
        </div>
      )}
    </div>
  )
}
