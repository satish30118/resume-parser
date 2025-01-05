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
            alert("An error occurred while analyzing the resume. Please try again.");
        } finally {
            setLoading(false); // Stop the loader
        }
    };

    return (
        <div className="app-container">
            <header className="header">
                <h1 className="title">Resume Analyzer</h1>
                <p className="subtitle">Upload a resume to get an in-depth analysis of skills, education, and suitability for roles.</p>
            </header>

            <div className="upload-section">
                <input
                    type="file"
                    onChange={handleFileChange}
                    className="file-input"
                />
                <button onClick={handleUpload} className="upload-button">
                    {loading ? "Analyzing..." : "Upload and Analyze"}
                </button>
            </div>

            {loading && <div className="loader">Analyzing your resume...</div>}

            {analysisResult && (
                <div className="result-section">
                    <h2 className="result-title">Analysis Result</h2>
                    <div className="result-content">
                        <h3>Name: {analysisResult.Name || "Not Found"}</h3>
                        <h3>Email: {analysisResult.Email.join(", ") || "Not Found"}</h3>
                        <h3>Phone: {analysisResult.Phone.join(", ") || "Not Found"}</h3>
                        <h3>Skills:</h3>
                        <ul>
                            {analysisResult.Skills.length > 0
                                ? analysisResult.Skills.map((skill, index) => <li key={index}>{skill}</li>)
                                : "No Skills Found"}
                        </ul>
                        <h3>Education:</h3>
                        <ul>
                            {analysisResult.Education.length > 0
                                ? analysisResult.Education.map((edu, index) => <li key={index}>{edu}</li>)
                                : "No Education Details Found"}
                        </ul>
                        <h3>Best Role: {analysisResult["Best Role"] || "Not Found"}</h3>
                        <h3>Role Match Scores:</h3>
                        <ul>
                            {Object.entries(analysisResult["All Role Scores"]).map(([role, score]) => (
                                <li key={role}>
                                    {role}: {score}%
                                </li>
                            ))}
                        </ul>
                    </div>
                    <p className="message">
                        <strong>Message:</strong> Keep improving your resume to achieve better role matches!
                    </p>
                </div>
            )}
        </div>
    );
}

export default App;
