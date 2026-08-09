const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
  page.on('requestfailed', request => console.log('REQUEST FAILED:', request.url(), request.failure().errorText));

  console.log('Navigating...');
  await page.goto('http://localhost:4000/recent.html', { waitUntil: 'networkidle2' });
  
  console.log('Clicking index button...');
  await page.click('#jd-index-btn-bottom');
  
  await page.waitForTimeout(1000); // wait for animation
  
  const isOpen = await page.evaluate(() => {
    const panel = document.getElementById('jd-index-panel');
    return panel ? panel.classList.contains('is-open') : false;
  });
  
  console.log('Is panel open? ', isOpen);
  
  await browser.close();
})();
