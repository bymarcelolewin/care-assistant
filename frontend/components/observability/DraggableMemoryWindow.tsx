"use client"

import { useState, useRef } from "react"
import Draggable, { DraggableData, DraggableEvent } from "react-draggable"
import { X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { MemoryContent } from "./MemoryContent"
import { ConversationState } from "@/lib/types"

interface DraggableMemoryWindowProps {
  state: ConversationState | null
  onClose: () => void
  onFocus: () => void
  zIndex: number
}

/**
 * DraggableMemoryWindow - A draggable window displaying conversation memory/state
 *
 * Features:
 * - Draggable by header
 * - Fixed size (400px × 500px)
 * - Close button
 * - Brings to front on click
 */
export function DraggableMemoryWindow({
  state,
  onClose,
  onFocus,
  zIndex,
}: DraggableMemoryWindowProps) {
  // Position centered over chat - window opens in middle of viewport
  // Center horizontally: (viewport width - window width) / 2
  // Center vertically: 100px from top for visibility
  const [position, setPosition] = useState({
    x: typeof window !== 'undefined' ? (window.innerWidth - 400) / 2 : 400,
    y: 100
  })
  const nodeRef = useRef(null)

  const handleDrag = (_e: DraggableEvent, data: DraggableData) => {
    setPosition({ x: data.x, y: data.y })
  }

  return (
    <Draggable
      nodeRef={nodeRef}
      handle=".drag-handle"
      position={position}
      onDrag={handleDrag}
    >
      <div
        ref={nodeRef}
        className="fixed"
        style={{
          width: "400px",
          height: "500px",
          zIndex,
        }}
        onClick={onFocus}
      >
        <Card className="h-full flex flex-col shadow-lg border-gray-200 p-0">
          {/* Header - Drag Handle */}
          <div className="drag-handle cursor-move bg-slate-100 px-4 py-3 border-b flex items-center justify-between rounded-t-lg">
            <h3 className="font-semibold text-base">Memory</h3>
            <Button
              variant="ghost"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                onClose()
              }}
              className="h-6 w-6 p-0 hover:bg-slate-200"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Content - Scrollable */}
          <div className="flex-1 overflow-y-auto p-4">
            <MemoryContent state={state} />
          </div>
        </Card>
      </div>
    </Draggable>
  )
}
