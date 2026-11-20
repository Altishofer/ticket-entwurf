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


PLANE = """<svg class="rp" viewBox="0 0 300 90" aria-hidden="true">
<path d="M299 39 C296 34 292 31 286.5 30.5 L284 30 C276 26.5 262 25 248 25 L230 25 L128 25.5 C100 27 62 30.5 30 32.6 L14 33.6 L14 36 C40 37.5 80 41.5 120 47 C160 52.5 200 55.5 228 55 C250 54.5 268 51 284 47.6 L286.5 47.4 C292 47 296 44 299 39 Z"/>
<path d="M230.5 25.4 C223 15 207 8.5 186 8.5 C163 8.5 143 14 126 25.4 Z" opacity=".45"/>
<path d="M66 31 L50 6.5 Q48 3.5 44 3.5 L24 3.5 Q19.5 3.5 19 8 L16.5 35 L30 32.6 Z"/>
<path d="M5 34.2 C18 32.2 40 31.9 64 33.2 L64 35.4 C40 36.8 18 37.2 5 36.4 Z"/>
<path d="M150 52 C175 48.5 210 48 242 50 C245 51.6 245 54.6 242 56 C210 58.4 175 57.5 150 53.6 Z"/>
<path d="M231 55 L235.5 54.6 L251.5 77.5 L247.5 78.5 Z"/>
<path d="M237 80.3 C239 75.2 248 74 257.5 74.5 C265.5 75 270.5 77.6 270.5 80.3 C270.5 83.2 264.5 85.4 256 85.4 C246.5 85.4 237 84.2 237 80.3 Z"/>
<path d="M22 35.5 L25 35.4 L29.5 43 L26.6 43.5 Z"/><circle cx="28.4" cy="44.6" r="2.1"/>
<path d="M290.5 5 C291.9 5 292.5 7 292.5 9 L292.5 69 C292.5 71 291.9 73 290.5 73 C289.1 73 288.5 71 288.5 69 L288.5 9 C288.5 7 289.1 5 290.5 5 Z"/>
</svg>
"""

CHECKIN_URL = "https://altishofer.github.io/ticket-entwurf/checkin/"
RICKROLL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def qr_svg(data):
    import segno  # pip install segno
    q = segno.make(data, error="m")
    d = "".join(f"M{x} {y}h1v1h-1z" for y, row in enumerate(q.matrix) for x, v in enumerate(row) if v)
    n = len(q.matrix)
    return f'<svg viewBox="0 0 {n} {n}" shape-rendering="crispEdges" aria-hidden="true"><path d="{d}"/></svg>'


QR_BOX = f"""<img class="sp" src="hb-mad.png" alt=""><div class="qrbox"><div class="qr">{qr_svg(CHECKIN_URL)}</div><div class="qrtxt"><b>Online Check-in</b><span>Code scannen und Sitzplatz bestätigen</span></div></div>"""

def tokenize(markup):
    # hard-coded colours -> classes so variants can recolour them
    markup = markup.replace('fill="#e9a23b"', 'class="ic"')
    markup = markup.replace('stroke="#2c5f6b"', 'class="track"')
    markup = markup.replace('<svg id="bc"', '<svg class="bc"')
    markup = markup.replace('</svg>\n          <div class="to">', '</svg>\n' + PLANE + '          <svg class="phf" viewBox="0 0 100 30" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><path class="trail" d="M3 25 C14 25 19 25 23 21 C27 17 27 12 23 12 C19 12 19 17 23 21 C27 25 50 27 72 26.5 C86 26 95 25 89.5 22"/><image href="hb-mad.png" x="50" y="0" width="42.5" height="29.2"/></svg>\n          <div class="to">', 1)
    markup = re.sub(r'<div class="barcode">.*?</div></div>', QR_BOX, markup, count=1)
    return markup


front, back = tokenize(front), tokenize(back)
SIG = ('<svg class="sig" viewBox="0 0 160 40" aria-hidden="true">'
       '<path class="track" d="M4 32 C40 32 62 32 74 24 C88 14 92 2 80 2 C68 2 70 16 82 24 C96 33 120 32 146 32" fill="none" stroke-width="1.4" stroke-dasharray="3 2.4" stroke-linecap="round"/>'
       '<g transform="translate(150 32) rotate(90)"><path class="ic" d="M0 -6 L1.6 -1.5 L6 1.5 L6 3 L1.6 1.8 L1.2 5 L2.6 6.2 L2.6 7.2 L0 6.4 L-2.6 7.2 L-2.6 6.2 L-1.2 5 L-1.6 1.8 L-6 3 L-6 1.5 L-1.6 -1.5 Z"/></g></svg>')
back = back.replace('<div class="letter">', '<div class="letter">' + SIG, 1)

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800"
         "&family=Instrument+Sans:wght@400;500;600;700"
         "&family=JetBrains+Mono:wght@500;700"
         "&family=IBM+Plex+Mono:wght@400;500;700"
         "&family=Archivo:wght@400;500;700;900"
         "&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700"
         "&family=DM+Sans:wght@400;500;700"
         "&family=Barlow+Condensed:ital,wght@1,800&family=Barlow:wght@500;600&family=Space+Grotesk:wght@500;700&family=Unbounded:wght@700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400;1,8..60,600"
         "&display=swap")

