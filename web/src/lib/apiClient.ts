import { APIError } from "./errors"

interface RequestOptions extends RequestInit {
  params?: Record<string, string>
}

const API_BASE_URL = import.meta.env.WEB_API_BASE_URL || "http://localhost:8000"

export class APIClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private buildUrl(endpoint: string, params?: Record<string, string>): string {
    const url = new URL(`${this.baseUrl}${endpoint}`)
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        url.searchParams.set(key, value)
      })
    }
    return url.toString()
  }

  async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const { params, ...fetchOptions } = options
    const url = this.buildUrl(endpoint, params)

    try {
      const response = await fetch(url, fetchOptions)
      if (!response.ok) {
        throw new APIError(`Request failed: ${response.statusText}`, response.status)
      }
      return await response.json()
    } catch (error) {
      if (error instanceof APIError) throw error
      const message = error instanceof Error ? error.message : "Request failed"
      throw new APIError(message)
    }
  }

  async get<T>(endpoint: string, params?: Record<string, string>): Promise<T> {
    return this.request<T>(endpoint, { method: "GET", params })
  }

  async post<T>(endpoint: string, body?: unknown, params?: Record<string, string>): Promise<T> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: body instanceof FormData ? body : JSON.stringify(body),
      params,
    })
  }
}

export const apiClient = new APIClient(API_BASE_URL)
export { API_BASE_URL }
