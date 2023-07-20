const express = require('express');
const mysql = require('mysql');
const Chart = require('chart.js');

const app = express();
const port = 3000;

// Create a MySQL connection
const connection = mysql.createConnection({
    host: "analysis.cyufabl1vpsa.ap-northeast-1.rds.amazonaws.com",
    user: "admin",
    password: "admin123",
    database: "analysis"
});

// Connect to MySQL
connection.connect((err) => {
  if (err) throw err;
  console.log('Connected to MySQL!');
});

// Define a route to fetch the data from MySQL and render the chart
app.get('/', (req, res) => {
  const query = 'SELECT * FROM analysis order by id desc limit 1'; // Modify this query to fetch your data
  connection.query(query, (err, rows) => {
    if (err) throw err;
    delete rows[0].id;
    delete rows[0].Go;
    const labels = Object.keys(rows[0]);
    const data = Object.values(rows[0]);

    const chartData = {
      labels: labels,
      datasets: [{
        label: 'Data',
        data: data,
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    };

    // Render the chart
    const chartHTML = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Bar Chart</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      </head>
      <body>
        <canvas id="chartCanvas"></canvas>
        <script>
          const ctx = document.getElementById('chartCanvas').getContext('2d');
          new Chart(ctx, {
            type: 'bar',
            data: ${JSON.stringify(chartData)},
            options: {
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
        </script>
      </body>
      </html>
    `;

    res.send(chartHTML);
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
