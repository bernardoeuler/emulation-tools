import React from "react"
import { Button } from "@/components/ui/button"
import { FileUpload } from "./fileUpload"
import { FormatSelector } from "./formatSelector"
import { Footer } from "./footer"
import { ConversionStatus } from "./conversionStatus"
import { useConversion } from "@/hooks/useConversion"
import { getDownloadUrl } from "@/services/converter/getDownloadUrl"

const SUPPORTED_FORMATS = ".zip, .chd, .cue + .bin and .iso"

export function PS1Converter() {
  const [selectedFiles, setSelectedFiles] = React.useState<File[]>([])
  const [selectedFormat] = React.useState("chd")
  const { state, startConversion, reset } = useConversion()

  const isProcessing = state.step !== "idle"
  const totalFileSize = selectedFiles.reduce((sum, file) => sum + file.size, 0) / 1024 / 1024

  const handleFileSelect = (files: File[]) => {
    setSelectedFiles(files)
  }

  const handleConvert = async () => {
    if (selectedFiles.length === 0) return
    await startConversion(selectedFiles)
  }

  const handleDownload = (downloadId: string) => {
    const filename = `ps1-game-${selectedFiles[0]?.name || "converted"}`
    const url = getDownloadUrl(downloadId)
    const link = document.createElement("a")
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const handleReset = () => {
    reset()
    setSelectedFiles([])
  }

  return (
    <div className="min-h-dvh bg-background flex flex-col">
      <main className="flex-1 w-full">
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-8 md:px-10 lg:px-16 pt-24 sm:pt-28 md:pt-32 pb-12 sm:pb-16 md:pb-20">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
            {/* Title & Description */}
            <div className="flex flex-col justify-start">
              <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-foreground mb-6">
                PlayStation 1 Converter
              </h1>
              <p className="text-base sm:text-lg text-muted-foreground max-w-md">
                Convert PS1 games from one format to another. The converter accepts{" "}
                <span className="font-semibold text-foreground">{SUPPORTED_FORMATS}</span>.
              </p>
            </div>

            {/* Upload & Convert Form */}
            <div className="flex flex-col gap-8">
              <div>
                <h2 className="text-2xl sm:text-3xl font-bold text-foreground text-center mb-8">
                  Convert your game
                </h2>

                {!isProcessing && (
                  <div className="mb-8">
                    <FileUpload onFileSelect={handleFileSelect} />
                    {selectedFiles.length > 0 && (
                      <div className="mt-3 space-y-2">
                        <p className="text-sm text-muted-foreground">
                          Selected: <span className="font-medium text-foreground">{selectedFiles.length} file{selectedFiles.length !== 1 ? "s" : ""}</span> ({totalFileSize.toFixed(2)} MB)
                        </p>
                        <ul className="text-sm text-muted-foreground space-y-1">
                          {selectedFiles.map((file, idx) => (
                            <li key={idx} className="flex items-center gap-2">
                              <span className="text-foreground font-medium">•</span>
                              {file.name}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {isProcessing ? (
                <ConversionStatus
                  step={state.step as "uploading" | "converting" | "ready" | "error"}
                  progress={state.progress}
                  error={state.error}
                  downloadId={state.downloadId}
                  onDownload={handleDownload}
                  onReset={handleReset}
                />
              ) : (
                <>
                  <div className="space-y-2">
                    <label htmlFor="format-select" className="block text-sm font-semibold text-foreground">
                      Convert to
                    </label>
                    <FormatSelector value={selectedFormat} onChange={() => {}} />
                  </div>

                  <Button
                    onClick={handleConvert}
                    disabled={selectedFiles.length === 0}
                    size="lg"
                    className="w-full"
                  >
                    Convert game
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default PS1Converter

