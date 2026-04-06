export interface UploadResponse {
  request_id: string
}

export interface StatusResponse {
  download_id?: string
  status?: string
  error?: string
}
