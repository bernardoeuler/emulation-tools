import { useState } from "react"

export default function DownloadScreen({ requestId }) {
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState(null)
    const [downloadId, setDownloadId] = useState("")

    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL

    function pollData() {
        console.log("Polling...")
        const endpoint = `${API_BASE_URL}/status/${requestId}`
        fetch(endpoint)
            .then(res => res.json())
            .then(json => {
                console.log(json)
                
                if (json.status !== "pending") {
                    if (json.status == "ready") {
                        console.log("Download fetched:", json["download_id"] || "...")
                        setDownloadId(json["download_id"])
                        setIsLoading(false)
                    }

                    setIsLoading(false)
                    clearInterval(statusPolling)
               }
            })
            .catch(err => console.error("Polling error:", err));
    }

    const statusPolling = setInterval(pollData, 2000)

    if (downloadId) console.log(downloadId)

    return (
        <div>
            <h1>Download converted files</h1>
            {isLoading && <p>Loading...</p>}
            {downloadId !== "" && <a href={`${API_BASE_URL}/download/${downloadId}`} download>Download link</a>}
        </div>
    )
}