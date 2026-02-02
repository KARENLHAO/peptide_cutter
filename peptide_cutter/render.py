from __future__ import annotations

from typing import Dict, List


def render_result_txt(
    seq: str, meta: Dict, selected: List[str], summary: Dict, line_width: int
) -> str:
    parts: List[str] = []
    parts.append("## Part 1: Input sequence display")

    accession = meta.get("accession", "User_Sequence")
    description = meta.get("description", "N/A")
    parts.append(f"Accession: {accession}")
    parts.append(f"Description: {description}")
    parts.append(f"The sequence is {len(seq)} amino acids long.")
    parts.append("```")
    parts.append(_render_sequence_display(seq))
    parts.append("```")

    replacements = meta.get("replacements", {})
    if replacements:
        replacement_notes = []
        for src in sorted(replacements):
            info = replacements[src]
            replacement_notes.append(
                f"{src}->{info['to']} (count={info['count']})"
            )
        parts.append("Replacements applied: " + "; ".join(replacement_notes))

    parts.append("")
    parts.append(
        "## Part 2: Selected cleavage enzymes and chemicals (all) [available enzymes]:"
    )
    for name in summary["selected_sorted"]:
        parts.append(f"- {name}")

    do_not_cut = summary["do_not_cut"]
    if do_not_cut:
        parts.append("The selected enzymes do not cut: " + ", ".join(do_not_cut))
    else:
        parts.append("The selected enzymes do not cut: None")

    parts.append("")
    parts.append("## Part 3: Cleavage site table")
    parts.append(
        "| Name of enzyme | No. of cleavages | Positions of cleavage sites |"
    )
    parts.append("| --- | --- | --- |")
    for row in summary["table_rows"]:
        positions = ", ".join(str(p) for p in row["sites"]) if row["sites"] else "-"
        parts.append(
            f"| {row['name']} | {row['count']} | {positions} |"
        )

    parts.append("")
    parts.append("## Part 4: Sequence map")
    parts.append("```")
    parts.append(_render_sequence_map(seq, summary["groups"], line_width))
    parts.append("```")

    return "\n".join(parts).rstrip() + "\n"


def write_result(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _render_sequence_display(seq: str) -> str:
    width = 60
    index_width = len(str(len(seq)))
    lines: List[str] = []
    for start in range(1, len(seq) + 1, width):
        chunk = seq[start - 1 : start - 1 + width]
        ruler = _build_ruler(start, len(chunk))
        lines.append(" " * (index_width + 1) + ruler)
        lines.append(f"{start:>{index_width}} {chunk}")
    return "\n".join(lines)


def _render_sequence_map(seq: str, groups: List[Dict], line_width: int) -> str:
    label_width = max(
        [len(group["name"]) for group in groups] + [len("Ruler"), len("Sequence")]
    )
    length = len(seq)
    lines: List[str] = []

    for start in range(1, length + 1, line_width):
        end = min(start + line_width - 1, length)
        chunk = seq[start - 1 : end]
        lines.append(f"Window {start}-{end}")
        for group in groups:
            marker = _marker_line(group["sites"], start, end, line_width)
            lines.append(f"{group['name']:<{label_width}} {marker}")
        ruler = _build_ruler(start, len(chunk)).ljust(line_width)
        lines.append(f"{'Ruler':<{label_width}} {ruler}")
        lines.append(f"{'Sequence':<{label_width}} {chunk.ljust(line_width)}")
        if end < length:
            lines.append("")

    return "\n".join(lines)


def _marker_line(sites: List[int], start: int, end: int, width: int) -> str:
    site_set = set(sites)
    length = end - start + 1
    markers = ["|" if pos in site_set else " " for pos in range(start, end + 1)]
    if length < width:
        markers.extend([" "] * (width - length))
    return "".join(markers)


def _build_ruler(start: int, length: int) -> str:
    if length <= 0:
        return ""
    blocks: List[str] = []
    for offset in range(10, length + 1, 10):
        pos = start + offset - 1
        blocks.append(f"{pos:>10}")
    return "".join(blocks)
