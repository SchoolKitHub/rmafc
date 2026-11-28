// SMS through Termii (https://developers.termii.com).
//
// Environment variables (Vercel → Settings → Environment Variables):
//   TERMII_API_KEY     API key from the Termii dashboard
//   TERMII_SENDER_ID   approved sender ID, e.g. "RMAFCSummit" (3–11 characters)
//   TERMII_BASE_URL    optional; your account's base URL from the dashboard
//                      (default https://v3.api.termii.com)
//
// Nigerian rules this follows:
//   - Transactional messages (registration receipts) go on the "dnd" route,
//     which reaches numbers on the Do-Not-Disturb list. Never put marketing on it.
//   - Promotional messages go on the "generic" route, only 08:00–20:00 WAT,
//     and carry an opt-out line. The generic route does not reach DND numbers.

const BASE = (process.env.TERMII_BASE_URL || 'https://v3.api.termii.com').replace(/\/$/, '');

// Accepts 0803..., +234803..., 234803..., 803... and returns 234XXXXXXXXXX, or ''.
export function normalisePhone(raw, defaultCountry = '234') {
  let d = String(raw || '').replace(/[^\d+]/g, '');
  if (!d) return '';
  if (d.startsWith('+')) d = d.slice(1);
  else if (d.startsWith('00')) d = d.slice(2);
  else if (d.startsWith('0') && d.length === 11) d = defaultCountry + d.slice(1);
  else if (d.length === 10 && /^[789]/.test(d)) d = defaultCountry + d;
  return /^\d{10,15}$/.test(d) ? d : '';
}

export function smsConfigured() {
  return Boolean(process.env.TERMII_API_KEY && process.env.TERMII_SENDER_ID);
}

// kind: 'transactional' (dnd route) or 'promotional' (generic route)
export async function sendSms(to, text, kind = 'transactional') {
  const number = normalisePhone(to);
  if (!number) return { ok: false, error: 'invalid number' };
  if (!smsConfigured()) return { ok: false, error: 'SMS not configured' };
  const r = await fetch(`${BASE}/api/sms/send`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      api_key: process.env.TERMII_API_KEY,
      to: number,
      from: process.env.TERMII_SENDER_ID,
      sms: text,
      type: 'plain',
      channel: kind === 'promotional' ? 'generic' : 'dnd'
    })
  });
  const body = await r.json().catch(() => ({}));
  return r.ok ? { ok: true, id: body.message_id, balance: body.balance } : { ok: false, error: body.message || `HTTP ${r.status}` };
}
