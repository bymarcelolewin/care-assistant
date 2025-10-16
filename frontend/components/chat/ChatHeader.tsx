"use client"

import { Button } from "@/components/ui/button"
import { RotateCcw } from "lucide-react"

interface ChatHeaderProps {
  onClearConversation: () => void
}

export function ChatHeader({ onClearConversation }: ChatHeaderProps) {
  return (
    <div className="border-b p-4 flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-bold">CARE Assistant</h1>
        <p className="text-sm text-muted-foreground">
          Coverage Analysis and Recommendation Engine
        </p>
      </div>
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
  )
}
