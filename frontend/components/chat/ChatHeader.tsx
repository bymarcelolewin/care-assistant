"use client"

import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { RotateCcw } from "lucide-react"

interface ChatHeaderProps {
  onClearConversation: () => void
  showMemory: boolean
  showGraph: boolean
  showSteps: boolean
  onToggleMemory: () => void
  onToggleGraph: () => void
  onToggleSteps: () => void
}

export function ChatHeader({
  onClearConversation,
  showMemory,
  showGraph,
  showSteps,
  onToggleMemory,
  onToggleGraph,
  onToggleSteps,
}: ChatHeaderProps) {
  return (
    <div className="border-b p-4 px-10 flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-bold">CARE Assistant</h1>
        <p className="text-sm text-muted-foreground">
          Coverage Analysis and Recommendation Engine
        </p>
      </div>
      <div className="flex items-center gap-6">
        {/* Observability Checkboxes */}
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-muted-foreground">Observability:</span>
          <div className="flex items-center gap-2">
            <Checkbox
              id="memory-checkbox"
              checked={showMemory}
              onCheckedChange={onToggleMemory}
            />
            <Label
              htmlFor="memory-checkbox"
              className="text-sm cursor-pointer"
            >
              Memory
            </Label>
          </div>
          <div className="flex items-center gap-2">
            <Checkbox
              id="graph-checkbox"
              checked={showGraph}
              onCheckedChange={onToggleGraph}
            />
            <Label
              htmlFor="graph-checkbox"
              className="text-sm cursor-pointer"
            >
              Graph
            </Label>
          </div>
          <div className="flex items-center gap-2">
            <Checkbox
              id="steps-checkbox"
              checked={showSteps}
              onCheckedChange={onToggleSteps}
            />
            <Label
              htmlFor="steps-checkbox"
              className="text-sm cursor-pointer"
            >
              Steps
            </Label>
          </div>
        </div>

        {/* Clear Conversation Button */}
        <Button
          variant="outline"
          size="sm"
          onClick={onClearConversation}
          className="gap-2"
        >
          <RotateCcw className="h-4 w-4" />
          Clear Conversation
        </Button>
      </div>
    </div>
  )
}
