from __future__ import annotations

import argparse
import sys
import re
import random
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
from .utils.merge_part4_txts import generate_enzyme_txts, render_part4_text_from_rows
from .rules import load_rules
from .sequence import extract_fasta_header, parse_sequence, validate_sequence


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PeptideCutter")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--seq", help="Sequence text (raw or FASTA)")
    group.add_argument("--fasta", help="FASTA file path")
    rules_default = Path(__file__).with_name("cleavage_rules.json")
    parser.add_argument("--rules", default=str(rules_default))
    parser.add_argument("--enzymes", nargs="+", required=True)
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
        "--prob",
        type=float,
        default=1.0,
        help="Probability [0-1] to keep cleavage sites for the selected enzyme.",
    )
    parser.add_argument(
        "--prob-target",
        choices=["trypsin", "chymotrypsin"],
        default="trypsin",
        help="Which enzyme the --prob applies to.",
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
        if not 0.0 <= args.prob <= 1.0:
            raise ValueError("--prob must be between 0 and 1.")

        rules = load_rules(args.rules)
        selected = _select_enzymes(args.enzymes, rules)

        sites_by_enzyme = find_cleavage_sites(seq, rules, selected)
        if args.prob < 1.0:
            rng = random.Random()
            for enzyme_name, sites in sites_by_enzyme.items():
                if args.prob_target == "trypsin" and enzyme_name == "Trypsin":
                    sites_by_enzyme[enzyme_name] = [
                        pos for pos in sites if rng.random() < args.prob
                    ]
                elif args.prob_target == "chymotrypsin" and enzyme_name.startswith(
                    "Chymotrypsin"
                ):
                    sites_by_enzyme[enzyme_name] = [
                        pos for pos in sites if rng.random() < args.prob
                    ]
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
    if len(requested) == 1 and requested[0].lower() == "all":
        return sorted(rules.enzymes.keys(), key=_natural_key)
    if any(item.lower() == "all" for item in requested):
        raise ValueError("--enzymes 'all' cannot be combined with other names")

    requested_unique = sorted(set(requested))
    missing = [name for name in requested_unique if name not in rules.enzymes]
    if missing:
        raise ValueError("Unknown enzymes: " + ", ".join(sorted(missing)))
    return sorted(requested_unique, key=_natural_key)


def _natural_key(text: str):
    parts = re.split(r"(\d+)", text)
    key: List[object] = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part.lower())
    return tuple(key)


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
