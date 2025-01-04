const express = require("express");
const multer = require("multer");
const { spawn } = require("child_process");
const cors = require("cors");
const path = require("path");
const fs = require("fs");

const app = express();
app.use(cors());

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, "public")));

// Set up Multer for file uploads
const upload = multer({ dest: "uploads/" });

app.post("/upload-resume", upload.single("resume"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
    }

    // Invoke Python script
    const pythonProcess = spawn("python", ["resume_parser_ml.py", req.file.path]);

    let output = "";
    let errorOutput = "";

    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
        errorOutput += data.toString();
    });

    pythonProcess.on("close", (code) => {
        // Delete the uploaded file after processing
        fs.unlink(req.file.path, (err) => {
            if (err) console.error("Error deleting file:", err);
        });

        if (code !== 0) {
            console.error("Python script error:", errorOutput);
            return res.status(500).json({ error: "Error processing resume" });
        }

        try {
            const parsedData = JSON.parse(output);
            res.json(parsedData);
        } catch (err) {
            console.error("Error parsing Python output:", err);
            res.status(500).json({ error: "Error parsing Python output" });
        }
    });
});

// Serve the homepage (index.html)
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
