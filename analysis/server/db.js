const express = require('express');
const mysql = require('mysql');
const cors = require('cors');
const app = express();
const port = 3001;
app.use(cors());

const connection = mysql.createConnection({
    host: "analysis.cyufabl1vpsa.ap-northeast-1.rds.amazonaws.com",
    user: "admin",
    password: "admin123",
    database: "analysis"
});

connection.connect((err) => {
  if (err) throw err;
  console.log('Connected to MySQL!');
});

app.get('/', (req, res) => {
  res.send('Hello, Express!');
});

app.get('/api/analysis/:selectedJobTitle', (req, res) => {
  const selectedJobTitle = req.params.selectedJobTitle;
  console.error(`Selected Job Title: ${selectedJobTitle}`);
  console.error('hi');
  const query = `SELECT * FROM \`${selectedJobTitle}\` ORDER BY id DESC LIMIT 1`;
  connection.query(query, (err, rows) => {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal Server Error' });
      return;
    }

    if (rows.length === 0) {
      res.status(404).json({ error: 'Data not found' });
      return;
    }

    delete rows[0].id;
    delete rows[0].Go;
    const row = Object.entries(rows[0]).sort((a, b) => b[1] - a[1]).slice(0, 6);
    res.json(row);
  });
});


app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
