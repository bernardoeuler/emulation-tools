import { AlertCircle, CheckCircle, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"

interface ConversionStatusProps {
  step: "uploading" | "converting" | "ready" | "error"
  progress: number
  error?: string | null
  downloadId?: string | null
  onReset: () => void
  onDownload?: (downloadId: string) => void
}

const STATUS_MESSAGES: Record<string, string> = {
  uploading: "Uploading your file...",
  converting: "Converting your game...",
  ready: "Conversion complete!",
  error: "Conversion failed",
}

export function ConversionStatus({
  step,
  progress,
  error,
  downloadId,
  onReset,
  onDownload,
}: ConversionStatusProps) {
  const isProcessing = step === "uploading" || step === "converting"
  const isSuccess = step === "ready"
  const isError = step === "error"

  const getIcon = () => {
    if (isProcessing) {
      return <Loader2 className="w-5 h-5 animate-spin text-primary" />
    }
    if (isSuccess) {
      return <CheckCircle className="w-5 h-5 text-green-500" />
    }
    return <AlertCircle className="w-5 h-5 text-destructive" />
  }

  return (
    <div className="w-full space-y-4">
      <div className="flex items-center gap-3">
        {getIcon()}
        <p className="text-sm font-medium text-foreground">
          {STATUS_MESSAGES[step] || ""}
        </p>
      </div>

      {isProcessing && (
        <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
          <div
            className="bg-primary h-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {isError && error && (
        <p className="text-sm text-destructive bg-destructive/10 p-3 rounded-md">
          {error}
        </p>
      )}

      <div className="flex gap-3 pt-2">
        {isSuccess && downloadId && (
          <>
            <Button
              variant="default"
              onClick={() => onDownload?.(downloadId)}
              className="flex-1"
            >
              Download game
            </Button>
            <Button variant="outline" onClick={onReset}>
              Convert another
            </Button>
          </>
        )}

        {isError && (
          <Button variant="default" onClick={onReset} className="w-full">
            Try again
          </Button>
        )}
      </div>
    </div>
  )
}