COMMON = """
.letter{position:relative}
.sig{display:none;position:absolute;right:7mm;bottom:5mm;width:44mm;height:11mm;opacity:.35}
.sig .track{stroke:var(--accent-deep)}
.write span{border-bottom:0}
.body{position:relative}
.rp{display:none;height:13mm;width:auto;max-width:100%;margin:0 auto;fill:var(--accent-deep)}
.sp{display:none;width:100%;height:24mm;object-fit:contain;margin:auto 0 1mm;filter:drop-shadow(0 .5mm .8mm rgba(0,0,0,.2))}
.phf{display:none;width:100%;height:26mm;overflow:visible;margin:-1.5mm 0 -1mm}
.phf .trail{fill:none;stroke:var(--accent-deep);stroke-width:.5;stroke-dasharray:1.4 1.1;stroke-linecap:round}
.phf image{filter:drop-shadow(0 .6px .8px rgba(0,0,0,.25))}
.qrbox{margin-top:auto;display:grid;grid-template-columns:17mm 1fr;gap:2.4mm;align-items:center}
.qr{background:#fff;border-radius:1.2mm;padding:1.6mm;line-height:0;box-shadow:0 0 0 .2mm rgba(0,0,0,.12)}
.qr svg{display:block;width:100%;height:auto;fill:#0f1420}
.qrtxt b{display:block;font:700 7.4pt/1.2 var(--display);color:var(--ink)}
.qrtxt span{display:block;font:500 5.8pt/1.3 var(--body);color:var(--muted);margin-top:.8mm}
.pass{color:var(--ink)}
.band{color:#fff}
.ic{fill:var(--sun)}
.loop .track{stroke:var(--accent-deep)}
.barcode rect{fill:var(--ink)}
"""

