"use client"

import { TraceEntry, Message } from "@/lib/types"
import { ExecutionStepsContent } from "@/components/observability/ExecutionStepsContent"

interface TraceViewProps {
  entries: TraceEntry[]
  messages: Message[]
}

/**
 * TraceView - Wrapper component for ExecutionStepsContent in the developer panel
 *
 * This component now uses the extracted ExecutionStepsContent component,
 * making the content reusable in draggable windows.
 */
export function TraceView({ entries, messages }: TraceViewProps) {
  return <ExecutionStepsContent entries={entries} messages={messages} />
}
