from __future__ import annotations

import re
from typing import Dict, List, Tuple

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


def parse_fasta_records(
    text: str, max_records: int | None = None
) -> List[Tuple[str, str, str]]:
    records: List[Tuple[str, str, str]] = []
    cur_id: str | None = None
    cur_desc: str = "N/A"
    cur_seq: List[str] = []

    def push_record() -> None:
        nonlocal cur_id, cur_desc, cur_seq
        if cur_id is None:
            return
        seq = re.sub(r"[\s\d]+", "", "".join(cur_seq)).upper()
        records.append((cur_id, cur_desc, seq))
        cur_id = None
        cur_desc = "N/A"
        cur_seq = []

    lines = text.splitlines()
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            if cur_id is not None:
                push_record()
            if max_records is not None and len(records) >= max_records:
                raise ValueError(
                    f"FASTA contains more than {max_records} records."
                )
            header = line[1:].strip()
            if not header:
                cur_id = "User_Sequence"
                cur_desc = "N/A"
            else:
                parts = header.split(None, 1)
                cur_id = parts[0] or "User_Sequence"
                cur_desc = parts[1].strip() if len(parts) > 1 else "N/A"
        else:
            if cur_id is None:
                raise ValueError("FASTA must start with a '>' header line.")
            cur_seq.append(line)

    if cur_id is not None:
        push_record()

    return records


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
