from __future__ import annotations

import argparse
import sys
import re
import shutil
import os
from pathlib import Path
from typing import List

from .aggregate import build_summary
from .engine import find_cleavage_sites
from .render import (
    render_part3_csv,
    render_result_parts,
    write_part3_csv,
    write_result_parts,
)
from .utils.html_report import build_html_report
from .utils.merge_part4_txts import (
    enzyme_abbr,
    generate_enzyme_txts,
    normalize_abbr,
    render_part4_text_from_rows,
)
from .rules import load_rules
from .sequence import extract_fasta_header, parse_sequence, validate_sequence


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PeptideCutter")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--seq", help="Sequence text (raw or FASTA)")
    group.add_argument("--fasta", help="FASTA file path")
    rules_default = Path(__file__).with_name("cleavage_rules.json")
    parser.add_argument("--rules", default=str(rules_default))
    parser.add_argument(
        "--enzymes",
        nargs="+",
        required=True,
        help="Enzyme names or abbreviations. Use 'all' for all enzymes. "
        "Multiple enzymes can be provided as a semicolon-separated string.",
    )
    parser.add_argument(
        "--out",
        default=".",
        help="Output directory (default: .).",
    )
    parser.add_argument(
        "--line-width",
        type=int,
        default=60,
        help="Line width for sequence display and Part 4 blocks (10-60).",
    )
    parser.add_argument(
        "--cleanup-tmp",
        action="store_true",
        help="Remove the tmp directory after the run completes.",
    )
    args = parser.parse_args(argv)

    try:
        text = _load_input_text(args.seq, args.fasta)
        accession, description = extract_fasta_header(text)
        seq = parse_sequence(text)
        seq, meta = validate_sequence(seq, strict=True)
        meta["accession"] = accession
        meta["description"] = description

        if not seq:
            raise ValueError("Sequence is empty after cleaning.")

        if not 10 <= args.line_width <= 60:
            raise ValueError("--line-width must be between 10 and 60.")
        rules = load_rules(args.rules)
        selected = _select_enzymes(args.enzymes, rules)

        sites_by_enzyme = find_cleavage_sites(seq, rules, selected)
        summary = build_summary(selected, sites_by_enzyme)
        parts = render_result_parts(seq, meta, selected, summary, args.line_width)

        html_out = _resolve_html_out(args.out)
        txt_base = html_out.with_suffix(".txt")

        write_result_parts(str(txt_base), parts)
        part3_csv = render_part3_csv(summary)
        write_part3_csv(str(html_out), part3_csv)
        enzyme_dir = Path("tmp") / "enzyme_txts"
        rows = [
            (row["name"], row["sites"])
            for row in summary["table_rows"]
            if row["count"] > 0
        ]
        generate_enzyme_txts(
            rows=rows,
            seq_id=meta.get("accession", "SEQ"),
            seq=seq,
            out_dir=enzyme_dir,
            block_size=args.line_width,
        )
        part4_text = render_part4_text_from_rows(
            rows=rows,
            seq=seq,
            block_size=args.line_width,
        )
        part4_path = Path("tmp") / "parts_txts" / f"{txt_base.stem}_part4.txt"
        part4_path.write_text(part4_text, encoding="utf-8")

        html = build_html_report(
            seq=seq,
            meta=meta,
            summary=summary,
            line_width=args.line_width,
            part4_text=part4_text,
        )
        html_out.write_text(html, encoding="utf-8")

        if args.cleanup_tmp:
            tmp_dir = Path("tmp")
            if tmp_dir.exists():
                shutil.rmtree(tmp_dir)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


def _load_input_text(seq_arg: str | None, fasta_path: str | None) -> str:
    if fasta_path:
        path = Path(fasta_path)
        if not path.exists():
            raise ValueError(f"FASTA file not found: {fasta_path}")
        return path.read_text(encoding="utf-8")
    if seq_arg is not None:
        return seq_arg
    raise ValueError("Either --seq or --fasta must be provided.")


def _select_enzymes(requested: List[str], rules) -> List[str]:
    requested = _split_enzymes_args(requested)
    if len(requested) == 1 and requested[0].lower() == "all":
        return sorted(rules.enzymes.keys(), key=_natural_key)
    if any(item.lower() == "all" for item in requested):
        raise ValueError("--enzymes 'all' cannot be combined with other names")

    full_names = list(rules.enzymes.keys())
    full_by_lower = {name.lower(): name for name in full_names}
    abbr_map: dict[str, str] = {}
    for name in full_names:
        try:
            abbr = normalize_abbr(enzyme_abbr(name)).lower()
        except Exception:
            continue
        abbr_map.setdefault(abbr, name)

    resolved: List[str] = []
    missing: List[str] = []
    for token in requested:
        if token in rules.enzymes:
            resolved.append(token)
            continue
        lower = token.lower()
        if lower in full_by_lower:
            resolved.append(full_by_lower[lower])
            continue
        abbr = normalize_abbr(token).lower()
        if abbr in abbr_map:
            resolved.append(abbr_map[abbr])
            continue
        missing.append(token)

    if missing:
        raise ValueError("Unknown enzymes: " + ", ".join(sorted(missing)))
    return sorted(set(resolved), key=_natural_key)


def _natural_key(text: str):
    parts = re.split(r"(\d+)", text)
    key: List[object] = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part.lower())
    return tuple(key)


def _split_enzymes_args(raw: List[str]) -> List[str]:
    if not raw:
        return []
    if len(raw) == 1:
        value = raw[0].strip()
        if value.lower() == "all":
            return [value]
        if ";" in value:
            return [item.strip() for item in value.split(";") if item.strip()]
        return [value]
    return [item.strip() for item in raw if item.strip()]


def _resolve_html_out(out_arg: str) -> Path:
    if not out_arg:
        return Path("./report.html")
    if out_arg.endswith(os.sep) or out_arg in {".", ".."}:
        out_dir = Path(out_arg)
        out_dir.mkdir(parents=True, exist_ok=True)
        return out_dir / "report.html"
    out_path = Path(out_arg)
    if out_path.exists() and out_path.is_dir():
        return out_path / "report.html"
    if out_path.suffix.lower() != ".html":
        return out_path.with_suffix(".html")
    return out_path


if __name__ == "__main__":
    raise SystemExit(main())
