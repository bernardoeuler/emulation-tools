import { useState, useRef, useEffect } from "react"
import { ChevronDown } from "lucide-react"

interface FormatSelectorProps {
  value: string
  onChange: (format: string) => void
  formats?: { label: string; value: string }[]
}

const DEFAULT_FORMATS = [
  { label: "CHD", value: "chd" },
  { label: "CUE", value: "cue" },
  { label: "BIN", value: "bin" },
  { label: "ISO", value: "iso" },
  { label: "ZIP", value: "zip" },
]

export function FormatSelector({
  value,
  onChange,
  formats = DEFAULT_FORMATS
}: FormatSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const selectedFormat = formats.find(f => f.value === value) || formats[0]

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  const handleSelect = (format: { label: string; value: string }) => {
    onChange(format.value)
    setIsOpen(false)
  }

  return (
    <div ref={dropdownRef} className="relative w-full">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-4 py-3 border border-input rounded-md bg-background text-foreground hover:bg-accent/50 transition-colors focus:outline-none focus:ring-2 focus:ring-ring/50"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
      >
        <span className="font-medium">{selectedFormat.label}</span>
        <ChevronDown
          className={`w-5 h-5 text-muted-foreground transition-transform ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-background border border-input rounded-md shadow-lg z-10">
          {formats.map((format) => (
            <button
              key={format.value}
              onClick={() => handleSelect(format)}
              className={`w-full px-4 py-2 text-left transition-colors first:rounded-t-md last:rounded-b-md ${
                format.value === value
                  ? "bg-primary text-primary-foreground"
                  : "hover:bg-accent text-foreground"
              }`}
              role="option"
              aria-selected={format.value === value}
            >
              {format.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
