"use client"

import { MessageList } from "./MessageList"
import { MessageInput } from "./MessageInput"
import { LoadingIndicator } from "./LoadingIndicator"
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
        <MessageList messages={messages} />
        {isLoading && (
          <div className="px-4 py-2">
            <LoadingIndicator message={loadingMessage} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4">
        <MessageInput
          onSendMessage={onSendMessage}
          disabled={isLoading}
          placeholder={isLoading ? "Waiting for response..." : "Ask anything you like..."}
        />
      </div>
    </div>
  )
}
