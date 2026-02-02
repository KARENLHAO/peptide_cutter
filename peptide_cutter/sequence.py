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


def validate_sequence(
    seq: str, strict: bool, replacements: Dict[str, str] | None
) -> Tuple[str, Dict]:
    seq = seq.upper()
    replacements = {k.upper(): v.upper() for k, v in (replacements or {}).items()}

    invalid_positions: Dict[str, list[int]] = {}
    for idx, aa in enumerate(seq, start=1):
        if aa not in STANDARD_AA:
            invalid_positions.setdefault(aa, []).append(idx)

    meta: Dict[str, object] = {
        "replacements": {},
        "invalid_positions": invalid_positions,
        "replaced": False,
    }

    if replacements:
        for src, dst in replacements.items():
            if len(src) != 1 or len(dst) != 1:
                raise ValueError(f"Invalid replacement mapping: {src}={dst}")
            if dst not in STANDARD_AA:
                raise ValueError(
                    f"Invalid replacement target '{dst}'. Must be a standard amino acid."
                )

        chars = list(seq)
        counts: Dict[str, int] = {}
        for i, aa in enumerate(chars):
            if aa in replacements:
                counts[aa] = counts.get(aa, 0) + 1
                chars[i] = replacements[aa]
        seq = "".join(chars)
        for src, count in counts.items():
            meta["replacements"][src] = {"to": replacements[src], "count": count}
        meta["replaced"] = bool(counts)

    remaining_invalid: Dict[str, list[int]] = {}
    for idx, aa in enumerate(seq, start=1):
        if aa not in STANDARD_AA:
            remaining_invalid.setdefault(aa, []).append(idx)

    if strict and remaining_invalid:
        raise ValueError(_format_illegal_error(remaining_invalid))

    return seq, meta


def _format_illegal_error(invalid_positions: Dict[str, list[int]]) -> str:
    parts = []
    for aa in sorted(invalid_positions):
        pos = ", ".join(str(p) for p in invalid_positions[aa])
        parts.append(f"{aa}: [{pos}]")
    suggestions = (
        "Suggestions: B -> D or N; Z -> E or Q; J -> I or L; "
        "X requires explicit replacement. Other non-standard letters must be "
        "replaced via --replace to a standard amino acid."
    )
    return "Illegal amino acid characters found: " + "; ".join(parts) + ". " + suggestions
