"use client"

import { useState, KeyboardEvent } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Send } from "lucide-react"

interface MessageInputProps {
  onSendMessage: (message: string) => void
  disabled?: boolean
  placeholder?: string
}

export function MessageInput({
  onSendMessage,
  disabled = false,
  placeholder = "Type your message..."
}: MessageInputProps) {
  const [input, setInput] = useState("")

  const handleSend = () => {
    const trimmedInput = input.trim()
    if (trimmedInput && !disabled) {
      onSendMessage(trimmedInput)
      setInput("")
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="relative bg-gray-50 border border-gray-300 rounded-lg flex items-center py-2">
      <Input
        type="text"
        placeholder={placeholder}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        className="flex-1 border-0 bg-transparent pr-12 focus-visible:ring-0 focus-visible:ring-offset-0 shadow-none outline-none"
      />
      <Button
        onClick={handleSend}
        disabled={disabled || !input.trim()}
        size="icon"
        className="absolute right-2 bg-gray-500 hover:bg-gray-600"
      >
        <Send className="h-4 w-4" />
        <span className="sr-only">Send message</span>
      </Button>
    </div>
  )
}
