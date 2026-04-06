import { apiClient } from "@/lib/api-client"
import type { StatusResponse } from "./types"

export async function getConversionStatus(requestId: string): Promise<StatusResponse> {
  return apiClient.get<StatusResponse>(`/status/${requestId}`)
}
