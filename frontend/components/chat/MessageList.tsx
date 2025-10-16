"use client"

import { useEffect, useRef } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Message } from "@/lib/types"

interface MessageListProps {
  messages: Message[]
}

export function MessageList({ messages }: MessageListProps) {
  const scrollAreaRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollViewport = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]')
      if (scrollViewport) {
        scrollViewport.scrollTop = scrollViewport.scrollHeight
      }
    }
  }, [messages])

  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <p>No messages yet. Start the conversation!</p>
      </div>
    )
  }

  return (
    <ScrollArea className="h-full w-full pr-4" ref={scrollAreaRef}>
      <div className="space-y-4 pt-4 pb-4">
        {messages.map((message) => (
          <Card
            key={message.id}
            className={`max-w-[80%] ${
              message.role === "user"
                ? "ml-auto bg-slate-600 text-white"
                : "mr-auto bg-muted"
            } ${message.isProgress ? "opacity-70 italic" : ""}`}
          >
            <CardContent className="p-4">
              <div className="flex flex-col gap-1">
                <div className="text-xs font-semibold opacity-70">
                  {message.role === "user" ? "You" : "CARE Assistant"}
                </div>
                <div className="text-sm whitespace-pre-wrap">
                  {message.content}
                </div>
                <div className="text-xs opacity-50 mt-1">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </ScrollArea>
  )
}
