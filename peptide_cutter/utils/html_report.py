from __future__ import annotations

from html import escape
from typing import Dict, List


_PROLINE_NOTE_URL = "https://pubmed.ncbi.nlm.nih.gov/9695945/"

_CSS_COMMON = """
:root {
  --ink: #1b1f24;
  --muted: #5b6069;
  --accent: #e07a2f;
  --accent-2: #1f6d64;
  --accent-3: #2b3a50;
  --bg: #f2efe8;
  --panel: #fbf8f2;
  --border: #e3d9cc;
  --shadow: 0 18px 45px rgba(25, 24, 20, 0.12);
  --serif: "Baskerville", "Palatino", "Times New Roman", serif;
  --sans: "Futura", "Gill Sans", "Optima", "Trebuchet MS", sans-serif;
  --mono: "IBM Plex Mono", "SF Mono", "Menlo", "Consolas", monospace;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: var(--serif);
  color: var(--ink);
  background: var(--bg);
  line-height: 1.6;
}

body::before {
  content: "";
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(circle at 15% 15%, rgba(224, 122, 47, 0.08), transparent 45%),
    radial-gradient(circle at 85% 10%, rgba(31, 109, 100, 0.12), transparent 50%),
    linear-gradient(140deg, rgba(255, 255, 255, 0.72), rgba(255, 255, 255, 0.84)),
    repeating-linear-gradient(
      0deg,
      rgba(0, 0, 0, 0.04),
      rgba(0, 0, 0, 0.04) 1px,
      transparent 1px,
      transparent 28px
    );
  z-index: -2;
}

body::after {
  content: "";
  position: fixed;
  inset: 0;
  background-image: repeating-linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.03),
    rgba(0, 0, 0, 0.03) 1px,
    transparent 1px,
    transparent 60px
  );
  opacity: 0.6;
  z-index: -1;
  pointer-events: none;
}

.report {
  max-width: 1140px;
  margin: 0 auto;
  padding: 44px 24px 90px;
  position: relative;
}

.report::before {
  content: "";
  position: absolute;
  top: 28px;
  bottom: 28px;
  left: 16px;
  width: 4px;
  border-radius: 999px;
  background: linear-gradient(180deg, rgba(224, 122, 47, 0.8), rgba(31, 109, 100, 0.7));
  opacity: 0.8;
}

.skip-link {
  position: absolute;
  left: -999px;
  top: 12px;
  background: #fff;
  color: var(--ink);
  padding: 8px 14px;
  border-radius: 999px;
  border: 2px solid var(--accent);
  font-family: var(--sans);
  text-decoration: none;
  z-index: 10;
}

.skip-link:focus {
  left: 16px;
}

:focus-visible {
  outline: 3px solid var(--accent);
  outline-offset: 2px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
"""

