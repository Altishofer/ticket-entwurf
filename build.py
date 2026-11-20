"""Build design variants of the boarding pass from ../boarding-pass.html.

Outputs (in this folder):
  boarding-pass-<key>.html  print file per variant (2 A4 pages)
  index.html                gallery page with all variants
Run: python3 build.py   (then render PDFs with chromium --print-to-pdf)
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
base = (HERE.parent / "boarding-pass.html").read_text()

style = re.search(r"<style>(.*?)</style>", base, re.S).group(1)
front = re.search(r'(  <div class="pass front">.*?\n  </div>\n)</div>', base, re.S).group(1)
back = re.search(r'(  <div class="pass back">.*?\n  </div>\n)</div>', base, re.S).group(1)


def tokenize(markup):
    # hard-coded colours -> classes so variants can recolour them
    markup = markup.replace('fill="#e9a23b"', 'class="ic"')
    markup = markup.replace('stroke="#2c5f6b"', 'class="track"')
    markup = markup.replace('<svg id="bc"', '<svg class="bc"')
    return markup


front, back = tokenize(front), tokenize(back)

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800"
         "&family=Instrument+Sans:wght@400;500;600;700"
         "&family=JetBrains+Mono:wght@500;700"
         "&family=IBM+Plex+Mono:wght@400;500;700"
         "&family=Archivo:wght@400;500;700;900"
         "&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700"
         "&family=DM+Sans:wght@400;500;700"
         "&family=Righteous&family=Work+Sans:wght@400;500;600;700"
         "&display=swap")

COMMON = """
.pass{color:var(--ink)}
.band{color:#fff}
.ic{fill:var(--sun)}
.loop .track{stroke:var(--accent-deep)}
.barcode rect{fill:var(--ink)}
"""

VARIANTS = [
    ("1", "Teal", "Die aktuelle Version im Stil der Einladungsseite: Petrol mit Akzent in Sonnengelb.", ""),

    ("2", "Thermodruck", "Wie ein echter Boarding Pass vom Automaten: alles in Schreibmaschinenschrift, schwarz auf Weiss, mit rotem Stempel.", """
.v-2 .pass{--ink:#16181d;--muted:#5b6069;--line:#b7bac0;--paper:#fbfbf8;--accent:#16181d;--accent-soft:#fbfbf8;--accent-deep:#16181d;--sun:#d2232a;--sun-soft:transparent;
  --display:"IBM Plex Mono",ui-monospace,monospace;--body:"IBM Plex Mono",ui-monospace,monospace;--mono:"IBM Plex Mono",ui-monospace,monospace;border-radius:2mm}
.v-2 .band{background:var(--paper);color:var(--ink);height:13mm;border-bottom:.6mm solid var(--ink)}
.v-2 .brand{font-weight:700;font-size:11pt}
.v-2 .brand small{opacity:1;color:var(--muted);font-weight:500}
.v-2 .band .kind b{color:var(--sun);font-weight:700}
.v-2 .lbl{font-weight:500;letter-spacing:.08em;font-size:5.4pt}
.v-2 .val{font-weight:700;font-size:9.5pt}
.v-2 .grid .val{font-size:8.6pt}
.v-2 .sub{font-size:5.6pt}
.v-2 .pax .val{font-size:14pt}
.v-2 .iata{font-weight:700;font-size:23pt;color:var(--ink)}
.v-2 .status{background:none;border:.45mm solid var(--sun);color:var(--sun);border-radius:.8mm;transform:rotate(-5deg);font-weight:700}
.v-2 .grid{border-top-style:dashed}
.v-2 .foot{background:none;border-top:.3mm dashed var(--line);color:var(--ink)}
.v-2 .stub,.v-2 .info{background:var(--paper)}
.v-2 .front .stub,.v-2 .back .stub{border-color:var(--ink)}
.v-2 .info h3{font-weight:700}
"""),

    ("3", "Swiss", "Reduziert und typografisch: grosse Ortskürzel, Schwarz und Weiss mit Signalrot, keine Rundungen.", """
.v-3 .pass{--ink:#111111;--muted:#6b6b6b;--line:#d6d6d6;--paper:#ffffff;--accent:#e30613;--accent-soft:#111111;--accent-deep:#111111;--sun:#e30613;--sun-soft:#e30613;
  --display:"Archivo","Helvetica Neue",Arial,sans-serif;--body:"Archivo","Helvetica Neue",Arial,sans-serif;border-radius:0;outline-color:#cfcfcf}
.v-3 .band{background:var(--paper);color:var(--ink);height:14mm;border-bottom:.4mm solid var(--ink)}
.v-3 .brand{font-weight:900}
.v-3 .brand small{opacity:1;color:var(--muted)}
.v-3 .band .kind b{color:var(--accent);font-weight:900}
.v-3 .stub .band{background:var(--accent);color:#fff;border-bottom-color:var(--accent)}
.v-3 .back .main .band{background:var(--accent);color:#fff;border-bottom-color:var(--accent)}
.v-3 .back .main .band .ic{fill:#fff}
.v-3 .back .main .band small{color:#fff;opacity:.85}
.v-3 .lbl{color:var(--accent);font-weight:700}
.v-3 .val{font-weight:900}
.v-3 .iata{font-size:30pt;font-weight:900;letter-spacing:-.035em;color:var(--ink)}
.v-3 .loop .track{stroke:var(--ink)}
.v-3 .status{background:var(--accent);color:#fff;border:0;border-radius:0}
.v-3 .grid{border-top:.4mm solid var(--ink)}
.v-3 .foot{background:var(--ink);color:#fff}
.v-3 .stub,.v-3 .info{background:var(--paper)}
.v-3 .front .stub,.v-3 .back .stub{border-style:solid;border-width:0 0 0 .3mm;border-color:var(--ink)}
.v-3 .back .stub{border-width:0 .3mm 0 0}
.v-3 .info h3{color:var(--accent)}
"""),

    ("4", "Nachtflug", "Dunkles Nachtblau mit Gold und einer Serifenschrift. Wirkt festlich. Braucht viel Druckfarbe, das Schreibfeld hinten bleibt hell.", """
.v-4 .pass{--ink:#f2ede2;--muted:#9fa9bc;--line:#33435d;--paper:#0f1b2e;--accent:#0a1422;--accent-soft:#0a1422;--accent-deep:#e6c27c;--sun:#e6c27c;--sun-soft:transparent;
  --display:"Fraunces",Georgia,serif;--body:"DM Sans","Segoe UI",system-ui,sans-serif;outline-color:#0f1b2e}
.v-4 .band{background:var(--accent);color:var(--ink);border-bottom:.3mm solid var(--sun)}
.v-4 .brand{font-weight:600}
.v-4 .val{font-weight:600}
.v-4 .iata{font-weight:600;color:var(--sun)}
.v-4 .lbl{color:var(--sun);opacity:.85}
.v-4 .status{color:var(--sun);border-color:var(--sun)}
.v-4 .foot{color:var(--ink)}
.v-4 .stub,.v-4 .info{background:#13233a}
.v-4 .info h3{color:var(--sun)}
.v-4 .back .letter{background:#f6f2ea;--line:#cfc6b4}
"""),

    ("5", "Retro", "Airline-Ticket aus den Siebzigern: Streifen in Rot, Orange und Senfgelb, runde Schrift, warmes Braun.", """
.v-5 .pass{--ink:#2b1d16;--muted:#7a6457;--line:#e0d3c7;--paper:#fffdf9;--accent:#c4421a;--accent-soft:#fbeadf;--accent-deep:#8f2d10;--sun:#f2a922;--sun-soft:#fff1d6;
  --display:"Righteous","Segoe UI",system-ui,sans-serif;--body:"Work Sans","Segoe UI",system-ui,sans-serif;border-radius:7mm}
.v-5 .band{position:relative;padding-bottom:3mm}
.v-5 .band::after{content:"";position:absolute;left:0;right:0;bottom:0;height:3.2mm;background:linear-gradient(#e8742a 0 33%,#f2a922 33% 66%,#6b3a1f 66%)}
.v-5 .brand,.v-5 .val,.v-5 .iata,.v-5 .band .kind b{font-weight:400}
.v-5 .band .kind b{color:#ffd27a}
.v-5 .brand small{color:#fff;opacity:.9;font-family:var(--body);font-weight:600}
.v-5 .iata{color:var(--accent)}
.v-5 .lbl{font-family:var(--body);color:var(--accent-deep)}
.v-5 .status{color:var(--accent-deep);border-color:var(--sun);border-radius:4mm}
.v-5 .stub,.v-5 .info{background:#fff7ee}
.v-5 .info h3{color:var(--accent)}
"""),
]

ALL_VARIANT_CSS = COMMON + "".join(v[3] for v in VARIANTS)

SCRIPT = """<script>
(function(){
  const s = "DR-HUNKELER-HBMAD-2026";
  document.querySelectorAll("svg.bc").forEach(svg => {
    let seed = 0; for (const c of s) seed = (seed * 31 + c.charCodeAt(0)) >>> 0;
    const rnd = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;
    let x = 0, out = "";
    while (x < 200) {
      const w = 0.8 + Math.floor(rnd() * 4) * 0.9;
      out += `<rect x="${x.toFixed(2)}" y="0" width="${w.toFixed(2)}" height="40"/>`;
      x += w + 0.8 + Math.floor(rnd() * 3) * 0.9;
    }
    svg.innerHTML = out;
  });
  document.querySelectorAll(".marks").forEach(el => {
    const xs = [10, 200], ys = [105.5, 191.5]; let html = "";
    for (const x of xs) for (const y of ys) {
      html += `<i class="v" style="left:${x}mm;top:${y < 150 ? y - 8 : y + 2}mm"></i>`;
      html += `<i class="h" style="left:${x < 100 ? x - 5 : x + 1}mm;top:${y}mm;width:4mm"></i>`;
    }
    el.innerHTML = html;
  });
})();
</script>"""


def print_file(key, name):
    return f"""<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Boarding Pass {key} {name}</title>
<link href="{FONTS}" rel="stylesheet">
<style>{style}{ALL_VARIANT_CSS}</style>
</head>
<body class="v-{key}">
<p class="hint">Variante {key} · {name}. A4 beidseitig drucken (über die lange Kante wenden), 100 %, nicht «an Seite anpassen». Entlang der Schnittmarken ausschneiden.</p>
<div class="sheet">
  <div class="sheet-label">Seite 1 · Vorderseite</div>
  <div class="marks"></div>
{front}</div>
<div class="sheet">
  <div class="sheet-label">Seite 2 · Rückseite</div>
  <div class="marks"></div>
{back}</div>
{SCRIPT}
</body>
</html>
"""


GALLERY_CSS = """
/* Layout: one column of variants; each shows front and back of the pass as a physical object */
:root{
  --g-bg:#e7eaef; --g-fg:#141821; --g-muted:#535b6a; --g-card:#f6f7f9; --g-line:#cdd2db; --g-accent:#2c5f6b;
  --g-display:"Bricolage Grotesque","Segoe UI",system-ui,sans-serif; --g-body:"Instrument Sans","Segoe UI",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--g-bg:#14171d;--g-fg:#eceef2;--g-muted:#a3aab7;--g-card:#1c2028;--g-line:#2e3440;--g-accent:#8cc3cf;color-scheme:dark}}
:root[data-theme="dark"]{--g-bg:#14171d;--g-fg:#eceef2;--g-muted:#a3aab7;--g-card:#1c2028;--g-line:#2e3440;--g-accent:#8cc3cf;color-scheme:dark}
html,body{background:var(--g-bg);color:var(--g-fg);font-family:var(--g-body)}
.wrap{max-width:1560px;margin:0 auto;padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px));padding-block:28px 48px}
header.top h1{font:800 clamp(28px,5vw,40px)/1.1 var(--g-display);margin:0 0 8px;text-wrap:balance}
header.top p{margin:0;color:var(--g-muted);font-size:16px;line-height:1.5;max-width:68ch}
nav.jump{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 8px}
nav.jump a{font:600 14px/1 var(--g-body);color:var(--g-fg);text-decoration:none;border:1px solid var(--g-line);border-radius:999px;padding:9px 14px;background:var(--g-card)}
nav.jump a:focus-visible{outline:2px solid var(--g-accent);outline-offset:2px}
.variant{margin-top:28px;padding-top:22px;border-top:1px solid var(--g-line)}
.variant h2{font:800 24px/1.2 var(--g-display);margin:0 0 4px;display:flex;gap:12px;align-items:baseline}
.variant h2 span{font:700 13px/1 var(--g-body);letter-spacing:.12em;color:var(--g-accent)}
.variant p{margin:0 0 16px;color:var(--g-muted);font-size:15px;max-width:68ch}
.variant p.dl{margin:-6px 0 16px}
.dl a{color:var(--g-accent);font-weight:600}
.sides{display:flex;flex-wrap:wrap;gap:18px 24px}
.side{min-width:0}
.side small{display:block;font:600 12px/1 var(--g-body);letter-spacing:.1em;text-transform:uppercase;color:var(--g-muted);margin-bottom:8px}
.frame{position:relative;width:190mm;height:86mm;zoom:.95}
.frame .pass{left:0;top:0;box-shadow:0 6px 22px rgba(0,0,0,.18)}
@media (max-width:1560px){.frame{zoom:.9}}
@media (max-width:800px){.frame{zoom:.62}}
@media (max-width:520px){.frame{zoom:.44}}
"""


def gallery():
    nav = "".join(f'<a href="#v-{k}">Variante {k} · {n}</a>' for k, n, _, _ in VARIANTS)
    blocks = ""
    for k, n, d, _ in VARIANTS:
        blocks += f"""
<section class="variant v-{k}" id="v-{k}">
  <h2><span>VARIANTE {k}</span>{n}</h2>
  <p>{d}</p>
  <p class="dl"><a href="boarding-pass-{k}.pdf">PDF von Variante {k} zum Drucken</a></p>
  <div class="sides">
    <div class="side"><small>Vorderseite</small><div class="frame">
{front}    </div></div>
    <div class="side"><small>Rückseite</small><div class="frame">
{back}    </div></div>
  </div>
</section>"""
    return f"""<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>Boarding Pass Varianten</title>
<link href="{FONTS}" rel="stylesheet">
<style>{style}{ALL_VARIANT_CSS}{GALLERY_CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <h1>Boarding Pass Varianten</h1>
  <p>Fünf Designs mit demselben Inhalt für Benjamins Kunstflug. Welche Nummer gefällt dir am besten? Zum Drucken gibt es für jede Variante ein eigenes PDF mit Vorder- und Rückseite.</p>
  <nav class="jump">{nav}</nav>
</header>
{blocks}
</div>
{SCRIPT}
</body>
</html>
"""


for k, n, _, _ in VARIANTS:
    (HERE / f"boarding-pass-{k}.html").write_text(print_file(k, n))
(HERE / "index.html").write_text(gallery())
print("built", [v[0] for v in VARIANTS])
