"use client"

import { ConversationState } from "@/lib/types"
import { MemoryContent } from "@/components/observability/MemoryContent"

interface StateViewProps {
  state: ConversationState | null
}

/**
 * StateView - Wrapper component for MemoryContent in the developer panel
 *
 * This component now uses the extracted MemoryContent component,
 * making the content reusable in draggable windows.
 */
export function StateView({ state }: StateViewProps) {
  return <MemoryContent state={state} />
}
