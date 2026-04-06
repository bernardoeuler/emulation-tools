import { useState, useCallback, useRef, useEffect } from "react"
import { uploadFiles } from "@/services/converter/uploadFiles"
import { getConversionStatus } from "@/services/converter/getConversionStatus"
import { APIError } from "@/lib/errors"

interface ConversionState {
  step: "idle" | "uploading" | "converting" | "ready" | "error"
  requestId: string | null
  downloadId: string | null
  error: string | null
  progress: number
}

interface UseConversionOptions {
  pollInterval?: number
  maxRetries?: number
}

const INITIAL_STATE: ConversionState = {
  step: "idle",
  requestId: null,
  downloadId: null,
  error: null,
  progress: 0,
}

const PROGRESS = {
  UPLOAD_START: 10,
  CONVERTING: 20,
  POLLING_MAX: 95,
  COMPLETE: 100,
} as const

export function useConversion(options: UseConversionOptions = {}) {
  const { pollInterval = 2000, maxRetries = 60 } = options

  const [state, setState] = useState<ConversionState>(INITIAL_STATE)
  const pollTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const retryCountRef = useRef(0)

  const clearPollTimeout = useCallback(() => {
    if (pollTimeoutRef.current) {
      clearTimeout(pollTimeoutRef.current)
      pollTimeoutRef.current = null
    }
  }, [])

  const schedulePoll = useCallback(
    (requestId: string) => {
      pollTimeoutRef.current = setTimeout(() => pollStatus(requestId), pollInterval)
    },
    [pollInterval]
  )

  const pollStatus = useCallback(
    async (requestId: string) => {
      if (retryCountRef.current >= maxRetries) {
        setState(prev => ({
          ...prev,
          step: "error",
          error: "Conversion timeout. Please try again.",
        }))
        return
      }

      try {
        const response = await getConversionStatus(requestId)

        if (response.status === "ready" && response.download_id) {
          setState(prev => ({
            ...prev,
            step: "ready",
            downloadId: response.download_id!,
            progress: PROGRESS.COMPLETE,
          }))
          retryCountRef.current = 0
          return
        }

        if (response.download_id || response.error) {
          retryCountRef.current++
          setState(prev => ({
            ...prev,
            progress: Math.min(PROGRESS.POLLING_MAX, prev.progress + 1),
          }))
          schedulePoll(requestId)
        }
      } catch (error) {
        setState(prev => ({
          ...prev,
          step: "error",
          error: error instanceof APIError ? error.message : "Failed to check status",
        }))
      }
    },
    [maxRetries, schedulePoll]
  )

  const startConversion = useCallback(
    async (files: File[]) => {
      if (files.length === 0) return

      clearPollTimeout()
      retryCountRef.current = 0

      setState({
        step: "uploading",
        requestId: null,
        downloadId: null,
        error: null,
        progress: PROGRESS.UPLOAD_START,
      })

      try {
        const requestId = await uploadFiles(files)

        setState(prev => ({
          ...prev,
          step: "converting",
          requestId,
          progress: PROGRESS.CONVERTING,
        }))

        schedulePoll(requestId)
      } catch (error) {
        setState({
          ...INITIAL_STATE,
          step: "error",
          error: error instanceof APIError ? error.message : "Upload failed. Please try again.",
        })
      }
    },
    [clearPollTimeout, schedulePoll]
  )

  const reset = useCallback(() => {
    clearPollTimeout()
    retryCountRef.current = 0
    setState(INITIAL_STATE)
  }, [clearPollTimeout])

  useEffect(() => {
    return clearPollTimeout
  }, [clearPollTimeout])

  return { state, startConversion, reset }
}

export type { UseConversionOptions }
