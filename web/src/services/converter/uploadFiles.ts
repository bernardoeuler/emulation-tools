import { apiClient } from "@/lib/apiClient"
import type { UploadResponse } from "./types"

export async function uploadFiles(files: File[]): Promise<string> {
  const formData = new FormData()
  files.forEach((file) => formData.append("file_uploads", file))

  const data = await apiClient.post<UploadResponse>("/upload/", formData)
  return data.request_id
}
