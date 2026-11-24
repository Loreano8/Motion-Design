// Rendu image par image d'un film HTML qui expose window.renderAt(t) et window.__ready.
// Usage : node tools/render.js <film.html> [secondes=8] [fps=60] [largeur=1920] [hauteur=1080] [sortie=film.mp4]
// Rend les images 0 à N-1 (jamais N), les envoie à ffmpeg : H.264 High, yuv420p, faststart.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');

const [file, secs = 8, fps = 60, W = 1920, H = 1080, out = 'film.mp4'] = process.argv.slice(2);
if (!file) { console.error('usage: node tools/render.js film.html [secs] [fps] [w] [h] [out]'); process.exit(1); }

(async () => {
  const N = Math.round(Number(secs) * Number(fps));
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-profile:v', 'high', '-preset', 'slow', '-crf', '16',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });

  const browser = await chromium.launch({ args: ['--ignore-gpu-blocklist', '--enable-gpu'] });
  const page = await browser.newPage({ viewport: { width: Number(W), height: Number(H) } });
  await page.goto('file://' + path.resolve(file) + '?render=1');
  await page.waitForFunction('window.__ready === true', null, { timeout: 60000 });

  for (let i = 0; i < N; i++) {
    await page.evaluate(t => window.renderAt(t), i / Number(fps));
    const png = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % Number(fps) === 0) process.stdout.write(`\r${i}/${N}`);
  }
  await browser.close();
  ff.stdin.end();
  ff.on('close', code => { console.log(`\n${out} (${N} images)`); process.exit(code); });
})();
