# RMAFC Summit 2026 — deploy this folder

Do not upload index.html on its own. The two files in /api are what save
registrations to Airtable and store uploaded documents. Without them the form
falls back to preview mode and nothing is saved.

## Deploy

Drag this WHOLE FOLDER onto vercel.com/new (not the individual files).

Folder contents:

  index.html        the website
  assets/hero.mp4   hero background video - must stay in the assets folder
  api/register.js   creates the Airtable record, sends the confirmation email
  api/upload.js     stores each uploaded file in Vercel Blob
  api/diag.js       /api/diag?key=rmafc-diag - checks the Airtable wiring
  package.json      tells Vercel to install @vercel/blob

The hero video is the only asset kept outside index.html, so the page stays
light. If assets/hero.mp4 is missing the hero falls back to the FPSO still
image, which is embedded in the page.

## Then, in the Vercel project

Settings -> Environment Variables:

  AIRTABLE_TOKEN    pat... token from airtable.com/create/tokens
                    scopes: data.records:write, schema.bases:read
                    access: the summit base only

  (AIRTABLE_BASE_ID is already built in: appoMRpjGyCkdRKob)

Optional, for the delegate confirmation email:

  RESEND_API_KEY    from resend.com
  MAIL_FROM         RMAFC Summit <summit@yourverifieddomain>
  MAIL_BCC          secretariat address copied on every confirmation

Storage -> connect the rmafc-summit-china-blob store to this project.

Redeploy after adding variables, then submit a test registration on the live
URL. A successful submission shows a REFERENCE number and no preview notice.

## Checking it worked

Airtable -> Registrations table: one row per delegate, files in Documents.
Vercel -> Logs: if a submission fails, the reason appears there. The usual
cause is a column name in Airtable that does not match exactly.

## SEO and analytics

Also in this folder:

  robots.txt        lets search engines crawl everything except /api
  sitemap.xml       the six pages, with Chinese (?lang=zh) alternates
  vercel.json       serves /about, /programme, /opportunities, /register, /news
  assets/og-image.jpg  1200x630 image shown when the link is shared

The <head> of index.html carries the page title, description, share tags,
structured data (Event + Organisation), Google Tag Manager and Hotjar.

Google Analytics 4 (G-XCRN0DWXFF) - loaded directly in <head>
  Events sent: page_view (each page), generate_lead (successful registration,
  with registration_category / area_of_interest / country), language_change,
  official_site_click (rmafc.gov.ng), outbound_click.
  GA Admin -> Events: mark generate_lead as a key event (conversion).
  GA Admin -> Custom definitions: add event-scoped dimensions
  registration_category, area_of_interest, language to see them in reports.

Google Tag Manager (GTM-TNMWCSKX) is also installed for future tags.
  Do NOT add a GA4 / Google tag inside GTM, or every visit is counted twice.

Google Search Console (verified by file)
  google9aa8c88aaddc1d7e.html must stay in the root of this folder.
  1. After deploying, check https://www.rmafcinvestmentsummit2026.org/google9aa8c88aaddc1d7e.html
     opens, then click Verify in Search Console.
  2. Sitemaps -> submit sitemap.xml
  3. Link Search Console to the GA4 property (GA Admin -> Product links).

If the site moves to its own domain, replace rmafcinvestmentsummit2026.org
in index.html, sitemap.xml and robots.txt.
