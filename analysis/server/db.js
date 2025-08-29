const mysql = require("mysql2/promise");

const dbConfig = {
  host: "db",
  port: 3306,
  user: "testuser",
  password: "testpass",
  database: "testdb",
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
};

const pool = mysql.createPool(dbConfig);

module.exports = { pool };
