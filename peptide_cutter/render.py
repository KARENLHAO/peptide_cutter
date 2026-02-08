from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Dict, List


def render_result_parts(
    seq: str, meta: Dict, selected: List[str], summary: Dict, line_width: int
) -> List[str]:
    part1: List[str] = []
    part1.append("Input sequence display")

    accession = meta.get("accession", "User_Sequence")
    part1.append(f"Accession: {accession}")
    part1.append(f"The sequence is {len(seq)} amino acids long.")
    part1.append("```")
    part1.append(_render_sequence_display(seq, line_width))
    part1.append("```")
    part1.append(f"The sequence is {len(seq)} amino acids long.")

    part2: List[str] = []
    part2.append(
        "Selected cleavage enzymes and chemicals [available enzymes]:"
    )
    for name in summary["selected_sorted"]:
        part2.append(f"- {name}")
    if _has_proline_endopeptidase(summary["selected_sorted"]):
        part2.append(
            "[*] NOTE: Proline-endopeptidase was reported to cleave only substrates "
            "whose sequences do not exceed 30 amino acids. An unusual beta-propeller "
            "domain regulates proteolysis: see Fulop et al., 1998. "
            "https://pubmed.ncbi.nlm.nih.gov/9695945/"
        )

    part3: List[str] = []
    part3.append("Cleavage site table")
    part3.append(
        "| Name of enzyme | No. of cleavages | Positions of cleavage sites |"
    )
    part3.append("| --- | --- | --- |")
    for row in summary["table_rows"]:
        if row["count"] == 0:
            continue
        positions = ", ".join(str(p) for p in row["sites"]) if row["sites"] else "-"
        part3.append(f"| {row['name']} | {row['count']} | {positions} |")

    part3.append("")
    do_not_cut = summary["do_not_cut"]
    if do_not_cut:
        part3.append("The selected enzymes do not cut: " + ", ".join(do_not_cut))
    else:
        part3.append("The selected enzymes do not cut: None")

    return [
        _finalize_section(part1),
        _finalize_section(part2),
        _finalize_section(part3),
    ]


def render_result_txt(
    seq: str, meta: Dict, selected: List[str], summary: Dict, line_width: int
) -> str:
    parts = render_result_parts(seq, meta, selected, summary, line_width)
    return "\n\n".join(part.rstrip() for part in parts).rstrip() + "\n"


def render_part3_csv(
    summary: Dict,
    chain_id: str | None = None,
    include_header: bool = True,
) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    header = ["Name of enzyme", "No. of cleavages", "Positions of cleavage sites"]
    if chain_id is not None:
        header = ["Chain ID"] + header
    if include_header:
        writer.writerow(header)
    for row in summary["table_rows"]:
        if row["count"] == 0:
            continue
        positions = ", ".join(str(p) for p in row["sites"]) if row["sites"] else "-"
        name = _clean_csv_enzyme_name(row["name"])
        record = [name, row["count"], positions]
        if chain_id is not None:
            record = [chain_id] + record
        writer.writerow(record)
    return buffer.getvalue()


def write_result_parts(path: str, parts: List[str]) -> List[Path]:
    base = Path(path)
    suffix = base.suffix or ".txt"
    stem = base.stem if base.suffix else base.name
    out_dir = _resolve_output_dir()
    outputs: List[Path] = []
    for index, content in enumerate(parts, start=1):
        out_path = out_dir / f"{stem}_part{index}{suffix}"
        out_path.write_text(content, encoding="utf-8")
        outputs.append(out_path)
    return outputs


def write_part3_csv(path: str, csv_text: str) -> Path:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(csv_text, encoding="utf-8")
    return out_path


def _resolve_output_dir() -> Path:
    out_dir = Path("tmp") / "parts_txts"
    enzyme_dir = Path("tmp") / "enzyme_txts"
    out_dir.mkdir(parents=True, exist_ok=True)
    enzyme_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def _finalize_section(lines: List[str]) -> str:
    return "\n".join(lines).rstrip() + "\n"


def _has_proline_endopeptidase(names: List[str]) -> bool:
    for name in names:
        cleaned = name.replace("[*]", "").strip()
        if cleaned == "Proline-endopeptidase":
            return True
    return False


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


def _clean_csv_enzyme_name(name: str) -> str:
    return name.replace("[*]", "").strip()
