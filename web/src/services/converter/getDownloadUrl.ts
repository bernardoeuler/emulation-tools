import { API_BASE_URL } from "@/lib/api-client"

export function getDownloadUrl(downloadId: string, filename?: string): string {
  const url = new URL(`${API_BASE_URL}/download/${downloadId}`)
  if (filename) url.searchParams.set("file", filename)
  return url.toString()
}
