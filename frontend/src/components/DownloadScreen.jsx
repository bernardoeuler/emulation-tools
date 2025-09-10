import { useState, useEffect } from "react"

export default function DownloadScreen({ requestId }) {
    const [isLoading, setIsLoading] = useState(true)
    const [downloadId, setDownloadId] = useState("")

    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL

    useEffect(() => {
        if (downloadId === "") {
            const statusPolling = setInterval(() => {
                fetch(`${API_BASE_URL}/status/${requestId}`)
                    .then(res => res.json())
                    .then(json => {
                        if (json.status !== "pending" && json.status !== "processing") {
                            if (json.status === "done") {
                                setDownloadId(json["download_id"])
                            }
                            setIsLoading(false)
                        }
                    })
                    .catch(err => console.error("Polling error:", err))
            }, 2000)

            return () => clearInterval(statusPolling)
        }
    }, [downloadId, requestId, API_BASE_URL])

    return (
        <div>
            <h1>Download converted files</h1>
            {isLoading && <p>Loading...</p>}
            {downloadId !== "" && <a href={`${API_BASE_URL}/download/${downloadId}`} download>Download link</a>}
        </div>
    )
}