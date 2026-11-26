"""Build index.html and contact.html from data/*.json. Run after update_metrics.py.
All styling is Times New Roman with justified paragraphs, per the owner's standing rule.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

metrics = json.loads((DATA / "metrics.json").read_text())
pubs = json.loads((DATA / "publications.json").read_text())

CSS = """
body { font-family: 'Times New Roman', Times, serif; margin: 0; color: #1a1a1a; background: #fff; }
header.site { border-bottom: 3px double #1a3a5c; padding: 28px 20px 18px; max-width: 900px; margin: 0 auto; }
header.site h1 { font-size: 30px; margin: 0 0 4px; color: #1a3a5c; }
header.site .role { font-size: 17px; color: #444; }
nav.site { max-width: 900px; margin: 0 auto; padding: 10px 20px; border-bottom: 1px solid #ccc; font-size: 16px; }
nav.site a { margin-right: 22px; color: #1a3a5c; }
main { max-width: 900px; margin: 0 auto; padding: 12px 20px 60px; }
h2 { font-size: 22px; color: #1a3a5c; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 36px; }
p, li { font-size: 16px; line-height: 1.55; text-align: justify; }
.mwrap { overflow-x: auto; }
table.metrics { border-collapse: collapse; margin: 10px 0; }
table.metrics th, table.metrics td { border: 1px solid #bbb; padding: 6px 14px; font-size: 15px; text-align: left; }
table.metrics th { background: #eef2f6; }
.pub { margin: 0 0 14px; }
.pub .status { font-weight: bold; }
.small { font-size: 13px; color: #666; }
a { color: #1a3a5c; }
.carousel { margin: 14px 0 4px; text-align: center; }
.carousel img { max-width: 100%; max-height: 430px; border: 1px solid #ddd; padding: 8px; background: #fff; }
.carousel .bar { margin-top: 8px; display: flex; align-items: center; justify-content: center; gap: 14px; }
.carousel button { font-family: inherit; font-size: 20px; width: 40px; height: 36px; cursor: pointer; }
.carousel .cap { font-size: 14px; color: #555; }
.dots span { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #ccc; margin: 6px 3px 0; }
.dots span.on { background: #1a3a5c; }
form.contact label { display: block; margin: 14px 0 4px; font-size: 16px; }
form.contact input, form.contact textarea { width: 100%; max-width: 560px; font-family: inherit; font-size: 16px; padding: 8px; border: 1px solid #999; }
form.contact button { margin-top: 16px; font-family: inherit; font-size: 17px; padding: 10px 26px; background: #1a3a5c; color: #fff; border: 0; cursor: pointer; }
footer { max-width: 900px; margin: 0 auto; padding: 18px 20px 40px; border-top: 1px solid #ccc; font-size: 13px; color: #666; }
"""

FIGURES = [
    ("assets/pub-scheme1.png", "Scheme 1: synthesis routes of the pyranopyrazole derivatives", "Scheme 1. Synthesis of the pyranopyrazole derivatives."),
    ("assets/pub-fig-antibacterial.png", "Bar chart of inhibition zones for the pyranopyrazole derivatives against four bacterial strains", "Fig. 1. Antibacterial activity against different bacterial strains."),
    ("assets/pub-fig-homolumo.png", "HOMO and LUMO frontier molecular orbital surfaces for compounds 2a, 4a, 5a, 7a and 8a", "Fig. 2. Frontier molecular orbitals (HOMO and LUMO)."),
    ("assets/pub-fig-mep.png", "Molecular electrostatic potential maps of the most active derivatives", "Fig. 5. Molecular electrostatic potential maps of the most active derivatives."),
]
FIGURE_CREDIT = ("Figures from: Abdelatty, M. M. et al. Rational design and antibacterial assessment of novel "
                 "pyranopyrazole derivatives. Scientific Reports 16, 11621 (2026). Open access, CC BY 4.0.")

CAROUSEL_JS = """
let acad_i = 0;
const acad_figs = ACAD_FIGS;
function acad_show(i) {
  acad_i = (i + acad_figs.length) % acad_figs.length;
  const f = acad_figs[acad_i];
  document.getElementById('acad-img').src = f[0];
  document.getElementById('acad-img').alt = f[1];
  document.getElementById('acad-cap').textContent = f[2];
  document.querySelectorAll('.dots span').forEach((d, k) => d.className = k === acad_i ? 'on' : '');
}
setInterval(() => acad_show(acad_i + 1), 4500);
""".replace("ACAD_FIGS", json.dumps([[f[0], f[1], f[2]] for f in FIGURES]))


def esc(s):
    return html.escape(str(s or ""))


def head(title):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
<header class="site">
  <h1>Mahmoud M. Abdelatty</h1>
  <div class="role">Instructor and researcher, Chemistry Department, Faculty of Science, Fayoum University, Egypt</div>
</header>
<nav class="site">
  <a href="index.html">Profile</a>
  <a href="index.html#publications">Publications</a>
  <a href="index.html#metrics">Metrics</a>
  <a href="contact.html">Contact &amp; collaboration</a>
</nav>
"""


COUNTER_SNIPPET = """
<!-- Privacy-friendly visitor counter: GoatCounter (free, donation-supported, no cookies).
Dashboard: https://mahmoud-abdelatty.goatcounter.com -->
<script data-goatcounter="https://mahmoud-abdelatty.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
"""

# Visible counter: reads GoatCounter's public TOTAL endpoint (all pages, all time).
# Requires the GoatCounter setting "Allow adding visitor counts on your website".
# count_unique = unique visitors GoatCounter recorded for the whole site.
# GoatCounter caches this endpoint for up to four hours, so the number lags.
VISITS_SNIPPET = """
<p class="small" id="site-visits" hidden>Unique visitors to this site: <span id="sv-count"></span></p>
<script>
fetch('https://mahmoud-abdelatty.goatcounter.com/counter/TOTAL.json')
  .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
  .then(function (d) {
    document.getElementById('sv-count').textContent = d.count_unique;
    document.getElementById('site-visits').hidden = false;
  })
  .catch(function () { /* counter unavailable; line stays hidden */ });
</script>
"""


def metrics_table():
    gs, sc, oa = metrics["google_scholar"], metrics["scopus"], metrics["openalex"]
    rows = [
        ("Google Scholar", gs.get("citations"), gs.get("h_index"), gs.get("i10_index"), "manual re-check", gs.get("as_of")),
        ("Scopus", sc.get("citations"), sc.get("h_index"), "-", "manual re-check", sc.get("as_of")),
        ("OpenAlex", oa.get("citations"), oa.get("h_index"), "-", "automatic (weekly)", oa.get("as_of")),
    ]
    body = "".join(
        f"<tr><td>{esc(db)}</td><td>{esc(cit)}</td><td>{esc(h)}</td><td>{esc(i10)}</td><td>{esc(how)}</td><td>{esc(asof)}</td></tr>"
        for db, cit, h, i10, how, asof in rows)
    return f"""<div class="mwrap"><table class="metrics">
<tr><th>Database</th><th>Citations</th><th>h-index</th><th>i10-index</th><th>Update</th><th>Figures as of</th></tr>{body}
</table></div>
<p class="small">Each row keeps its own date: it changes only when that database's figures were last successfully checked. OpenAlex refreshes weekly once the included GitHub Actions workflow is deployed; Google Scholar has no public API and Scopus needs an Elsevier API key, so those rows are re-checked manually. Databases index different sources, so counts differ.</p>"""


def publications_html():
    out = []
    asof = pubs.get("scholar_as_of")
    for p in pubs["published"]:
        cit = p.get("scholar_citations")
        cit_line = (f' Cited by {cit} (<a href="https://scholar.google.com/citations?user=Wxlva7YAAAAJ&hl=en">Google Scholar</a>, {esc(asof)}).'
                    if isinstance(cit, int) and cit and asof else "")
        oa = " (open access)" if p.get("open_access") else ""
        out.append(
            f'<p class="pub"><a href="https://doi.org/{esc(p["doi"])}">{esc(p["title"])}</a><br>'
            f'{esc(p["authors"])}. {esc(p["venue"])}.{oa}{cit_line}</p>')
    return "\n".join(out)


def carousel_html():
    dots = "".join(f'<span class="{"on" if i == 0 else ""}"></span>' for i in range(len(FIGURES)))
    return f"""<div class="carousel">
  <img id="acad-img" src="{FIGURES[0][0]}" alt="{esc(FIGURES[0][1])}">
  <div class="bar">
    <button type="button" onclick="acad_show(acad_i-1)" aria-label="Previous figure">&lsaquo;</button>
    <span class="cap" id="acad-cap">{esc(FIGURES[0][2])}</span>
    <button type="button" onclick="acad_show(acad_i+1)" aria-label="Next figure">&rsaquo;</button>
  </div>
  <div class="dots">{dots}</div>
</div>
<p class="small">{esc(FIGURE_CREDIT)}</p>
<script>{CAROUSEL_JS}</script>"""


index = head("Mahmoud M. Abdelatty - Fayoum University") + f"""
<main>
<h2>About</h2>
<p>I am an instructor in the Chemistry Department, Faculty of Science, Fayoum University, Egypt. My research combines organic synthesis with materials chemistry: heterocyclic compounds and molecular docking, benzoxazine-based polymers for supercapacitors, and MOF-based composites for tumor therapy.</p>

<h2>Selected figures from my research</h2>
{carousel_html()}

<h2 id="metrics">Citation metrics</h2>
{metrics_table()}
<p>Profiles:
<a href="https://scholar.google.com/citations?user=Wxlva7YAAAAJ&hl=en">Google Scholar</a> &middot;
<a href="https://www.scopus.com/authid/detail.uri?authorId=58703124300">Scopus (58703124300)</a> &middot;
<a href="https://orcid.org/0000-0002-8136-8397">ORCID (0000-0002-8136-8397)</a> &middot;
<a href="https://www.webofscience.com/wos/author/record/JBI-7603-2023">Web of Science (JBI-7603-2023)</a> &middot;
<a href="https://www.linkedin.com/in/mahmoud-m-abdelati-2515511b3/">LinkedIn</a></p>

<h2>Education and positions</h2>
<ul>
<li>Instructor, Chemistry Department<br>Faculty of Science, Fayoum University</li>
<li>MSc Organic Chemistry<br>Fayoum University</li>
<li>BSc Chemistry<br>Fayoum University</li>
</ul>

<h2 id="publications">Publications</h2>
{publications_html()}

<h2>Conference presentations</h2>
<ul>
<li>Symposium on Medicinal Chemistry, Chinese Pharmaceutical Association, Xinjiang Medical University, Xinjiang, China. Poster: Synthesis and medicinal chemobiological evaluation of novel pyrazoles as potential antimicrobial agents.</li>
<li>The 19th National Synthetic Organic Chemistry Symposium, Jiangsu Suzhou, China. Poster: Synthesis of novel pyranopyrazoles as potential antibacterial agents.</li>
<li>ICBSEA 2018, Fayoum University, 3-5 Apr 2018. Poster: Formulating new nano fertilizers for enhanced seed germination, plant nutrition, and production in wheat under stress.</li>
</ul>
</main>
<footer>
<p>Contact: <a href="mailto:mma34@fayoum.edu.eg">mma34@fayoum.edu.eg</a> &middot; Chemistry Department, Faculty of Science, Fayoum University, 63514 Fayoum, Egypt.</p>
{COUNTER_SNIPPET}
{VISITS_SNIPPET}
</footer>
</body>
</html>
"""

contact = head("Contact - Mahmoud M. Abdelatty") + f"""
<main>
<h2>Contact &amp; collaboration</h2>
<p>I welcome collaboration on heterocyclic synthesis, benzoxazine-based polymers for energy storage, MOF-based composites for tumor therapy, and molecular docking studies. Write to me through the form below, or directly at <a href="mailto:mma34@fayoum.edu.eg">mma34@fayoum.edu.eg</a>.</p>

<!-- This form posts to Formspree (free plan, 50 submissions/month, 30-day archive).
Submissions arrive in the site owner's email inbox. The _gotcha field is a hidden honeypot: spam bots fill it, humans never see it. -->
<form class="contact" action="https://formspree.io/f/mjywllwd" method="POST">
  <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
  <label for="f-name">Your name</label>
  <input id="f-name" name="name" type="text" required>
  <label for="f-email">Your email</label>
  <input id="f-email" name="email" type="email" required>
  <label for="f-affil">Your affiliation</label>
  <input id="f-affil" name="affiliation" type="text">
  <label for="f-msg">Your project or enquiry</label>
  <textarea id="f-msg" name="message" rows="7" required></textarea>
  <button type="submit">Send</button>
</form>
<p class="small">Messages sent here arrive by email; expect a reply at the address you give.</p>
</main>
<footer>
<p>Chemistry Department, Faculty of Science, Fayoum University, 63514 Fayoum, Egypt.</p>
{COUNTER_SNIPPET}
{VISITS_SNIPPET}
</footer>
</body>
</html>
"""

(ROOT / "index.html").write_text(index)
(ROOT / "contact.html").write_text(contact)
print("Wrote index.html and contact.html")
