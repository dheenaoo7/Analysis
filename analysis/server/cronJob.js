const cron = require("node-cron");
const { fetchAndStoreJobs } = require("./fetchJobs");

cron.schedule("0 0 * * *", () => {
  console.log("Scheduled cron running:", new Date());
  fetchAndStoreJobs();
}, {
  timezone: "Asia/Kolkata",
});
