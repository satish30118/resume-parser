import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
    const [file, setFile] = useState(null);
    const [analysisResult, setAnalysisResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            alert("Please upload a file first.");
            return;
        }

        setLoading(true); // Start the loader
        setAnalysisResult(null); // Clear previous results if any

        const formData = new FormData();
        formData.append("resume", file);

        try {
            const response = await axios.post("http://localhost:5000/upload-resume", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            setAnalysisResult(response.data);
        } catch (error) {
            console.error("Error uploading file:", error);
        } finally {
            setLoading(false); // Stop the loader
        }
    };

    return (
        <div className="container">
            <h1 className="title">Resume Analyzer</h1>
            <div className="upload-section">
                <input type="file" onChange={handleFileChange} className="file-input" />
                <button onClick={handleUpload} className="upload-button">Upload and Analyze</button>
            </div>

            {loading && <div className="loader">Analyzing...</div>}

            {analysisResult && (
                <div className="result-section">
                    <h2 className="result-title">Analysis Result:</h2>
                    <pre className="result-content">{JSON.stringify(analysisResult, null, 2)}</pre>
                    <p className="message">
                        <span>Sorry Aditya Bhai,</span> abhi logic part implement kiya hu, data mil raha h backend se, ab design baki h!
                    </p>
                </div>
            )}
        </div>
    );
}

export default App;



