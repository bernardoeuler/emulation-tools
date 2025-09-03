import { useState } from "react"
import DownloadScreen from "./DownloadScreen"

export default function FileForm() {
    const [files, setFiles] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [filesUploaded, setFilesUploaded] = useState(false)
    const [requestId, setRequestId] = useState("")

    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL

    const handleFileInputChange = (event) => {
        console.log(event.target.files)
        setFiles(Array.from(event.target.files))
    }

    const handleSubmit = async (event) => {
        event.preventDefault()

        const formData = new FormData()

        files.forEach(file => {
            formData.append("file_uploads", file)
        })

        try {
            setLoading(true)

            const endpoint = `${API_BASE_URL}/upload/`
            const response = await fetch(endpoint, {
                method: "POST",
                body: formData
            })

            if (response.ok) {
                const json = await response.json()
                setRequestId(json["request_id"])
                setFilesUploaded(true)
                console.log("File upload successfully")
            } else {
                setError("Error: " + response.statusText)
                console.log("Failed to upload file")
            }
        } catch (error) {
            setError(error)
            console.error(error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) return <div>Loading response...</div>

    if (filesUploaded && requestId !== "") return <DownloadScreen requestId={requestId} />

    return (
        <div style={{ height: "100vh", display: "flex", flexDirection: "column", alignItems: "center" }}>
            <h1>Upload file</h1>

            <form style={{ display: "flex", flexDirection: "column", alignItems: "center" }} onSubmit={handleSubmit}>
                <div>
                    <input type="file" onChange={handleFileInputChange} multiple />
                </div>
                <button type="submit">Upload</button>
            </form>

            {error && <div>Error: {error}</div>}
        </div>
    )
}
