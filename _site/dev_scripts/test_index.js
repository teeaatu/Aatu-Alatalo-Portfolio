const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('http://localhost:4000/recent.html');
  
  // Wait for the page to be loaded
  await page.waitForTimeout(2000);
  
  // Click the index button
  await page.click('#jd-index-btn-bottom');
  
  // Check if panel is open
  const classes = await page.evaluate(() => document.body.className);
  console.log("Body classes after click: ", classes);
  
  await page.waitForTimeout(1000);
  const classes2 = await page.evaluate(() => document.body.className);
  console.log("Body classes after 1s: ", classes2);
  
  await browser.close();
})();
