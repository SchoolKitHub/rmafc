// Diagnostic — visit /api/diag?key=rmafc-diag on the deployed site.
// Reports what the Airtable token can actually see and whether the
// Registrations table has the field names api/register.js expects.
// Requires the token scope: schema.bases:read

const BASE = process.env.AIRTABLE_BASE_ID || 'appoMRpjGyCkdRKob';
const TABLE = process.env.AIRTABLE_TABLE || 'Registrations';

const EXPECTED = [
  'Reference', 'Category', 'Full name', 'Organization', 'Position', 'Country',
  'Email', 'Phone', 'Area of interest', 'Accommodation', 'Investment interests',
  'Other information', 'Documents', 'Status', 'Submitted at'
];

export default async function handler(req, res) {
  const url = new URL(req.url, 'http://localhost');
  if (url.searchParams.get('key') !== 'rmafc-diag') return res.status(404).end();

  const out = {
    baseId: BASE,
    tableExpected: TABLE,
    tokenPresent: Boolean(process.env.AIRTABLE_TOKEN),
    blobTokenPresent: Boolean(process.env.BLOB_READ_WRITE_TOKEN),
    resendConfigured: Boolean(process.env.RESEND_API_KEY && process.env.MAIL_FROM)
  };

  if (!out.tokenPresent) {
    out.verdict = 'AIRTABLE_TOKEN is not set on this deployment.';
    return res.status(200).json(out);
  }

  const headers = { Authorization: `Bearer ${process.env.AIRTABLE_TOKEN}` };

  const basesRes = await fetch('https://api.airtable.com/v0/meta/bases', { headers });
  const basesBody = await basesRes.text();
  if (!basesRes.ok) {
    out.verdict = 'The token could not list bases. Add scope schema.bases:read, or the token is invalid.';
    out.airtableStatus = basesRes.status;
    out.airtableSays = basesBody.slice(0, 400);
    return res.status(200).json(out);
  }

  const bases = JSON.parse(basesBody).bases || [];
  out.basesTokenCanSee = bases.map(b => ({ id: b.id, name: b.name }));
  out.targetBaseInTokenAccess = bases.some(b => b.id === BASE);

  if (!out.targetBaseInTokenAccess) {
    out.verdict = `The token has no access to ${BASE}. On airtable.com/create/tokens, edit the token and add this base under Access.`;
    return res.status(200).json(out);
  }

  const schemaRes = await fetch(`https://api.airtable.com/v0/meta/bases/${BASE}/tables`, { headers });
  const schemaBody = await schemaRes.text();
  if (!schemaRes.ok) {
    out.verdict = 'Base is in the token access list but its schema could not be read.';
    out.airtableStatus = schemaRes.status;
    out.airtableSays = schemaBody.slice(0, 400);
    return res.status(200).json(out);
  }

  const tables = JSON.parse(schemaBody).tables || [];
  out.tablesInBase = tables.map(t => t.name);

  const table = tables.find(t => t.name === TABLE);
  if (!table) {
    out.verdict = `No table named "${TABLE}". Rename your table to match, or set AIRTABLE_TABLE to one of the names above.`;
    return res.status(200).json(out);
  }

  const actual = table.fields.map(f => f.name);
  const missing = EXPECTED.filter(n => !actual.includes(n));
  const documents = table.fields.find(f => f.name === 'Documents');

  out.fieldsInTable = actual;
  out.missingFields = missing;
  out.documentsFieldType = documents ? documents.type : null;

  const documentsOk = documents && documents.type === 'multipleAttachments';
  if (missing.length) {
    out.verdict = `Table found, but these columns are missing or spelled differently: ${missing.join(', ')}`;
  } else if (!documentsOk) {
    out.verdict = 'All columns present, but "Documents" must be an Attachment field.';
  } else {
    out.verdict = 'All good. Registrations should save.';
  }

  return res.status(200).json(out);
}
