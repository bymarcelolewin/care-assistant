"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Loader2 } from "lucide-react"

interface LoadingIndicatorProps {
  message?: string
}

export function LoadingIndicator({ message = "AI is thinking..." }: LoadingIndicatorProps) {
  return (
    <Card className="max-w-[80%] mr-auto bg-muted">
      <CardContent className="p-4">
        <div className="flex items-center gap-3">
          <Loader2 className="h-4 w-4 animate-spin" />
          <div className="text-sm text-muted-foreground">
            {message}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
