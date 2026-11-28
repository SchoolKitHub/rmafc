// Bulk SMS sender for summit campaigns (Termii).
//
//   TERMII_API_KEY=... TERMII_SENDER_ID=RMAFCSummit \
//   node tools/sms/send.mjs --list contacts.csv --message message.txt [--kind promotional|transactional] [--send]
//
// contacts.csv: a header row with at least `phone`; `name` is optional and fills {name}.
// Without --send it is a dry run: it prints what would go out and sends nothing.
//
// Safeguards:
//   - promotional sends only between 08:00 and 20:00 Lagos time, and always end with the opt-out line
//   - numbers in tools/sms/optout.txt (one per line, any format) are never messaged
//   - duplicates and invalid numbers are skipped
//   - every result is written to tools/sms/logs/<timestamp>.csv
import fs from 'node:fs';
import path from 'node:path';
import { normalisePhone, sendSms } from '../../lib/sms.js';

const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, all) => {
  if (v.startsWith('--')) a.push([v.slice(2), all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true]);
  return a;
}, []));
const kind = args.kind || 'promotional';
const live = args.send === true;
const OPTOUT = 'Reply STOP to opt out.';
if (!args.list || !args.message) { console.error('Usage: --list contacts.csv --message message.txt [--kind promotional|transactional] [--send]'); process.exit(1); }

let text = fs.readFileSync(args.message, 'utf8').trim();
if (kind === 'promotional' && !text.includes('STOP')) text += ' ' + OPTOUT;

const hourLagos = Number(new Intl.DateTimeFormat('en-GB', { hour: 'numeric', hour12: false, timeZone: 'Africa/Lagos' }).format(new Date()));
if (live && kind === 'promotional' && (hourLagos < 8 || hourLagos >= 20)) {
  console.error(`It is ${hourLagos}:00 in Lagos. Promotional SMS may only go out 08:00–20:00. Nothing sent.`); process.exit(1);
}

const here = path.dirname(new URL(import.meta.url).pathname);
const optFile = path.join(here, 'optout.txt');
const optout = new Set((fs.existsSync(optFile) ? fs.readFileSync(optFile, 'utf8') : '').split(/\r?\n/).map(l => normalisePhone(l)).filter(Boolean));

function parseCsv(s) {
  const rows = []; let row = [], cell = '', q = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (q) { if (c === '"' && s[i + 1] === '"') { cell += '"'; i++; } else if (c === '"') q = false; else cell += c; }
    else if (c === '"') q = true; else if (c === ',') { row.push(cell); cell = ''; }
    else if (c === '\n' || c === '\r') { if (c === '\r' && s[i + 1] === '\n') i++; row.push(cell); rows.push(row); row = []; cell = ''; }
    else cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  return rows.filter(r => r.some(x => x.trim()));
}
const [head, ...rows] = parseCsv(fs.readFileSync(args.list, 'utf8'));
const h = head.map(x => x.trim().toLowerCase());
const pi = h.indexOf('phone'), ni = h.indexOf('name');
if (pi < 0) { console.error('The CSV needs a "phone" column.'); process.exit(1); }

const seen = new Set(), jobs = [], skipped = [];
for (const r of rows) {
  const n = normalisePhone(r[pi]);
  const why = !n ? 'invalid' : optout.has(n) ? 'opted out' : seen.has(n) ? 'duplicate' : '';
  if (why) { skipped.push([r[pi], why]); continue; }
  seen.add(n);
  const name = ni >= 0 ? (r[ni] || '').trim().split(/\s+/)[0] : '';
  jobs.push([n, text.replace(/\{name\}/g, name || 'Sir/Madam')]);
}
const len = Math.max(0, ...jobs.map(j => j[1].length));
const parts = len <= 160 ? 1 : Math.ceil(len / 153);
console.log(`${jobs.length} to send, ${skipped.length} skipped (${kind}, ${live ? 'LIVE' : 'dry run'}). Longest message: ${len} characters = ${parts} SMS part(s); the unit cost is per part.`);
skipped.forEach(([p, w]) => console.log(`  skip ${p}: ${w}`));
if (!live) { jobs.slice(0, 3).forEach(([n, t]) => console.log(`  ${n}: ${t}`)); console.log('Dry run only. Add --send to send.'); process.exit(0); }

fs.mkdirSync(path.join(here, 'logs'), { recursive: true });
const log = path.join(here, 'logs', new Date().toISOString().replace(/[:.]/g, '-') + '.csv');
fs.writeFileSync(log, 'phone,status,detail\n');
let ok = 0;
for (const [n, t] of jobs) {
  const r = await sendSms(n, t, kind);
  if (r.ok) ok++;
  fs.appendFileSync(log, `${n},${r.ok ? 'sent' : 'failed'},"${String(r.ok ? r.id : r.error).replace(/"/g, "'")}"\n`);
  await new Promise(res => setTimeout(res, 250));
}
console.log(`Sent ${ok} of ${jobs.length}. Log: ${log}`);
