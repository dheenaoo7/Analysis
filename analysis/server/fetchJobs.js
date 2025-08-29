const axios = require("axios");
const { chromium } = require("playwright");
const { pool } = require("./db");
const { keywordsSkills, patterns } = require("./keywords");

const roles = ["Data_Scientist", "Business_analyst", "Software_engineer"];
const ADZUNA_APP_ID = "0e5c5cd5";
const ADZUNA_APP_KEY = "ac5fcd0adb8444ec2503c34a94a44a78";
const ADZUNA_COUNTRY = "in";
const RESULTS_PER_PAGE = 50;
const MAX_PAGES = 3;

async function fetchAndStoreJobs() {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now - start + (start.getTimezoneOffset() - now.getTimezoneOffset()) * 60 * 1000;
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);
  const runId = `${dayOfYear}${now.getFullYear()}`;

  try {

    for (const role of roles) {
      const skillCounts = {};
      Object.values(keywordsSkills).forEach((val) => (skillCounts[val] = 0));

      for (let page = 1; page <= MAX_PAGES; page++) {
        const url = `https://api.adzuna.com/v1/api/jobs/${ADZUNA_COUNTRY}/search/${page}`;
        const params = {
          app_id: ADZUNA_APP_ID,
          app_key: ADZUNA_APP_KEY,
          what: role,
          results_per_page: RESULTS_PER_PAGE,
        };

        try {
          const resp = await axios.get(url, { params, timeout: 15000 });
          const results = resp.data.results || [];

          results.forEach((item) => {
            let desc = item.description || "";
            if (item.redirect_url) {
              const fullText = fetchFullDescriptionWithBrowser(item.redirect_url);
              if (fullText) {
                desc = fullText;
              }
            }
            for (const [kw, pat] of Object.entries(patterns)) {
              if (pat.test(desc)) {
                skillCounts[keywordsSkills[kw]] += 1;
              }
            }
          });
        } catch (err) {
          console.error("Adzuna API error:", err.message);
        }
      }

      const qry = "INSERT INTO analysis (id, role, data) VALUES (?, ?, ?)";
      await pool.execute(qry, [runId, role, JSON.stringify(skillCounts)]);
    }
  } catch (err) {
    console.error("Database error:", err.message);
  }
}

async function fetchFullDescriptionWithBrowser(url) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
  const content = await page.textContent("body");
  await browser.close();
  return content;
}

module.exports = { fetchAndStoreJobs };
