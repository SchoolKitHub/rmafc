// Creates the Airtable registration record and emails the delegate a confirmation.
//
// Environment variables (Vercel → Settings → Environment Variables):
//   AIRTABLE_TOKEN      Airtable personal access token, scopes: data.records:write
//   AIRTABLE_BASE_ID    e.g. appXXXXXXXXXXXXXX
//   AIRTABLE_TABLE      table name, default "Registrations"
//   RESEND_API_KEY      Resend API key (optional — omit to skip the email)
//   MAIL_FROM           e.g. "RMAFC Summit <summit@rmafc.gov.ng>"
//   MAIL_REPLY_TO       optional inbox that receives replies to the confirmation
//   MAIL_BCC            optional secretariat address copied on every confirmation
//   RESEND_AUDIENCE_ID  optional legacy audience id; omit to add registrants as global contacts
//   BLOB_READ_WRITE_TOKEN  added automatically when you create a Blob store

const AIRTABLE_BASE_ID = process.env.AIRTABLE_BASE_ID || 'appoMRpjGyCkdRKob';

const TEXT = {
  required: 'A full name and a valid email address are required.',
  server: 'Registration could not be saved. Please try again or email the secretariat.'
};

function reference() {
  const n = Math.floor(Math.random() * 9000) + 1000;
  return `RMAFC26-${n}`;
}

async function airtableCreate(fields) {
  const table = encodeURIComponent(process.env.AIRTABLE_TABLE || 'Registrations');
  const r = await fetch(`https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/${table}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.AIRTABLE_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ records: [{ fields }], typecast: true })
  });
  if (!r.ok) throw new Error(`Airtable ${r.status}: ${await r.text()}`);
  return r.json();
}

function confirmationHtml(d, ref) {
  return `<!doctype html><html><body style="margin:0;background:#f4f5f2;padding:28px 16px;font-family:Georgia,'Times New Roman',serif;color:#14203a;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;margin:0 auto;background:#ffffff;border:1px solid #dcdfd8;">
    <tr><td align="center" style="background:#ffffff;padding:26px 30px 20px;border-bottom:3px solid #0b6b3a;">
      <img src="https://www.rmafcinvestmentsummit2026.org/assets/coat-of-arms.png" width="86" height="73" alt="Federal Republic of Nigeria coat of arms" style="display:block;margin:0 auto 10px;border:0;width:86px;height:73px;">
      <div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;letter-spacing:.14em;color:#c8102e;">THE PRESIDENCY</div>
      <div style="font-family:Helvetica,Arial,sans-serif;font-size:11px;letter-spacing:.08em;color:#14203a;padding-top:4px;">Revenue Mobilisation Allocation and Fiscal Commission</div>
    </td></tr>
    <tr><td style="background:#0b1526;padding:26px 30px;">
      <div style="font-family:Helvetica,Arial,sans-serif;font-size:19px;font-weight:700;letter-spacing:.04em;color:#f2f4f1;">RMAFC SUMMIT 2026</div>
      <div style="font-family:Helvetica,Arial,sans-serif;font-size:10px;letter-spacing:.16em;color:#a9b4c7;padding-top:6px;">OIL &amp; GAS INVESTMENT &middot; BEIJING</div>
    </td></tr>
    <tr><td style="padding:30px;">
      <p style="margin:0 0 18px;font-size:17px;line-height:1.6;">Dear ${d.fullName || 'Delegate'},</p>
      <p style="margin:0 0 18px;font-size:17px;line-height:1.6;">Your registration for the 2026 Oil &amp; Gas Investment Summit, holding 24 and 25 February 2027 in Beijing, has been received by the Revenue Mobilisation Allocation and Fiscal Commission.</p>
      <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-top:1px solid #dcdfd8;margin:0 0 22px;font-family:Helvetica,Arial,sans-serif;font-size:14px;">
        <tr><td style="padding:12px 0 4px;color:#61708c;">Reference</td><td style="padding:12px 0 4px;text-align:right;">${ref}</td></tr>
        <tr><td style="padding:4px 0;color:#61708c;">Category</td><td style="padding:4px 0;text-align:right;">${d.category || '—'}</td></tr>
        <tr><td style="padding:4px 0;color:#61708c;">Organization</td><td style="padding:4px 0;text-align:right;">${d.company || '—'}</td></tr>
        <tr><td style="padding:4px 0 12px;color:#61708c;">Documents attached</td><td style="padding:4px 0 12px;text-align:right;">${(d.attachments || []).length}</td></tr>
      </table>
      <p style="margin:0 0 18px;font-size:17px;line-height:1.6;">The secretariat will be in touch with venue, hotel, airport, visa and local travel information, along with programme updates as sessions are confirmed.</p>
      <p style="margin:0;font-size:17px;line-height:1.6;">Revenue Mobilisation Allocation and Fiscal Commission</p>
    </td></tr>
  </table></body></html>`;
}

async function sendConfirmation(d, ref) {
  if (!process.env.RESEND_API_KEY || !process.env.MAIL_FROM) return;
  const payload = {
    from: process.env.MAIL_FROM,
    to: [d.email],
    subject: `Registration received — RMAFC Summit 2026 (${ref})`,
    html: confirmationHtml(d, ref)
  };
  if (process.env.MAIL_BCC) payload.bcc = [process.env.MAIL_BCC];
  if (process.env.MAIL_REPLY_TO) payload.reply_to = process.env.MAIL_REPLY_TO;
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  if (!r.ok) console.error('confirmation email failed', await r.text());
}

// Adds the registrant to Resend Contacts so they can receive broadcasts.
// Uses a global contact unless RESEND_AUDIENCE_ID is set (legacy audiences).
async function addContact(d) {
  if (!process.env.RESEND_API_KEY) return;
  const parts = String(d.fullName || '').trim().split(/\s+/);
  const audience = process.env.RESEND_AUDIENCE_ID;
  const url = audience
    ? `https://api.resend.com/audiences/${audience}/contacts`
    : 'https://api.resend.com/contacts';
  const r = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: String(d.email).trim(),
      first_name: parts[0] || '',
      last_name: parts.slice(1).join(' '),
      unsubscribed: false
    })
  });
  if (!r.ok) console.error('add contact failed', await r.text());
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

  const d = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  if (!d.fullName || !String(d.fullName).trim() || !String(d.email || '').includes('@')) {
    return res.status(400).json({ error: TEXT.required });
  }

  const ref = reference();
  const attachments = Array.isArray(d.attachments) ? d.attachments.slice(0, 20) : [];

  try {
    await airtableCreate({
      Reference: ref,
      Category: d.category || '',
      'Full name': String(d.fullName).trim(),
      Organization: d.company || '',
      Position: d.position || '',
      Country: d.country || '',
      Email: String(d.email).trim(),
      Phone: d.phone || '',
      'Area of interest': d.interest || '',
      'Dietary requirements': d.dietary || '',
      'Investment interests': d.investment || '',
      'Other information': d.other || '',
      Documents: attachments.map(a => ({ url: a.url, filename: a.filename })),
      Status: 'New',
      'Submitted at': new Date().toISOString()
    });
  } catch (err) {
    console.error('airtable failed', err);
    return res.status(500).json({ error: TEXT.server });
  }

  try {
    await sendConfirmation({ ...d, attachments }, ref);
  } catch (err) {
    console.error('email failed', err);
  }

  try {
    await addContact(d);
  } catch (err) {
    console.error('contact failed', err);
  }

  return res.status(200).json({ ok: true, reference: ref });
}
