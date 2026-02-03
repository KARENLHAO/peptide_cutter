from __future__ import annotations

import re
from typing import Dict, Tuple

STANDARD_AA = set("ACDEFGHIKLMNPQRSTVWY")


def parse_sequence(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith(">"):
        lines = lines[1:]
    cleaned = re.sub(r"[\s\d]+", "", "".join(lines))
    return cleaned.upper()


def extract_fasta_header(text: str) -> Tuple[str, str]:
    lines = text.splitlines()
    if lines and lines[0].startswith(">"):
        header = lines[0][1:].strip()
        if not header:
            return "User_Sequence", "N/A"
        parts = header.split(None, 1)
        accession = parts[0]
        description = parts[1].strip() if len(parts) > 1 else "N/A"
        return accession, description or "N/A"
    return "User_Sequence", "N/A"


def validate_sequence(seq: str, strict: bool) -> Tuple[str, Dict]:
    seq = seq.upper()

    invalid_positions: Dict[str, list[int]] = {}
    for idx, aa in enumerate(seq, start=1):
        if aa not in STANDARD_AA:
            invalid_positions.setdefault(aa, []).append(idx)

    meta: Dict[str, object] = {
        "invalid_positions": invalid_positions,
    }

    if strict and invalid_positions:
        raise ValueError(_format_illegal_error(invalid_positions))

    return seq, meta


def _format_illegal_error(invalid_positions: Dict[str, list[int]]) -> str:
    illegal = ", ".join(sorted(invalid_positions))
    return f"Illegal amino acid character(s) found: {illegal}"