_CSS_SINGLE = """
.back-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid rgba(31, 109, 100, 0.35);
  background: rgba(31, 109, 100, 0.08);
  color: var(--accent-3);
  text-decoration: none;
  font-family: var(--sans);
  font-size: 0.85rem;
  font-weight: 600;
}

.back-link:hover {
  border-color: var(--accent-2);
  color: var(--accent-2);
}

.hero {
  padding: 30px 36px 26px;
  border-radius: 22px;
  background: var(--panel);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
}

.hero::after {
  content: "";
  position: absolute;
  top: -60px;
  left: -60px;
  width: 160px;
  height: 160px;
  border-radius: 32px;
  background: linear-gradient(135deg, rgba(31, 109, 100, 0.16), transparent);
  transform: rotate(12deg);
}

.hero-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  font-family: var(--sans);
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.72rem;
  color: var(--accent-2);
}

.hero-badge {
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px dashed rgba(31, 109, 100, 0.45);
  background: rgba(31, 109, 100, 0.08);
}

h1 {
  font-family: var(--sans);
  font-size: 2.5rem;
  margin: 12px 0 10px;
  letter-spacing: 0.02em;
  color: var(--accent-3);
}

.subtitle {
  color: var(--muted);
  margin: 0 0 18px;
  font-size: 1.02rem;
}

.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.8fr) minmax(0, 1fr);
  gap: 22px;
  align-items: start;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
  margin-top: 10px;
}

.meta-card {
  border-radius: 14px;
  padding: 12px 14px;
  background: #fffdf9;
  border: 1px solid rgba(0, 0, 0, 0.06);
  font-family: var(--sans);
  font-size: 0.85rem;
  color: var(--muted);
}

.meta-card strong {
  display: block;
  font-size: 0.95rem;
  color: var(--ink);
  letter-spacing: 0.02em;
}

.hero-panel {
  padding: 16px;
  border-radius: 16px;
  border: 1px solid rgba(224, 122, 47, 0.24);
  background: linear-gradient(160deg, rgba(224, 122, 47, 0.12), rgba(255, 255, 255, 0.85));
  font-family: var(--sans);
  color: var(--ink);
}

.hero-panel p {
  margin: 0 0 12px;
}

.nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.nav a {
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  font-size: 0.82rem;
  text-decoration: none;
  color: var(--accent-3);
  background: rgba(255, 255, 255, 0.8);
}

.nav a:hover {
  border-color: var(--accent);
  color: var(--accent);
}

section {
  margin-top: 30px;
  padding: 26px 28px;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: var(--panel);
  box-shadow: 0 12px 26px rgba(25, 24, 20, 0.08);
  position: relative;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.section-title .tag {
  font-family: var(--sans);
  font-size: 0.72rem;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--accent-2);
  border-bottom: 2px solid var(--accent-2);
  padding-bottom: 4px;
}

.section-title .title {
  font-family: var(--sans);
  font-size: 1.4rem;
  color: var(--accent-3);
  letter-spacing: 0.01em;
}

p {
  margin: 0 0 12px;
  color: var(--muted);
}

.sequence pre,
.tracks pre {
  font-family: var(--mono);
  font-size: 0.9rem;
  line-height: 1.5;
  background: #ffffff;
  color: #1a1a1a;
  padding: 18px 18px;
  border-radius: 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  overflow-x: auto;
}

.tracks pre {
  background: #0f1d1c;
  color: #f5efe6;
  border: 1px solid rgba(31, 109, 100, 0.5);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.04);
}

.enzyme-list {
  columns: 2;
  column-gap: 30px;
  padding-left: 18px;
  margin: 12px 0 0;
  font-family: var(--sans);
  color: var(--ink);
}

.enzyme-list li {
  break-inside: avoid;
  margin-bottom: 6px;
}

.note {
  margin-top: 14px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid rgba(224, 122, 47, 0.35);
  background: rgba(224, 122, 47, 0.12);
  font-family: var(--sans);
  color: var(--accent-3);
}

.note a {
  color: var(--accent-3);
  text-decoration: underline;
  text-decoration-thickness: 2px;
  text-underline-offset: 3px;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 14px;
  font-family: var(--sans);
  font-size: 0.95rem;
  background: #fbfaf7;
  border: 1px solid #d9d6cf;
  border-radius: 12px;
  overflow: hidden;
}

thead {
  background: #dfe7e4;
}

th,
td {
  text-align: left;
  padding: 12px 14px;
  border-bottom: 1px solid #e1ddd7;
}

tbody tr:nth-child(even) {
  background: #f3f0ec;
}

.notice {
  margin-top: 14px;
  padding: 14px 16px;
  border-left: 4px solid #2b6d64;
  background: #dfe7e4;
  border-radius: 8px;
  font-family: var(--sans);
  color: #1f2c35;
}

footer {
  margin-top: 34px;
  font-family: var(--sans);
  font-size: 0.85rem;
  color: var(--muted);
  text-align: center;
}

@media (max-width: 980px) {
  .hero-grid {
    grid-template-columns: 1fr;
  }

  .enzyme-list {
    columns: 1;
  }
}
"""

