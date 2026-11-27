#!/usr/bin/env node
// Render an animated HTML scene to a JPEG frame sequence (1080x1920) for tools/make_short.py --frames.
// The page must define window.renderFrame(t) and may define window.setup(data).
//
// Usage: node tools/render_frames.js <scene.html> <seconds> <out_dir> [fps=30] [durations.txt]
// durations.txt (from voice_kokoro.py) is passed to setup() as {durations:[...]}.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const [html, secs, outDir, fpsArg, dursFile] = process.argv.slice(2);
  if (!html || !secs || !outDir) { console.error('usage: render_frames.js scene.html seconds out_dir [fps] [durations.txt]'); process.exit(1); }
  const fps = Number(fpsArg || 30), total = Math.ceil(Number(secs) * fps);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  if (dursFile) {
    const durations = fs.readFileSync(dursFile, 'utf8').trim().split(',').map(Number);
    await page.evaluate((d) => window.setup && window.setup({ durations: d }), durations);
  }
  for (let f = 0; f < total; f++) {
    await page.evaluate((t) => window.renderFrame(t), f / fps);
    await page.screenshot({ path: path.join(outDir, String(f).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 88 });
    if (f % 300 === 0) console.log(`frame ${f}/${total}`);
  }
  await browser.close();
  console.log(`✅ ${total} frames -> ${outDir}`);
})();
