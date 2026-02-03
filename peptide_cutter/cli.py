from __future__ import annotations

import argparse
import sys
import re
from pathlib import Path
from typing import Dict, List

from .aggregate import build_summary
from .engine import find_cleavage_sites
from .render import render_result_txt, write_result
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
    parser.add_argument("--out", default="./result.txt")
    parser.add_argument("--line-width", type=int, default=60)
    parser.add_argument("--replace", action="append", default=[])

    args = parser.parse_args(argv)

    try:
        text = _load_input_text(args.seq, args.fasta)
        accession, description = extract_fasta_header(text)
        seq = parse_sequence(text)
        replacements = _parse_replacements(args.replace)
        seq, meta = validate_sequence(seq, strict=True, replacements=replacements)
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
        content = render_result_txt(seq, meta, selected, summary, args.line_width)
        write_result(args.out, content)
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


def _parse_replacements(values: List[str]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--replace must be in the form X=Y")
        src, dst = value.split("=", 1)
        src = src.strip().upper()
        dst = dst.strip().upper()
        if len(src) != 1 or len(dst) != 1:
            raise ValueError("--replace must use single-letter amino acids")
        mapping[src] = dst
    return mapping


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


if __name__ == "__main__":
    raise SystemExit(main())