_CSS_INDEX = """
.hero-grid {
  grid-template-columns: 1fr;
  margin-top: 26px;
}

.title-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-top: 12px;
  margin-bottom: 8px;
}

.title-row h1 {
  margin: 0;
}

.total-card {
  background: linear-gradient(135deg, #ffffff 0%, #fff4e6 100%);
  border-radius: 14px;
  border: 1px solid rgba(224, 122, 47, 0.3);
  padding: 8px 12px;
  font-family: var(--sans);
  box-shadow:
    0 14px 30px rgba(27, 31, 36, 0.12),
    inset 0 0 0 1px rgba(255, 255, 255, 0.6);
  min-width: 160px;
  text-align: right;
  position: relative;
  overflow: hidden;
}

.total-card::after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 15% 20%, rgba(31, 109, 100, 0.18), transparent 55%);
  opacity: 0.6;
  pointer-events: none;
}

.total-card strong {
  display: block;
  color: var(--accent-3);
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  margin-bottom: 4px;
}

.total-card span {
  display: block;
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  position: relative;
  z-index: 1;
}

.toc-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(220px, 1fr));
  gap: 14px;
  align-items: stretch;
}

.toc-hint {
  margin: 0 0 12px;
  color: var(--muted);
  font-size: 1.05rem;
}

.toc-item {
  position: relative;
  display: grid;
  grid-template-columns: 1fr auto;
  grid-template-rows: auto auto;
  gap: 4px 10px;
  padding: 14px 16px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: linear-gradient(135deg, #ffffff 0%, #fff7ec 100%);
  text-decoration: none;
  color: var(--ink);
  font-family: var(--sans);
  box-shadow: 0 10px 24px rgba(27, 31, 36, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  overflow: hidden;
}

.toc-item::before {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 10% 10%, rgba(224, 122, 47, 0.12), transparent 50%),
    radial-gradient(circle at 90% 0%, rgba(31, 109, 100, 0.15), transparent 55%);
  opacity: 0.6;
  pointer-events: none;
}

.toc-name {
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.01em;
  z-index: 1;
}

.toc-meta {
  font-size: 0.78rem;
  color: var(--muted);
  z-index: 1;
}

.toc-arrow {
  grid-row: 1 / span 2;
  align-self: center;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--accent-2);
  z-index: 1;
}

.toc-item:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
  box-shadow: 0 16px 30px rgba(27, 31, 36, 0.12);
}

.chain-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.chain-header h2 {
  margin: 0;
  font-size: 1.6rem;
}

.chain-subtitle {
  margin: 6px 0 0;
  color: var(--muted);
  font-family: var(--sans);
}

.chain-block {
  margin-top: 18px;
  padding-top: 12px;
  border-top: 1px dashed var(--border);
}

.chain-footer {
  margin-top: 18px;
  text-align: right;
  font-family: var(--sans);
}

.chain-footer a {
  color: var(--accent-2);
  text-decoration: none;
  font-weight: 600;
}

@media (max-width: 980px) {
  .toc-grid {
    grid-template-columns: 1fr;
  }
}
"""


def _html_page(title: str, body: str, css: str, lang: str = "en") -> str:
    return f"""<!doctype html>
<html lang="{escape(lang)}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <style>
{css.strip()}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def _unique_anchor(base: str, used: set[str]) -> str:
    candidate = base or "seq"
    if candidate not in used:
        used.add(candidate)
        return candidate
    index = 2
    while f"{candidate}-{index}" in used:
        index += 1
    unique = f"{candidate}-{index}"
    used.add(unique)
    return unique


def build_html_report(
    seq: str,
    meta: Dict[str, str],
    summary: Dict,
    line_width: int,
    part4_text: str,
) -> str:
    if line_width <= 0:
        raise ValueError("line_width must be positive.")

    accession = escape(meta.get("accession") or "User_Sequence")
    length = len(seq)
    enzymes = summary.get("selected_sorted", [])
    enzyme_count = str(len(enzymes)) if enzymes else "0"

    part1_body = _render_part1_body(seq, line_width)
    part2_body = _render_part2_body(enzymes)
    part3_body = _render_part3_body(summary)
    part4_body = _render_part4_body(part4_text)

    body = f"""
<a class="skip-link" href="#content">Skip to content</a>
<div class="report">
  <div class="back-bar">
    <a class="back-link" href="All_in_One.html">返回目录</a>
  </div>
  <header class="hero">
    <div class="hero-top">
      <div>PeptideCutter</div>
      <div class="hero-badge">Sequence Digest</div>
    </div>
    <h1>Cleavage Map Report</h1>
    <p class="subtitle">A visually structured summary of predicted cleavage patterns.</p>
    <div class="hero-grid">
      <div>
        <div class="meta-grid">
          <div class="meta-card"><strong>Accession</strong>{accession}</div>
          <div class="meta-card"><strong>Length</strong>{length} aa</div>
          <div class="meta-card"><strong>Enzymes</strong>{enzyme_count}</div>
        </div>
      </div>
      <div class="hero-panel">
        <p>Use the anchors below to jump between the four report sections.</p>
        <nav class="nav" aria-label="Report sections">
          <a href="#part1">Part 1</a>
          <a href="#part2">Part 2</a>
          <a href="#part3">Part 3</a>
          <a href="#part4">Part 4</a>
        </nav>
      </div>
    </div>
  </header>

  <main id="content">
    <section id="part1" class="sequence">
      <div class="section-title"><span class="tag">Part 1</span><span class="title">Input Sequence</span></div>
      {part1_body}
    </section>

    <section id="part2">
      <div class="section-title"><span class="tag">Part 2</span><span class="title">Selected Enzymes</span></div>
      {part2_body}
    </section>

    <section id="part3">
      <div class="section-title"><span class="tag">Part 3</span><span class="title">Cleavage Site Table</span></div>
      {part3_body}
    </section>

    <section id="part4" class="tracks">
      <div class="section-title"><span class="tag">Part 4</span><span class="title">Cleavage Mapping</span></div>
      {part4_body}
    </section>
  </main>

  <footer>Generated by peptide-cutter</footer>
