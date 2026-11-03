import { put } from '@vercel/blob';

// Receives one file as a raw request body and stores it in Vercel Blob.
// Returns { url, filename } — the URL is then attached to the Airtable record.
export default async function handler(req, res) {
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

  try {
    const rawName = String(req.headers['x-filename'] || 'upload');
    const filename = decodeURIComponent(rawName).replace(/[^\w.\- ]+/g, '_').slice(0, 120) || 'upload';
    const contentType = String(req.headers['content-type'] || 'application/octet-stream');

    let body = req.body;
    if (!body || !(body instanceof Buffer)) {
      const chunks = [];
      for await (const chunk of req) chunks.push(chunk);
      body = Buffer.concat(chunks);
    }
    if (!body.length) return res.status(400).json({ error: 'Empty file' });

    const blob = await put(`registrations/${filename}`, body, {
      access: 'public',
      contentType,
      addRandomSuffix: true
    });

    return res.status(200).json({ url: blob.url, filename });
  } catch (err) {
    console.error('upload failed', err);
    const missingToken = /no token found|BLOB_READ_WRITE_TOKEN/i.test(String(err && err.message));
    return res.status(500).json({
      error: missingToken
        ? 'File storage is not configured on the server. Please notify the secretariat.'
        : 'Upload failed. Please try again.'
    });
  }
}
