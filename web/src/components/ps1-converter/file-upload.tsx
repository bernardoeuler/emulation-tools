import type { ChangeEvent, DragEvent } from "react"
import { useRef, useState } from "react"
import { Upload } from "lucide-react"

interface FileUploadProps {
  onFileSelect: (file: File) => void
  acceptedFormats?: string[]
}

export function FileUpload({ onFileSelect, acceptedFormats = [".zip", ".chd", ".cue", ".bin", ".iso"] }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files.length > 0) {
      onFileSelect(files[0])
    }
  }

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files
    if (files && files.length > 0) {
      onFileSelect(files[0])
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="w-full">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
        className={`border-2 border-dashed rounded-lg p-8 sm:p-12 text-center cursor-pointer transition-colors ${
          isDragging
            ? "border-primary bg-primary/5"
            : "border-input bg-muted/30 hover:border-primary/50"
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileChange}
          accept={acceptedFormats.join(",")}
          className="hidden"
          aria-label="Upload game file"
        />

        <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />

        <div className="space-y-1">
          <p className="font-semibold text-foreground">
            Click to upload <span className="font-normal text-muted-foreground">or drag and drop</span>
          </p>
          <p className="text-sm text-muted-foreground">
            Upload {acceptedFormats.join(", ")}
          </p>
        </div>
      </div>
    </div>
  )
}