</div>
"""
    return _html_page("PeptideCutter Report", body, _CSS_COMMON + _CSS_SINGLE)


def build_html_index_report(
    records: List[Dict],
    line_width: int,
    title: str = "PeptideCutter Multi-Sequence Report",
) -> str:
    if line_width <= 0:
        raise ValueError("line_width must be positive.")

    total = len(records)
    toc_items: List[str] = []
    sections: List[str] = []
    used_anchors: set[str] = set()

    for rec in records:
        chain_id = rec.get("chain_id") or rec.get("meta", {}).get("accession") or "SEQ"
        safe_id = rec.get("safe_id") or chain_id
        base_anchor = _safe_anchor(safe_id)
        anchor = _unique_anchor(base_anchor, used_anchors)
        seq = rec["seq"]
        summary = rec["summary"]
        part4_text = rec["part4_text"]

        enzymes = summary.get("selected_sorted", [])
        enzyme_count = str(len(enzymes)) if enzymes else "0"
        length = len(seq)

        toc_items.append(
            "\n".join(
                [
                    f"<a href=\"#{anchor}\" class=\"toc-item\">",
                    f"  <div class=\"toc-name\">{escape(str(chain_id))}</div>",
                    f"  <div class=\"toc-meta\">{length} aa · {enzyme_count} enzymes</div>",
                    "  <div class=\"toc-arrow\">&gt;</div>",
                    "</a>",
                ]
            )
        )

        part1_body = _render_part1_body(seq, line_width)
        part2_body = _render_part2_body(enzymes)
        part3_body = _render_part3_body(summary)
        part4_body = _render_part4_body(part4_text)

        section_html = f"""
    <section id="{anchor}" class="chain-section">
      <div class="chain-header">
        <div>
          <h2>{escape(str(chain_id))}</h2>
          <p class="chain-subtitle">Length {length} aa · Enzymes {enzyme_count}</p>
        </div>
        <nav class="nav chain-nav" aria-label="Chain sections">
          <a href="#{anchor}-part1">Part 1</a>
          <a href="#{anchor}-part2">Part 2</a>
          <a href="#{anchor}-part3">Part 3</a>
          <a href="#{anchor}-part4">Part 4</a>
        </nav>
      </div>

      <div id="{anchor}-part1" class="chain-block">
        <div class="section-title"><span class="tag">Part 1</span><span class="title">Input Sequence</span></div>
        {part1_body}
      </div>

      <div id="{anchor}-part2" class="chain-block">
        <div class="section-title"><span class="tag">Part 2</span><span class="title">Selected Enzymes</span></div>
        {part2_body}
      </div>

      <div id="{anchor}-part3" class="chain-block">
        <div class="section-title"><span class="tag">Part 3</span><span class="title">Cleavage Site Table</span></div>
        {part3_body}
      </div>

      <div id="{anchor}-part4" class="chain-block tracks">
        <div class="section-title"><span class="tag">Part 4</span><span class="title">Cleavage Mapping</span></div>
        {part4_body}
      </div>

      <div class="chain-footer"><a href="#top">Back to top</a></div>
    </section>
        """.rstrip()
        sections.append(section_html)

    toc_html = "\n".join(toc_items) if toc_items else "<p>No records found.</p>"
    sections_html = "\n".join(sections)

    body = f"""
<a class="skip-link" href="#content">Skip to content</a>
<div class="report" id="top">
  <header class="hero">
    <div class="hero-top">
      <div>PeptideCutter</div>
      <div class="hero-badge">Sequence Digest</div>
    </div>
    <div class="title-row">
      <h1>{escape(title)}</h1>
      <div class="total-card"><strong>Total Chains</strong><span>{total}</span></div>
    </div>
    <div class="hero-grid">
      <div class="hero-panel">
        <p class="toc-hint">Click a chain name to jump to its detailed report section.</p>
        <div class="toc-grid">
          {toc_html}
        </div>
      </div>
    </div>
  </header>

  <main id="content">
    {sections_html}
  </main>

  <footer>Generated by peptide-cutter</footer>