VARIANTS = [
    ("1", "Teal", ""),

    ("2", "Thermodruck", """
.v-2 .pass{--ink:#16181d;--muted:#5b6069;--line:#b7bac0;--paper:#fbfbf8;--accent:#16181d;--accent-soft:#fbfbf8;--accent-deep:#16181d;--sun:#2346a0;--sun-soft:transparent;
  --display:"IBM Plex Mono",ui-monospace,monospace;--body:"IBM Plex Mono",ui-monospace,monospace;--mono:"IBM Plex Mono",ui-monospace,monospace;border-radius:2mm}
.v-2 .band{background:var(--paper);color:var(--ink);height:13mm;border-bottom:.6mm solid var(--ink)}
.v-2 .brand{font-weight:700;font-size:11pt}
.v-2 .brand small{opacity:1;color:var(--muted);font-weight:500}
.v-2 .band .kind b{color:var(--ink);font-weight:700}
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

    ("3", "Swiss", """
.v-3 .pass{--ink:#111111;--muted:#6b6b6b;--line:#d6d6d6;--paper:#ffffff;--accent:#1f3bd6;--accent-soft:#111111;--accent-deep:#111111;--sun:#1f3bd6;--sun-soft:#1f3bd6;
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
.v-3 .front .stub{border-style:solid;border-width:0 0 0 .3mm;border-color:var(--ink)}
.v-3 .back .stub{border-style:solid;border-width:0 .3mm 0 0;border-color:var(--ink)}
.v-3 .info h3{color:var(--accent)}
"""),

    ("4", "Nachtflug", """
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

    ("5", "Cockpit", """
.v-5 .pass{--ink:#e4eef2;--muted:#7d929f;--line:#26363f;--paper:#10171c;--accent:#0a0f13;--accent-soft:#0a0f13;--accent-deep:#6fe3ff;--sun:#6fe3ff;--sun-soft:transparent;
  --display:"JetBrains Mono",ui-monospace,monospace;--body:"Instrument Sans","Segoe UI",system-ui,sans-serif;outline-color:#10171c}
.v-5 .band{background:var(--accent);color:var(--ink);border-bottom:.3mm solid var(--sun)}
.v-5 .body{background-image:linear-gradient(rgba(111,227,255,.07) .2mm,transparent .2mm),linear-gradient(90deg,rgba(111,227,255,.07) .2mm,transparent .2mm);background-size:5mm 5mm}
.v-5 .val{font-weight:700}
.v-5 .iata{font-weight:700;color:var(--sun);font-size:23pt}
.v-5 .lbl{color:var(--sun);opacity:.8}
.v-5 .status{color:var(--sun);border-color:var(--sun);background:transparent;border-radius:0}
.v-5 .foot{color:var(--ink)}
.v-5 .stub,.v-5 .info{background:#0d1317}
.v-5 .info h3{color:var(--sun)}
.v-5 .back .letter{background:#eef3f5;--line:#b9c6cd}
"""),

    ("6", "Lackierung", """
.v-6 .pass{--ink:#14213d;--muted:#5a6680;--line:#d3d9e6;--paper:#ffffff;--accent:#14213d;--accent-soft:#14213d;--accent-deep:#14213d;--sun:#4cc9f0;--sun-soft:#eaf8fd;
  --display:"Barlow Condensed","Arial Narrow",sans-serif;--body:"Barlow","Segoe UI",system-ui,sans-serif}
.v-6 .band{background:linear-gradient(115deg,#14213d 0 56%,#4cc9f0 56% 59.5%,#14213d 59.5% 61.5%,#2f6fe4 61.5% 67%,#14213d 67%)}
.v-6 .stub .band,.v-6 .back .main .band{background:linear-gradient(115deg,#14213d 0 70%,#4cc9f0 70% 76%,#14213d 76% 79%,#2f6fe4 79% 88%,#14213d 88%)}
.v-6 .brand,.v-6 .val,.v-6 .iata,.v-6 .band .kind b{font-style:italic;font-weight:800}
.v-6 .iata{font-size:31pt;letter-spacing:0;color:var(--ink)}
.v-6 .val{font-size:11.5pt}
.v-6 .grid .val{font-size:10.5pt}
.v-6 .pax .val{font-size:17pt}
.v-6 .lbl{font-family:var(--body);font-weight:600}
.v-6 .status{color:var(--ink);border-color:var(--sun);background:var(--sun-soft);font-family:var(--body)}
.v-6 .foot{color:#fff}
.v-6 .stub,.v-6 .info{background:#f6f8fc}
.v-6 .rp,.v-7 .rp{display:block}
.v-6 .loop,.v-7 .loop{display:none}
.v-7 .rp{fill:#ffffff}
"""),

    ("7", "Blaupause", """
.v-7 .pass{--ink:#f4f8ff;--muted:#bccdec;--line:rgba(255,255,255,.35);--paper:#1d4f9c;--accent:#1d4f9c;--accent-soft:transparent;--accent-deep:#ffffff;--sun:#ffffff;--sun-soft:transparent;
  --display:"Space Grotesk","Segoe UI",system-ui,sans-serif;--body:"Space Grotesk","Segoe UI",system-ui,sans-serif;
  background-image:linear-gradient(rgba(255,255,255,.09) .2mm,transparent .2mm),linear-gradient(90deg,rgba(255,255,255,.09) .2mm,transparent .2mm);background-size:4mm 4mm;outline-color:#1d4f9c}
.v-7 .band{background:transparent;border-bottom:.3mm solid var(--line)}
.v-7 .stub,.v-7 .info{background:transparent}
.v-7 .front .stub,.v-7 .back .stub{border-color:var(--line)}
.v-7 .lbl{font-family:var(--mono);letter-spacing:.06em;font-weight:500}
.v-7 .iata{font-weight:700;color:#fff}
.v-7 .val{font-weight:700}
.v-7 .status{border:.3mm dashed #fff;background:transparent;color:#fff;border-radius:0}
.v-7 .foot{background:transparent;border-top:.3mm solid var(--line);color:#fff}
.v-7 .back .letter{background:#f4f8ff;--line:#b8c6de}
"""),

    ("8", "Himmel", """
.v-8 .pass{--ink:#0d2238;--muted:#577089;--line:#cfe0ee;--paper:#ffffff;--accent:#2a7fc9;--accent-soft:#eef6fc;--accent-deep:#0f3d6e;--sun:#2a7fc9;--sun-soft:#eef6fc;
  --display:"Space Grotesk","Segoe UI",system-ui,sans-serif;--body:"Instrument Sans","Segoe UI",system-ui,sans-serif}
.v-8 .band{background:linear-gradient(100deg,#0f3d6e 0%,#2a7fc9 55%,#8fc8f0 100%)}
.v-8 .stub .band{background:linear-gradient(100deg,#2a7fc9,#8fc8f0)}
.v-8 .band .ic{fill:#fff}
.v-8 .band .kind b{color:#fff}
.v-8 .body{background:linear-gradient(#eef6fc,#ffffff 45%)}
.v-8 .iata,.v-8 .val{font-weight:700}
.v-8 .iata{color:#0f3d6e}
.v-8 .status{color:#0f3d6e;border-color:#8fc8f0;background:#ffffff}
.v-8 .stub,.v-8 .info{background:#f7fbfe}
"""),
    ("9", "Wertpapier", """
.v-9 .pass{--ink:#173a2e;--muted:#4f6b5f;--line:#b9cbbf;--paper:#f2f5ee;--accent:#1f4d3c;--accent-soft:#e2ebe0;--accent-deep:#173a2e;--sun:#b8933f;--sun-soft:#f3ecd8;
  --display:"Fraunces",Georgia,serif;--body:"DM Sans","Segoe UI",system-ui,sans-serif;
  background-image:repeating-radial-gradient(circle at 12% 135%,transparent 0 1.3mm,rgba(31,77,60,.075) 1.3mm 1.5mm),repeating-radial-gradient(circle at 95% -40%,transparent 0 1.7mm,rgba(31,77,60,.06) 1.7mm 1.9mm)}
.v-9 .band{background:repeating-linear-gradient(45deg,rgba(255,255,255,.07) 0 .35mm,transparent .35mm 1.1mm),repeating-linear-gradient(-45deg,rgba(255,255,255,.05) 0 .35mm,transparent .35mm 1.1mm),#1f4d3c}
.v-9 .brand,.v-9 .val,.v-9 .iata,.v-9 .band .kind b{font-weight:600}
.v-9 .band .kind b{color:#e3c47c}
.v-9 .iata{letter-spacing:.04em}
.v-9 .lbl{letter-spacing:.2em}
.v-9 .status{border-radius:5mm;border-color:var(--sun);color:#7a5d1d;background:var(--sun-soft)}
.v-9 .foot{background:transparent;border-top:.25mm solid var(--line)}
.v-9 .stub,.v-9 .info{background:transparent}
"""),

    ("10", "Abflugtafel", """
.v-10 .pass{--ink:#f3f3ee;--muted:#8e9197;--line:#2c2e33;--paper:#17181b;--accent:#0d0e10;--accent-soft:#0d0e10;--accent-deep:#ffd60a;--sun:#ffd60a;--sun-soft:transparent;
  --display:"JetBrains Mono",ui-monospace,monospace;--body:"Instrument Sans","Segoe UI",system-ui,sans-serif;outline-color:#17181b}
.v-10 .band{background:var(--accent);color:var(--ink);border-bottom:.3mm solid #2c2e33}
.v-10 .band .kind b{color:var(--sun)}
.v-10 .iata,.v-10 .stub .pair .val{font-family:"JetBrains Mono",monospace;font-weight:700;color:var(--sun);letter-spacing:.18em;display:inline-block;padding:.06em 0 .06em .05em;
  background:linear-gradient(transparent calc(50% - .5px),rgba(0,0,0,.9) calc(50% - .5px) calc(50% + .5px),transparent calc(50% + .5px)),repeating-linear-gradient(90deg,#2a2c31 0 .7em,transparent .7em .78em)}
.v-10 .iata{font-size:22pt}
.v-10 .route .to .iata{margin-right:-.18em}
.v-10 .val{font-weight:700}
.v-10 .lbl{color:var(--sun);opacity:.75}
.v-10 .status{color:var(--sun);border-color:var(--sun);background:transparent;border-radius:.6mm}
.v-10 .foot{color:var(--ink);border-top:.3mm solid #2c2e33}
.v-10 .stub,.v-10 .info{background:#121315}
.v-10 .info h3{color:var(--sun)}
.v-10 .back .letter{background:#f4f4ef;--line:#c9c9c2}
"""),

    ("11", "Holo", """
.v-11 .pass{--ink:#1b1830;--muted:#625d7a;--line:#ddd8ec;--paper:#ffffff;--accent:#2b2350;--accent-soft:#f4f1fb;--accent-deep:#2b2350;--sun:#2b2350;--sun-soft:transparent;
  --display:"Instrument Sans","Segoe UI",system-ui,sans-serif;--body:"Instrument Sans","Segoe UI",system-ui,sans-serif}
.v-11 .band,.v-11 .foot{background:linear-gradient(110deg,#c4efff 0%,#e5d2ff 30%,#ffd4ea 55%,#d6fff0 80%,#c4dcff 100%);color:#1b1830}
.v-11 .band .ic{fill:#1b1830}
.v-11 .brand,.v-11 .band .kind b,.v-11 .iata{font-family:"Unbounded","Segoe UI",system-ui,sans-serif;font-weight:700}
.v-11 .brand{font-size:10pt}
.v-11 .brand small{opacity:.7}
.v-11 .band .kind b{color:#1b1830;font-size:11.5pt}
.v-11 .iata{font-size:23pt;background:linear-gradient(110deg,#4f86ff,#a965ff 50%,#ff62ad);-webkit-background-clip:text;background-clip:text;color:transparent}
.v-11 .status{background:linear-gradient(110deg,#c4efff,#ffd4ea);border:0;color:#1b1830}
.v-11 .stub,.v-11 .info{background:#fbfaff}
"""),

    ("12", "Riso", """
.v-12 .pass{--ink:#0b4f9c;--muted:#4a78b0;--line:#ffb6dc;--paper:#fbfaf7;--accent:#ff4fae;--accent-soft:#ffe4f2;--accent-deep:#0b4f9c;--sun:#0b4f9c;--sun-soft:transparent;
  --display:"Space Grotesk","Segoe UI",system-ui,sans-serif;--body:"Space Grotesk","Segoe UI",system-ui,sans-serif;
  background-image:radial-gradient(rgba(11,79,156,.07) .14mm,transparent .16mm);background-size:.7mm .7mm}
.v-12 .band{color:#0b3a7a}
.v-12 .band .kind b{color:#0b3a7a}
.v-12 .brand small{opacity:.85}
.v-12 .iata{font-weight:700;color:#0b4f9c;text-shadow:.5mm .35mm 0 rgba(255,79,174,.85)}
.v-12 .pax .val{text-shadow:.35mm .25mm 0 rgba(255,79,174,.7)}
.v-12 .val{font-weight:700}
.v-12 .lbl{color:#ff3fa4}
.v-12 .loop .track{stroke:#ff3fa4}
.v-12 .status{background:#ff4fae;color:#fff;border:0;border-radius:0}
.v-12 .foot{color:#0b4f9c}
.v-12 .stub,.v-12 .info{background:transparent}
"""),

    ("13", "Paper", """
.v-13 .pass{--ink:#141414;--muted:#555555;--line:#cfcfcf;--paper:#ffffff;--accent:#ffffff;--accent-soft:#ffffff;--accent-deep:#141414;--sun:#141414;--sun-soft:transparent;
  --display:"Source Serif 4",Georgia,serif;--body:"Source Serif 4",Georgia,serif;border-radius:0;outline-color:#bdbdbd}
.v-13 .band{background:#fff;color:#141414;border-bottom:.25mm solid #141414}
.v-13 .band .kind b{color:#141414}
.v-13 .brand,.v-13 .val,.v-13 .iata,.v-13 .band .kind b{font-weight:600}
.v-13 .brand small{opacity:1;color:#555}
.v-13 .lbl{text-transform:lowercase;font-variant:small-caps;letter-spacing:.08em;font-size:7.4pt;font-weight:600;line-height:.8}
.v-13 .sub,.v-13 .foot{font-style:italic}
.v-13 .iata{font-style:italic;font-size:26pt}
.v-13 .pax .val::after{content:"1";font-size:.5em;vertical-align:super;margin-left:.3mm}
.v-13 .foot span:first-child::before{content:"1 ";font-size:.75em;vertical-align:super}
.v-13 .status{border:.25mm solid #141414;color:#141414;background:#fff;border-radius:0;text-transform:none;letter-spacing:.02em;font-family:var(--body);font-style:italic}
.v-13 .foot{background:#fff;border-top:.25mm solid #141414;color:#141414}
.v-13 .grid{border-top-color:#141414}
.v-13 .stub,.v-13 .info{background:#fff}
.v-13 .front .stub{border-left:.25mm solid #141414}
.v-13 .back .stub{border-right:.25mm solid #141414}
"""),
    ("14", "Livery", """
.v-14 .pass{--ink:#16204f;--muted:#5b6488;--line:#d5d9e6;--paper:#ffffff;--accent:#1b2a78;--accent-soft:#eef0f7;--accent-deep:#1b2a78;--sun:#c9ced8;--sun-soft:#eef0f7;
  --display:"Space Grotesk","Segoe UI",system-ui,sans-serif;--body:"Instrument Sans","Segoe UI",system-ui,sans-serif}
.v-14 .band{background:linear-gradient(to top,#1b2a78 0 1.1mm,#ffffff 1.1mm 1.5mm,#1b2a78 1.5mm 2.1mm,#c9ced8 2.1mm 2.5mm,transparent 2.5mm),#1b2a78}
.v-14 .stub .band .brand{flex-direction:column;align-items:flex-start;gap:0;font-size:12pt}
.v-14 .stub .band .brand::before{content:"Boarding Pass";font:700 6.5pt/1.2 var(--body);letter-spacing:.16em;text-transform:uppercase;opacity:.85;margin-bottom:.6mm}
.v-14 .band .kind b{color:#fff}
.v-14 .ic{fill:#c9ced8}
.v-14 .iata,.v-14 .val{font-weight:700}
.v-14 .iata{color:#1b2a78}
.v-14 .loop .track{stroke:#1b2a78}
.v-14 .route .ic{fill:#1b2a78}
.v-14 .status{color:#1b2a78;border-color:#1b2a78;background:#fff}
.v-14 .foot{background:#1b2a78;color:#fff}
.v-14 .stub,.v-14 .info{background:#f6f7fb}
.v-14 .route{margin:3.6mm 0 2.6mm}
.v-14 .grid{row-gap:3.4mm;padding-top:3mm}
"""),
    ("15", "HB-MAD", """
.v-15 .pass{--ink:#1c1418;--muted:#6d5f63;--line:#ddd3cc;--paper:#f4f0ea;--accent:#17121a;--accent-soft:#17121a;--accent-deep:#7d2033;--sun:#7d2033;--sun-soft:transparent;
  --display:"Archivo","Helvetica Neue",Arial,sans-serif;--body:"Instrument Sans","Segoe UI",system-ui,sans-serif}
.v-15 .band{background:linear-gradient(118deg,#17121a 0 57%,#7d2033 57% 65%,#efe9df 65% 66.6%,#17121a 66.6% 75%,#7d2033 75% 79%,#17121a 79%)}
.v-15 .stub .band,.v-15 .back .main .band{background:linear-gradient(118deg,#17121a 0 62%,#7d2033 62% 74%,#efe9df 74% 76%,#17121a 76%)}
.v-15 .band .kind b{color:#efe9df}
.v-15 .ic{fill:#efe9df}
.v-15 .brand,.v-15 .val,.v-15 .iata,.v-15 .band .kind b{font-weight:900}
.v-15 .iata{color:#17121a;font-size:27pt;letter-spacing:-.02em}
.v-15 .lbl{color:#7d2033}
.v-15 .status{color:#7d2033;border-color:#7d2033;background:transparent}
.v-15 .foot{color:#efe9df}
.v-15 .stub,.v-15 .info{background:#efe9df}
"""),

    ("16", "HB-MAD Nacht", """
.v-16 .pass{--ink:#efe9df;--muted:#a8999d;--line:#3a2d33;--paper:#17121a;--accent:#7d2033;--accent-soft:#100c12;--accent-deep:#efe9df;--sun:#efe9df;--sun-soft:transparent;
  --display:"Archivo","Helvetica Neue",Arial,sans-serif;--body:"Instrument Sans","Segoe UI",system-ui,sans-serif;outline-color:#17121a}
.v-16 .band{background:linear-gradient(118deg,#7d2033 0 70%,#efe9df 70% 71.8%,#17121a 71.8% 80%,#7d2033 80% 84%,#17121a 84%)}
.v-16 .stub .band,.v-16 .back .main .band{background:#7d2033}
.v-16 .band .kind b{color:#efe9df}
.v-16 .brand,.v-16 .val,.v-16 .iata,.v-16 .band .kind b{font-weight:900}
.v-16 .iata{font-size:27pt;letter-spacing:-.02em}
.v-16 .lbl{color:#c9566e}
.v-16 .status{color:#efe9df;border-color:#7d2033;background:#7d2033}
.v-16 .foot{color:#efe9df;border-top:.3mm solid #3a2d33}
.v-16 .stub,.v-16 .info{background:#120e14}
.v-16 .info h3{color:#c9566e}
.v-16 .back .letter{background:#f4f0ea;--line:#d6ccc4}
"""),

    ("17", "Teal Foto", ""),
]

# Vergleich: Variante 14 im Original, nur mit Zierlinien, und ganz verfeinert
_css14 = next(c for k, n, c in VARIANTS if k == "14")
_new_band = [l for l in _css14.splitlines() if l.startswith(".v-14 .band{")][0]
_old_band = ".v-14 .band{position:relative;padding-bottom:3mm;background:linear-gradient(transparent 0 79%,#ffffff 79% 84%,#c9ced8 84%),#1b2a78}"
_extras = (".v-14 .stub .band .brand", ".v-14 .route{", ".v-14 .grid{")
_base14 = "\n".join(l for l in _css14.splitlines() if not l.startswith(_extras))
VARIANTS += [
    ("14o", "Original", _base14.replace(_new_band, _old_band).replace(".v-14 ", ".v-14o ")),
    ("14p", "Nur Zierlinien", _base14.replace(".v-14 ", ".v-14p ")),
]
VARIANTS += [("14r", "Neue Rückseite", _css14.replace(".v-14 ", ".v-14r ") + """
.v-14r .sig{display:block}
.v-14r .sig .ic{fill:#1b2a78}
.v-14r .info{padding:4.5mm 4.5mm 4mm;gap:2.4mm}
.v-14r .info h3{font-size:8.8pt}
.v-14r .info ol,.v-14r .info ul{font-size:6.9pt;line-height:1.4;padding-left:4mm}
.v-14r .info li{margin-bottom:.6mm}
.v-14r .info .safety{padding-top:2.2mm}
.v-14r .info > .sub{font-size:6.6pt}
""")]
OLD_SUBS = {"14o": True, "14p": True}
SUBS_NEW_TO_OLD = {
    '<div class="sub">vorher Doktorand</div>': '<div class="sub">Upgrade von Doktorand</div>',
    '<div class="sub">Wochenende frei</div>': '<div class="sub">Wochenende nach Wahl</div>',
    '<div class="sub">Selbst am Steuer</div>': '<div class="sub">Selber steuern möglich</div>',
    '<div class="sub">Volles Programm</div>': '<div class="sub">Volles Kunstflugprogramm</div>',
    '<div class="sub">Aus dem Cockpit</div>': '<div class="sub">Aufnahme aus dem Cockpit</div>',
}


def front_for(k):
    m = front
    if k in OLD_SUBS:
        for new, old in SUBS_NEW_TO_OLD.items():
            m = m.replace(new, old)
    return m


LABELS = {"14o": "14 · Original", "14p": "14 · nur Zierlinien", "14": "14 · verfeinert", "14r": "14 · neue Rückseite"}

# Auswahl auf der Abstimmungsseite (nach der ersten Runde, 20.11.2026)
GALLERY = ["14o", "14p", "14", "14r"]

PHOTO = ["15", "16"]
STUBPHOTO = ["4", "9", "11", "14", "14o", "14p", "14r", "17"]
PHOTO_CSS = "".join(f".v-{k} .phf{{display:block}}.v-{k} .loop{{display:none}}.v-{k} .grid > div:is(:nth-child(2),:nth-child(4),:nth-child(5),:nth-child(9),:nth-child(10)){{display:none}}\n" for k in PHOTO)
PHOTO_CSS += "".join(f".v-{k} .sp{{display:block}}.v-{k} .stub .qrbox{{margin-top:0}}.v-{k} .stub .inner > :is(:nth-child(3),:nth-child(4)){{display:none}}\n" for k in STUBPHOTO)
ALL_VARIANT_CSS = COMMON + PHOTO_CSS + "".join(v[2] for v in VARIANTS)

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
    front = front_for(key)
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
/* Layout: one column of variants; each pass scales to its column, tap opens it full screen */
:root{
  --g-bg:#e7eaef; --g-fg:#141821; --g-line:#cdd2db; --g-accent:#2c5f6b; --g-veil:rgba(12,15,20,.92);
  --g-display:"Bricolage Grotesque","Segoe UI",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--g-bg:#14171d;--g-fg:#eceef2;--g-line:#2e3440;--g-accent:#8cc3cf;color-scheme:dark}}
:root[data-theme="dark"]{--g-bg:#14171d;--g-fg:#eceef2;--g-line:#2e3440;--g-accent:#8cc3cf;color-scheme:dark}
html,body{background:var(--g-bg);color:var(--g-fg)}
body{-webkit-tap-highlight-color:transparent}
.wrap{max-width:1560px;margin:0 auto;padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px));padding-block:max(20px, env(safe-area-inset-top, 0px)) max(40px, env(safe-area-inset-bottom, 0px))}
.variant{padding-block:22px 26px;border-top:1px solid var(--g-line)}
.variant:first-child{border-top:0;padding-top:4px}
.variant h2{font:800 clamp(28px,6vw,40px)/1 var(--g-display);margin:0 0 14px;letter-spacing:-.01em}
.sides{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,620px),1fr));gap:12px 22px}
.fit{position:relative;width:100%;height:calc((100vw - 32px) * .4526);cursor:zoom-in;border-radius:10px}
.fit:focus-visible{outline:3px solid var(--g-accent);outline-offset:4px}
.fit .frame{position:absolute;left:0;top:0;width:190mm;height:86mm;transform-origin:0 0}
.frame .pass{left:0;top:0;box-shadow:0 6px 22px rgba(0,0,0,.18)}
#lb{position:fixed;inset:0;z-index:20;background:var(--g-veil);cursor:zoom-out}
#lb .frame{position:absolute;left:50%;top:50%;width:190mm;height:86mm}
@media (prefers-reduced-motion:no-preference){#lb{animation:fade .18s ease-out}@keyframes fade{from{opacity:0}}}
"""

FIT_SCRIPT = """<script>
(function(){
  const fits = [...document.querySelectorAll(".fit")];
  function layout(){
    for (const f of fits) {
      const fr = f.firstElementChild, s = f.clientWidth / fr.offsetWidth;
      fr.style.transform = "scale(" + s + ")";
      f.style.height = (fr.offsetHeight * s) + "px";
    }
  }
  layout();
  addEventListener("resize", layout);
  if (document.fonts) document.fonts.ready.then(layout);

  let lb = null, cur = null;
  function close(){ if (lb) { lb.remove(); lb = null; cur = null; document.body.style.overflow = ""; } }
  function open(f){
    close(); cur = f;
    const fr = f.firstElementChild.cloneNode(true);
    lb = document.createElement("div"); lb.id = "lb"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true");
    lb.className = [...f.closest(".variant").classList].filter(c => c.startsWith("v-")).join(" ");
    lb.appendChild(fr); document.body.appendChild(lb); document.body.style.overflow = "hidden";
    const vw = innerWidth - 24, vh = innerHeight - 24, w = fr.offsetWidth, h = fr.offsetHeight;
    const turn = vh > vw * 1.15;
    const s = turn ? Math.min(vw / h, vh / w) : Math.min(vw / w, vh / h);
    fr.style.transform = "translate(-50%,-50%)" + (turn ? " rotate(90deg)" : "") + " scale(" + s + ")";
    lb.addEventListener("click", close);
  }
  for (const f of fits) {
    f.addEventListener("click", () => open(f));
    f.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(f); } });
  }
  addEventListener("keydown", e => { if (e.key === "Escape") close(); });
  addEventListener("resize", () => { if (cur) open(cur); });
})();
</script>"""


def gallery():
    blocks = ""
    shown = {k: (k, n, c) for k, n, c in VARIANTS}
    for k, n, _ in (shown[x] for x in GALLERY):
        letter = LABELS.get(k, k)
        front = front_for(k)
        blocks += f"""
