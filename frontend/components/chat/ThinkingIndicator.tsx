"use client"

export function ThinkingIndicator() {
  return (
    <div className="flex items-center gap-2 bg-muted p-4 rounded-tl-xl rounded-tr-xl rounded-br-xl rounded-bl-none max-w-[80px] mr-auto ml-6">
      <div className="flex gap-1">
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
      </div>
    </div>
  )
}
