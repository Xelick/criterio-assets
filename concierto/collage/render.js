// node render.js <layer> <out_dir> <frames...|f0-f1>   (frame f is drawn at t = f/24)
const { chromium } = require('playwright');
const path = require('path');
const [layer, out, ...spec] = process.argv.slice(2);
const frames = spec.flatMap(s => {
  if (!s.includes('-')) return [+s];
  const [a, b] = s.split('-').map(Number);
  return Array.from({length: b - a + 1}, (_, i) => a + i);
});
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({viewport: {width: 1920, height: 1080}, deviceScaleFactor: 1});
  page.on('pageerror', e => console.error('pageerror', e.message));
  page.on('console', m => console.log('console', m.text()));
  await page.goto('file://' + path.join(__dirname, 'index.html') + '?layer=' + layer);
  await page.waitForFunction('window.READY === true');
  for (const f of frames) {
    await page.evaluate(t => window.render(t), f / 24);
    await page.screenshot({path: path.join(out, `${layer}_${String(f).padStart(4, '0')}.png`), omitBackground: true});
  }
  await browser.close();
})();