</div>
"""
    return _html_page(title, body, _CSS_COMMON + _CSS_SINGLE + _CSS_INDEX)


def _render_part1_body(seq: str, line_width: int) -> str:
    seq_block = _render_pre(_render_sequence_display(seq, line_width), "sequence-block")
    return f"{seq_block}"


def _render_part2_body(enzymes: List[str]) -> str:
    intro = "<p>Selected cleavage enzymes and chemicals.</p>"
    if enzymes:
        items = "\n".join(f"<li>{escape(name)}</li>" for name in enzymes)
        list_html = f"<ul class=\"enzyme-list\">{items}</ul>"
    else:
        list_html = "<p>No enzymes selected.</p>"

    note_html = ""
    if _has_proline_endopeptidase(enzymes):
        note_html = (
            "<div class=\"note\">[*] NOTE: Proline-endopeptidase was reported to cleave "
            "only substrates whose sequences do not exceed 30 amino acids. An unusual "
            "beta-propeller domain regulates proteolysis: see "
            f"<a href=\"{_PROLINE_NOTE_URL}\">Fulop et al., 1998</a>.</div>"
        )

    return f"{intro}{list_html}{note_html}"


def _render_part3_body(summary: Dict) -> str:
    rows = [row for row in summary.get("table_rows", []) if row.get("count", 0) > 0]
    if not rows:
        table_html = "<p>No cleavage sites found.</p>"
    else:
        thead = "".join(
            f"<th scope=\"col\">{escape(cell)}</th>"
            for cell in [
                "Name of enzyme",
                "No. of cleavages",
                "Positions of cleavage sites",
            ]
        )
        tbody_rows: List[str] = []
        for row in rows:
            positions = ", ".join(str(p) for p in row.get("sites", [])) or "-"
            cells = "".join(
                [
                    f"<th scope=\"row\">{escape(str(row['name']))}</th>",
                    f"<td>{escape(str(row['count']))}</td>",
                    f"<td>{escape(positions)}</td>",
                ]
            )
            tbody_rows.append(f"<tr>{cells}</tr>")
        tbody = "".join(tbody_rows)
        table_html = (
            "<table>"
            "<caption class=\"sr-only\">Cleavage site table</caption>"
            f"<thead><tr>{thead}</tr></thead>"
            f"<tbody>{tbody}</tbody>"
            "</table>"
        )

    do_not_cut = summary.get("do_not_cut", [])
    if do_not_cut:
        notice = "The selected enzymes do not cut: " + ", ".join(do_not_cut)
    else:
        notice = "The selected enzymes do not cut: None"
    notice_html = f"<div class=\"notice\">{escape(notice)}</div>"
    return f"{table_html}{notice_html}"


def _render_part4_body(part4_text: str) -> str:
    text = part4_text.strip("\n")
    return _render_pre(text, "tracks-block")


def _render_pre(text: str, pre_class: str) -> str:
    safe = escape(text)
    return f"<pre class=\"{pre_class}\"><code>{safe}</code></pre>"


def _safe_anchor(text: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in str(text))
    cleaned = "-".join(part for part in cleaned.split("-") if part)
    return cleaned.lower() or "seq"


def _render_sequence_display(seq: str, width: int) -> str:
    index_width = len(str(len(seq)))
    lines: List[str] = []
    for start in range(1, len(seq) + 1, width):
        chunk = seq[start - 1 : start - 1 + width]
        ruler = _build_ruler(start, len(chunk))
        lines.append(" " * (index_width + 1) + ruler)
        lines.append(f"{start:>{index_width}} {chunk}")
    return "\n".join(lines)


def _build_ruler(start: int, length: int) -> str:
    if length <= 0:
        return ""
    blocks: List[str] = []
    for offset in range(10, length + 1, 10):
        pos = start + offset - 1
        blocks.append(f"{pos:>10}")
    return "".join(blocks)


def _has_proline_endopeptidase(enzymes: List[str]) -> bool:
    for name in enzymes:
        cleaned = name.replace("[*]", "").strip()
        if cleaned == "Proline-endopeptidase":
            return True
    return False
