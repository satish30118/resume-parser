const express = require("express");
const multer = require("multer");
const { spawn } = require("child_process");
const cors = require("cors");
const path = require("path");

const app = express();
app.use(cors());

const upload = multer({ dest: "uploads/" });

app.post("/upload-resume", upload.single("resume"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
    }

    // Invoke Python script
    const pythonProcess = spawn("python", ["resume_parser.py", req.file.path]);

    let output = "";
    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on("data", (error) => {
        console.error("Python error:", error.toString());
    });

    pythonProcess.on("close", () => {
        // Send parsed data back to the frontend
        try {
            const parsedData = JSON.parse(output);
            res.json(parsedData);
        } catch (err) {
            res.status(500).json({ error: "Error parsing Python output" });
        }
    });
});

const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
