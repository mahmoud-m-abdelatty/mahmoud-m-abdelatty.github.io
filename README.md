# Personal academic website - Mahmoud M. Abdelatty

Static academic site: Times New Roman, justified text, figure carousel from the
open-access Scientific Reports paper, citation metrics, publications, and a
contact & collaboration page. Works offline too: unzip and open `index.html`.
Do not edit the HTML by hand: edit `data/*.json` or `scripts/build_site.py`,
then run `python3 scripts/build_site.py`.

## Current status

- Pages, carousel, publications with verified Google Scholar per-paper counts
  and dates, metrics table with a per-database "as of" column.
- Contact form live through Formspree (endpoint
  `https://formspree.io/f/mjywllwd`); verified end-to-end with a test
  submission on 26 Nov 2026.
- Weekly metric refresh via the included GitHub Actions workflow
  (`.github/workflows/update-metrics.yml`).
  - Automatic: OpenAlex row (citations, h-index) and detection of new
    publications indexed in OpenAlex.
  - Not automatic: Google Scholar (no public API; Scholar blocks automated
    access) and Scopus (needs an Elsevier API key, free via the university).
    New papers that appear on Scholar but not yet in OpenAlex are picked up
    at the next manual re-check, not automatically.
  - Dates only move forward on a successful fetch; a failed run keeps the
    last good numbers and their dates.
- Visitor counter: GoatCounter (no cookies). Every page footer shows the
  number of unique visitors to the site, read from GoatCounter's public
  TOTAL endpoint (cached up to four hours). Dashboard
  `https://mahmoud-abdelatty.goatcounter.com`.

## Stack (free tier, $0)

| Piece | Service | Cost |
|---|---|---|
| Hosting + weekly automation | GitHub Pages + Actions | $0 (Actions free for public repositories) |
| Contact form | Formspree Free | $0, 50 submissions/month, 30-day archive |
| Visitor counter | GoatCounter hosted | $0, donation-supported |

The site is published with GitHub Pages from the `main` branch at
`https://mahmoud-m-abdelatty.github.io/`.

## Alternatives

- Netlify or Cloudflare Pages can host the same folder for free; Netlify has
  built-in forms. See their current pricing pages for limits.
- Google Forms can be embedded using the owner's existing Google account (no
  new service sign-up), at the cost of Google branding on the form.
- A custom domain (~$10-15/year) is optional and never required.

## Data files

- `data/metrics.json` - one block per database, each with its own `as_of`
  date. Scholar and Scopus blocks change only on a manual re-check.
- `data/publications.json` - `scholar_citations` per paper are verified
  against the live Scholar profile (`scholar_as_of`) and are never
  overwritten automatically; `openalex_citations` refresh weekly.