<section class="variant v-{k}" id="v{k}">
  <h2>{letter}</h2>
  <div class="sides">
    <div class="fit" tabindex="0" role="button" aria-label="{letter} Vorderseite gross anzeigen"><div class="frame">
{front}    </div></div>
    <div class="fit" tabindex="0" role="button" aria-label="{letter} Rückseite gross anzeigen"><div class="frame">
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
<main class="wrap">
{blocks}
</main>
{SCRIPT}
{FIT_SCRIPT}
</body>
</html>
"""


CHECKIN = f"""<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="4;url={RICKROLL}">
<title>Online Check-in · PHD 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Instrument+Sans:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#eef0f4;--card:#ffffff;--ink:#0f1420;--muted:#4a5263;--line:#d5d9e1;--accent:#2c5f6b;--soft:#e6f0f1}}
@media (prefers-color-scheme: dark){{:root{{--bg:#12161c;--card:#1b2029;--ink:#eceef2;--muted:#a3aab7;--line:#2e3440;--accent:#8cc3cf;--soft:#1f2c31;color-scheme:dark}}}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--bg);color:var(--ink);font:16px/1.5 "Instrument Sans","Segoe UI",system-ui,sans-serif;padding:24px max(16px, env(safe-area-inset-left, 0px))}}
.card{{width:100%;max-width:420px;background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden}}
.top{{background:var(--accent);color:#fff;padding:18px 22px;display:flex;justify-content:space-between;align-items:center;font:700 13px/1 "Instrument Sans",sans-serif;letter-spacing:.14em;text-transform:uppercase}}
.top b{{font:800 20px/1 "Bricolage Grotesque",sans-serif;letter-spacing:0}}
.in{{padding:22px}}
.route{{display:flex;justify-content:space-between;align-items:baseline;font:800 34px/1 "Bricolage Grotesque",sans-serif;margin:4px 0 18px}}
.route span{{font:600 24px/1 "Instrument Sans",sans-serif;color:var(--muted)}}
dl{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:0 0 22px}}
dt{{font:700 11px/1 "Instrument Sans",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
dd{{margin:4px 0 0;font-weight:700}}
.bar{{height:8px;border-radius:99px;background:var(--soft);overflow:hidden}}
.bar i{{display:block;height:100%;width:8%;background:var(--accent);border-radius:99px;transition:width 3.2s ease-in-out}}
.st{{margin:12px 0 0;color:var(--muted);font-size:14px}}
</style>
</head>
<body>
<main class="card">
  <div class="top">Online Check-in <b>PHD 2026</b></div>
  <div class="in">
    <div class="route">ETH <span>→</span> LFGB</div>
    <dl>
      <div><dt>Passagier</dt><dd>Dr. Benjamin Hunkeler</dd></div>
      <div><dt>Sitz</dt><dd>1A · Doctor</dd></div>
      <div><dt>Flugzeug</dt><dd>XtremeAir XA42</dd></div>
      <div><dt>Status</dt><dd id="s">Prüfung läuft</dd></div>
    </dl>
    <div class="bar"><i id="b"></i></div>
    <p class="st" id="t">Sitzplatz wird bestätigt …</p>
  </div>
</main>
<script>
requestAnimationFrame(() => requestAnimationFrame(() => document.getElementById("b").style.width = "100%"));
setTimeout(() => {{ document.getElementById("t").textContent = "Bordkarte wird geöffnet …"; document.getElementById("s").textContent = "Bestätigt ✓"; }}, 2200);
setTimeout(() => location.replace("{RICKROLL}"), 3300);
</script>
</body>
</html>
"""
(HERE / "checkin").mkdir(exist_ok=True)
(HERE / "checkin" / "index.html").write_text(CHECKIN)

READY_CSS = """
/* Druckvorlage: Endformat 190 x 86 mm + 3 mm Beschnitt rundherum, eine Seite pro Seite des Passes */
@page{size:196mm 92mm;margin:0}
html,body{margin:0;background:#fff}
.page{width:196mm;height:92mm;position:relative;overflow:hidden;background:#fff;page-break-after:always;break-after:page}
.page .pass{left:3mm;top:3mm;border-radius:0;outline:0;overflow:visible}
.v-14r .front .main .band{box-shadow:0 -3mm 0 #1b2a78,-3mm 0 0 #1b2a78,-3mm -3mm 0 #1b2a78}
.v-14r .front .stub .band{box-shadow:0 -3mm 0 #1b2a78,3mm 0 0 #1b2a78,3mm -3mm 0 #1b2a78}
.v-14r .front .stub{box-shadow:3mm 0 0 #f6f7fb,0 3mm 0 #f6f7fb,3mm 3mm 0 #f6f7fb}
.v-14r .front .foot{box-shadow:-3mm 0 0 #1b2a78,0 3mm 0 #1b2a78,-3mm 3mm 0 #1b2a78}
.v-14r .back .info{box-shadow:-3mm 0 0 #f6f7fb,0 -3mm 0 #f6f7fb,0 3mm 0 #f6f7fb,-3mm -3mm 0 #f6f7fb,-3mm 3mm 0 #f6f7fb}
.v-14r .back .main .band{box-shadow:0 -3mm 0 #1b2a78,3mm 0 0 #1b2a78,3mm -3mm 0 #1b2a78}
"""


def ready_file(key):
    return f"""<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<title>Boarding Pass Druckvorlage</title>
<link href="{FONTS}" rel="stylesheet">
<style>{style}{ALL_VARIANT_CSS}{READY_CSS}</style>
</head>
<body class="v-{key}">
<div class="page">
{front_for(key)}</div>
<div class="page">
{back}</div>
{SCRIPT}
</body>
</html>
"""


TICKET_CSS = """
/* Nur das Ticket: Vorder- und Rückseite untereinander; Druck je Seite 190 x 86 mm */
@page{size:190mm 86mm;margin:0}
html,body{margin:0;background:#e6e9ef}
body{padding-block:8mm;padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px))}
.page{width:190mm;height:86mm;position:relative;margin:0 auto 8mm;border-radius:5mm;overflow:hidden;box-shadow:0 6px 24px rgba(15,20,32,.18)}
.page .pass{left:0;top:0;outline:0}
@media screen and (max-width:780px){.page{zoom:.5}}
@media screen and (max-width:420px){.page{zoom:.46}}
@media print{html,body{background:#fff;padding:0}.page{margin:0;border-radius:0;box-shadow:none;zoom:1;page-break-after:always;break-after:page}}
"""


def ticket_file(key):
    import base64
    img = "data:image/png;base64," + base64.b64encode((HERE / "hb-mad.png").read_bytes()).decode()
    html = f"""<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Boarding Pass PHD 2026</title>
<link href="{FONTS}" rel="stylesheet">
<style>{style}{ALL_VARIANT_CSS}{TICKET_CSS}</style>
</head>
<body class="v-{key}">
<div class="page">
{front_for(key)}</div>
<div class="page">
{back}</div>
{SCRIPT}
</body>
</html>
"""
    return html.replace('src="hb-mad.png"', f'src="{img}"').replace('href="hb-mad.png"', f'href="{img}"')


SHOW_CSS = """
/* Bild zum Teilen: Pässe als Objekte auf ruhigem Grund */
html,body{margin:0;width:100%;height:100%;overflow:hidden}
body{background:radial-gradient(120% 90% at 50% 40%,#f3f5f9 0%,#dfe4ec 70%,#d3d9e3 100%)}
.page{position:absolute;width:190mm;height:86mm;border-radius:5mm;overflow:hidden;transform-origin:50% 50%;
  box-shadow:0 2px 4px rgba(15,25,60,.10),0 18px 40px rgba(15,25,60,.22)}
.page .pass{left:0;top:0;outline:0}
.duo .page.f{left:50%;top:50%;z-index:2;transform:translate(-50%,-104%) rotate(-3deg)}
.duo .page.b{left:50%;top:50%;z-index:1;transform:translate(-50%,6%) rotate(2.2deg)}
.solo .page.f{left:50%;top:50%;transform:translate(-50%,-50%) rotate(-2deg) scale(.96)}
"""


def show_file(key, mode):
    html = ticket_file(key)
    html = html.replace("{TICKET_CSS}", "")
    html = html.replace(TICKET_CSS, SHOW_CSS)
    html = html.replace('<body class="v-' + key + '">', '<body class="v-' + key + ' ' + mode + '">', 1)
    html = html.replace('<div class="page">', '<div class="page f">', 1).replace('<div class="page">', '<div class="page b">', 1)
    if mode == "solo":
        html = re.sub(r'<div class="page b">.*?</div>\n<script>', '<script>', html, count=1, flags=re.S)
    return html


(HERE.parent / "druck").mkdir(exist_ok=True)
(HERE.parent / "druck" / "boarding-pass-ticket.html").write_text(ticket_file("14r"))
(HERE.parent / "druck" / "teilen-beide.html").write_text(show_file("14r", "duo"))

(HERE / "druck").mkdir(exist_ok=True)
(HERE / "druck" / "boarding-pass-druck.html").write_text(ready_file("14r").replace('src="hb-mad.png"', 'src="../hb-mad.png"'))

for k, n, _ in VARIANTS:
    (HERE / f"boarding-pass-{k}.html").write_text(print_file(k, n))
(HERE / "index.html").write_text(gallery())
print("built", [v[0] for v in VARIANTS])
