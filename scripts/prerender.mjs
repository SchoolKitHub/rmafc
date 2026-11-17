// Prerender: bake each page's rendered content into its static HTML.
//
// Every page ships as a self-unpacking bundle: the HTML a crawler downloads
// holds ~18 words ("Unpacking...") and the real content only exists after the
// bundle runs. Google renders it eventually; Baidu, Bing, link previews and AI
// crawlers mostly don't. This script renders each page in headless Chromium,
// takes the visible content as plain semantic HTML, and writes it into the
// page's <body> between the prerender markers. When the bundle unpacks it
// replaces the whole document, so visitors still get the normal site.
//
// Run after every rebuild/export of the site, from the repo root:
//   npm i --no-save playwright && npx playwright install chromium
//   node scripts/prerender.mjs
//
// Pages come from sitemap.xml. Rerunning is safe: the old block is replaced.

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const START = '<!-- prerender:start -->';
const END = '<!-- prerender:end -->';
const ANCHOR = '<div id="__bundler_loading">';

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.mp4': 'video/mp4', '.woff2': 'font/woff2', '.pdf': 'application/pdf',
  '.xml': 'application/xml', '.txt': 'text/plain' };

// Static server with Vercel-style clean URLs (/about -> about.html).
function serve() {
  const server = http.createServer((req, res) => {
    let u = decodeURIComponent(req.url.split('?')[0]);
    let f = path.join(ROOT, u === '/' ? 'index.html' : u);
    if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
    if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f += '.html';
    if (!fs.existsSync(f)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  });
  return new Promise(r => server.listen(0, '127.0.0.1', () => r(server)));
}

function pagesFromSitemap() {
  const xml = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
  return [...xml.matchAll(/<loc>https?:\/\/[^/]+(\/[^<]*)<\/loc>/g)].map(m => m[1]);
}

const fileFor = p => path.join(ROOT, p === '/' ? 'index.html' : p.replace(/^\//, '') + '.html');

// Runs in the page: serialise visible content to attribute-free semantic HTML.
function extract() {
  const KEEP = new Set(['H1','H2','H3','H4','H5','H6','P','UL','OL','LI','A','STRONG','EM','B','I',
    'HEADER','NAV','MAIN','SECTION','ARTICLE','FOOTER','TABLE','THEAD','TBODY','TR','TD','TH',
    'DL','DT','DD','BLOCKQUOTE','BR','DIV','SPAN']);
  const SKIP = new Set(['SCRIPT','STYLE','NOSCRIPT','SVG','IMG','VIDEO','AUDIO','CANVAS','IFRAME',
    'BUTTON','FORM','INPUT','SELECT','TEXTAREA','TEMPLATE','LINK','META']);
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const escAttr = s => esc(s).replace(/"/g, '&quot;');
  function walk(n) {
    if (n.nodeType === 3) return esc(n.nodeValue.replace(/\s+/g, ' '));
    if (n.nodeType !== 1 || SKIP.has(n.tagName)) return '';
    const cs = getComputedStyle(n);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') return '';
    if (n.getAttribute('aria-hidden') === 'true') return '';
    const inner = [...n.childNodes].map(walk).join('');
    if (!inner.trim() && n.tagName !== 'BR') return '';
    if (!KEEP.has(n.tagName)) return inner;
    if (n.tagName === 'BR') return '<br>';
    let tag = n.tagName.toLowerCase(), attrs = '';
    if (tag === 'a') {
      const href = n.getAttribute('href');
      if (!href || href.startsWith('javascript:') || href === '#') return inner;
      attrs = ` href="${escAttr(href)}"`;
    }
    if (tag === 'span') return inner + ' ';
    return `<${tag}${attrs}>${inner.trim()}</${tag}>`;
  }
  return walk(document.body).replace(/<div>(\s*)<\/div>/g, '').replace(/\s{2,}/g, ' ');
}

const STYLE = '<style>#prerender{max-width:960px;margin:0 auto;padding:24px 16px 64px;' +
  'font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#1b2333}' +
  '#prerender a{color:#0d7a4f}#prerender h1,#prerender h2,#prerender h3{line-height:1.2}' +
  '#prerender nav,#prerender header{display:flex;flex-wrap:wrap;gap:4px 16px}</style>';

const server = await serve();
const base = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch();
let failed = 0;

for (const p of pagesFromSitemap()) {
  const file = fileFor(p);
  if (!fs.existsSync(file)) { console.warn('skip, no file:', p); continue; }
  const ctx = await browser.newContext({ locale: 'en-GB', viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  try {
    await page.goto(base + p, { waitUntil: 'load' });
    await page.waitForSelector('h1', { timeout: 20000 });
    await page.waitForTimeout(1500);
    const body = await page.evaluate(extract);
    const words = body.replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length;
    if (words < 50) throw new Error(`only ${words} words rendered`);
    let html = fs.readFileSync(file, 'utf8');
    const block = `${START}\n  ${STYLE}<div id="prerender">${body}</div>\n  ${END}\n  `;
    const s = html.indexOf(START), e = html.indexOf(END);
    if (s !== -1 && e > s) {
      html = html.slice(0, s) + block.trimEnd() + html.slice(e + END.length);
    } else {
      const a = html.indexOf(ANCHOR);
      if (a === -1) throw new Error('no ' + ANCHOR + ' in file');
      html = html.slice(0, a) + block + html.slice(a);
    }
    fs.writeFileSync(file, html);
    console.log(`ok   ${p.padEnd(18)} ${words} words`);
  } catch (err) {
    failed++;
    console.error(`FAIL ${p}: ${err.message}`);
  }
  await ctx.close();
}

await browser.close();
server.close();
process.exit(failed ? 1 : 0);
