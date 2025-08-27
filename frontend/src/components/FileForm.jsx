import { useState } from "react"

export default function FileForm() {
    const [files, setFiles] = useState([])

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
            const endpoint = `${API_BASE_URL}/upload/`
            const response = await fetch(endpoint, {
                method: "POST",
                body: formData
            })

            if (response.ok) {
                console.log("File upload successfully")
            } else {
                console.log("Failed to upload file")
            }
        } catch (error) {
            console.error(error)
        }
    }

    return (
        <div style={{ height: "100vh", display: "flex", flexDirection: "column", alignItems: "center" }}>
            <h1>Upload file</h1>

            <form style={{ display: "flex", flexDirection: "column", alignItems: "center" }} onSubmit={handleSubmit}>
                <div>
                    <input type="file" onChange={handleFileInputChange} multiple />
                </div>
                <button type="submit">Upload</button>
            </form>
        </div>
    )
}
