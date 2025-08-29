// server.js
const express = require("express");
const cors = require("cors");
const { pool } = require("./db") 
const { fetchAndStoreJobs } = require("./fetchJobs");

require("./cronJob");

const app = express();
const port = 3001;
app.use(cors());



// Root endpoint
app.get("/", (req, res) => res.send("Hello, Express!"));

// Manual endpoint to trigger job
app.get("/run-job-now", async (req, res) => {
  try {
    console.log("Manual job trigger:", new Date());
    await fetchAndStoreJobs();
    res.send("Job executed successfully!");
  } catch (err) {
    console.error("Error executing job:", err);
    res.status(500).send("Job failed");
  }
});

// Analysis endpoint
app.get("/api/analysis/:selectedJobTitle", async (req, res) => {
  const selectedJobTitle = req.params.selectedJobTitle;
  console.log(`Selected Job Title: ${selectedJobTitle}`);

  const query = `SELECT * FROM \`${selectedJobTitle}\` ORDER BY id DESC LIMIT 1`;

  try {
    const [rows] = await pool.query(query);

    if (!rows || rows.length === 0) {
      return res.status(404).json({ error: "Data not found" });
    }

    // Remove unwanted keys
    delete rows[0].id;
    delete rows[0].Go;

    // Sort values descending and take top 6
    const row = Object.entries(rows[0])
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6);

    res.json(row);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// Start server
app.listen(port, () => console.log(`Server running on port ${port}`));
