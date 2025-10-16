"use client"

import { MessageList } from "./MessageList"
import { MessageInput } from "./MessageInput"
import { Message } from "@/lib/types"

interface ChatWindowProps {
  messages: Message[]
  onSendMessage: (message: string) => void
  isLoading: boolean
  loadingMessage?: string
}

export function ChatWindow({
  messages,
  onSendMessage,
  isLoading,
  loadingMessage
}: ChatWindowProps) {
  return (
    <div className="h-full flex flex-col p-6">
      {/* Messages Area */}
      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} isLoading={isLoading} />
      </div>

      {/* Input Area */}
      <div className="pt-6 px-4 pb-4">
        <MessageInput
          onSendMessage={onSendMessage}
          disabled={isLoading}
          placeholder={isLoading ? "Waiting for response..." : "Ask anything you like..."}
        />
      </div>
    </div>
  )
}
