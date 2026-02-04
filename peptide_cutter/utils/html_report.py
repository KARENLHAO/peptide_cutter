from __future__ import annotations

from html import escape
from typing import Dict, List


_PROLINE_NOTE_URL = "https://pubmed.ncbi.nlm.nih.gov/9695945/"


def build_html_report(
    seq: str,
    meta: Dict[str, str],
    summary: Dict,
    line_width: int,
    part4_text: str,
) -> str:
    accession = escape(meta.get("accession") or "User_Sequence")
    length = len(seq)
    enzymes = summary.get("selected_sorted", [])
    enzyme_count = str(len(enzymes)) if enzymes else "0"

    part1_body = _render_part1_body(seq, line_width)
    part2_body = _render_part2_body(enzymes)
    part3_body = _render_part3_body(summary)
    part4_body = _render_part4_body(part4_text)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>PeptideCutter Report</title>
  <style>
    :root {{
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
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: var(--serif);
      color: var(--ink);
      background: var(--bg);
      line-height: 1.6;
    }}

    body::before {{
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
    }}

    body::after {{
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
    }}

    .report {{
      max-width: 1140px;
      margin: 0 auto;
      padding: 44px 24px 90px;
      position: relative;
    }}

    .report::before {{
      content: "";
      position: absolute;
      top: 28px;
      bottom: 28px;
      left: 16px;
      width: 4px;
      border-radius: 999px;
      background: linear-gradient(180deg, rgba(224, 122, 47, 0.8), rgba(31, 109, 100, 0.7));
      opacity: 0.8;
    }}

    .hero {{
      padding: 30px 36px 26px;
      border-radius: 22px;
      background: var(--panel);
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      position: relative;
      overflow: hidden;
    }}

    .hero::after {{
      content: "";
      position: absolute;
      top: -60px;
      left: -60px;
      width: 160px;
      height: 160px;
      border-radius: 32px;
      background: linear-gradient(135deg, rgba(31, 109, 100, 0.16), transparent);
      transform: rotate(12deg);
    }}

    .hero-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      font-family: var(--sans);
      text-transform: uppercase;
      letter-spacing: 0.2em;
      font-size: 0.72rem;
      color: var(--accent-2);
    }}

    .hero-badge {{
      padding: 6px 12px;
      border-radius: 999px;
      border: 1px dashed rgba(31, 109, 100, 0.45);
      background: rgba(31, 109, 100, 0.08);
    }}

    h1 {{
      font-family: var(--sans);
      font-size: 2.5rem;
      margin: 12px 0 10px;
      letter-spacing: 0.02em;
      color: var(--accent-3);
    }}

    .subtitle {{
      color: var(--muted);
      margin: 0 0 18px;
      font-size: 1.02rem;
    }}

    .hero-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.8fr) minmax(0, 1fr);
      gap: 22px;
      align-items: start;
    }}

    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 12px;
      margin-top: 10px;
    }}

    .meta-card {{
      border-radius: 14px;
      padding: 12px 14px;
      background: #fffdf9;
      border: 1px solid rgba(0, 0, 0, 0.06);
      font-family: var(--sans);
      font-size: 0.85rem;
      color: var(--muted);
    }}

    .meta-card strong {{
      display: block;
      font-size: 0.95rem;
      color: var(--ink);
      letter-spacing: 0.02em;
    }}

    .hero-panel {{
      padding: 16px;
      border-radius: 16px;
      border: 1px solid rgba(224, 122, 47, 0.24);
      background: linear-gradient(160deg, rgba(224, 122, 47, 0.12), rgba(255, 255, 255, 0.85));
      font-family: var(--sans);
      color: var(--ink);
    }}

    .hero-panel p {{
      margin: 0 0 12px;
    }}

    .nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .nav a {{
      padding: 6px 12px;
      border-radius: 999px;
      border: 1px solid rgba(0, 0, 0, 0.12);
      font-size: 0.82rem;
      text-decoration: none;
      color: var(--accent-3);
      background: rgba(255, 255, 255, 0.8);
    }}

    .nav a:hover {{
      border-color: var(--accent);
      color: var(--accent);
    }}

    section {{
      margin-top: 30px;
      padding: 26px 28px;
      border-radius: 18px;
      border: 1px solid var(--border);
      background: var(--panel);
      box-shadow: 0 12px 26px rgba(25, 24, 20, 0.08);
      position: relative;
    }}

    .section-title {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }}

    .section-title .tag {{
      font-family: var(--sans);
      font-size: 0.72rem;
      letter-spacing: 0.24em;
      text-transform: uppercase;
      color: var(--accent-2);
      border-bottom: 2px solid var(--accent-2);
      padding-bottom: 4px;
    }}

    .section-title .title {{
      font-family: var(--sans);
      font-size: 1.4rem;
      color: var(--accent-3);
      letter-spacing: 0.01em;
    }}

    p {{
      margin: 0 0 12px;
      color: var(--muted);
    }}

    .sequence pre,
    .tracks pre {{
      font-family: var(--mono);
      font-size: 0.9rem;
      line-height: 1.5;
      background: #ffffff;
      color: #1a1a1a;
      padding: 18px 18px;
      border-radius: 14px;
      border: 1px solid rgba(0, 0, 0, 0.08);
      overflow-x: auto;
    }}

    .tracks pre {{
      background: #0f1d1c;
      color: #f5efe6;
      border: 1px solid rgba(31, 109, 100, 0.5);
      box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.04);
    }}

    .enzyme-list {{
      columns: 2;
      column-gap: 30px;
      padding-left: 18px;
      margin: 12px 0 0;
      font-family: var(--sans);
      color: var(--ink);
    }}

    .enzyme-list li {{
      break-inside: avoid;
      margin-bottom: 6px;
    }}

    .note {{
      margin-top: 14px;
      padding: 12px 14px;
      border-radius: 12px;
      border: 1px solid rgba(224, 122, 47, 0.35);
      background: rgba(224, 122, 47, 0.12);
      font-family: var(--sans);
      color: var(--accent-3);
    }}

    .note a {{
      color: var(--accent-3);
      text-decoration: underline;
      text-decoration-thickness: 2px;
      text-underline-offset: 3px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 14px;
      font-family: var(--sans);
      font-size: 0.95rem;
      background: #fffdfa;
      border: 1px solid rgba(0, 0, 0, 0.06);
    }}

    thead {{
      background: rgba(31, 109, 100, 0.14);
    }}

    th, td {{
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    }}

    tbody tr:nth-child(even) {{
      background: rgba(0, 0, 0, 0.03);
    }}

    .notice {{
      margin-top: 12px;
      padding: 12px 14px;
      border-left: 4px solid var(--accent-2);
      background: rgba(31, 109, 100, 0.12);
      font-family: var(--sans);
      color: var(--accent-3);
    }}

    footer {{
      margin-top: 34px;
      font-family: var(--sans);
      font-size: 0.85rem;
      color: var(--muted);
      text-align: center;
    }}

    @media (max-width: 980px) {{
      .hero-grid {{
        grid-template-columns: 1fr;
      }}

      .enzyme-list {{
        columns: 1;
      }}
    }}
  </style>
</head>
<body>
  <div class="report">
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
          <div class="nav">
            <a href="#part1">Part 1</a>
            <a href="#part2">Part 2</a>
            <a href="#part3">Part 3</a>
            <a href="#part4">Part 4</a>
          </div>
        </div>
      </div>
    </header>

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

    <footer>Generated by peptide-cutter</footer>
  </div>
</body>
</html>
"""


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
            f"<th>{escape(cell)}</th>"
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
                f"<td>{escape(cell)}</td>"
                for cell in [row["name"], str(row["count"]), positions]
            )
            tbody_rows.append(f"<tr>{cells}</tr>")
        tbody = "".join(tbody_rows)
        table_html = f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>"

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
