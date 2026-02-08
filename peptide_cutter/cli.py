from __future__ import annotations

import argparse
import sys
import re
import shutil
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
from .utils.html_report import build_html_report, build_html_index_report
from .utils.merge_part4_txts import (
    enzyme_abbr,
    generate_enzyme_txts,
    normalize_abbr,
    render_part4_text_from_rows,
)
from .rules import load_rules
from .sequence import (
    extract_fasta_header,
    parse_fasta_records,
    parse_sequence,
    validate_sequence,
)

MAX_FASTA_RECORDS = 10000
MERGED_CSV_NAME = "All_in_One.csv"
MERGED_HTML_NAME = "All_in_One.html"


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
        help="Base output directory (default: .).",
    )
    parser.add_argument(
        "--line-width",
        type=int,
        default=60,
        help="Line width for sequence display and Part 4 blocks (10-60).",
    )
    parser.add_argument(
        "--csv-name",
        default=MERGED_CSV_NAME,
        help="Merged CSV file name (default: All_in_One.csv).",
    )
    parser.add_argument(
        "--cleanup-tmp",
        action="store_true",
        help="Remove the tmp directory after the run completes.",
    )
    parser.add_argument(
        "--tar-results",
        action="store_true",
        help="Package the results directory into results.tar.gz.",
    )
    args = parser.parse_args(argv)

    try:
        if not 10 <= args.line_width <= 60:
            raise ValueError("--line-width must be between 10 and 60.")
        rules = load_rules(args.rules)
        selected = _select_enzymes(args.enzymes, rules)

        text = _load_input_text(args.seq, args.fasta)
        records = _parse_input_records(text)
        if not records:
            raise ValueError("No FASTA records found in input.")

        chain_counts: dict[str, int] = {}
        safe_counts: dict[str, int] = {}
        merged_csv_parts: List[str] = []
        merged_records: List[dict] = []
        report_dir, csv_dir = _resolve_output_dirs(args.out)
        for accession, description, raw_seq in records:
            chain_id = _reserve_chain_id(accession, chain_counts)
            seq, meta = validate_sequence(raw_seq, strict=True)
            if not seq:
                raise ValueError(f"Empty sequence for record: {accession}")
            meta["accession"] = chain_id
            meta["description"] = description

            output_id = _reserve_safe_id(chain_id, safe_counts)
            sites_by_enzyme = find_cleavage_sites(seq, rules, selected)
            summary = build_summary(selected, sites_by_enzyme)
            parts = render_result_parts(seq, meta, selected, summary, args.line_width)

            html_out = report_dir / f"{output_id}_report.html"
            txt_base = html_out.with_suffix(".txt")

            write_result_parts(str(txt_base), parts)
            part3_csv = render_part3_csv(
                summary,
                chain_id=chain_id,
                include_header=not merged_csv_parts,
            )
            if part3_csv:
                merged_csv_parts.append(part3_csv)
            per_chain_csv = render_part3_csv(summary)
            if per_chain_csv:
                per_chain_path = csv_dir / f"{output_id}.csv"
                write_part3_csv(str(per_chain_path), per_chain_csv)
            enzyme_dir = Path("tmp") / "enzyme_txts" / output_id
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
            merged_records.append(
                {
                    "chain_id": chain_id,
                    "safe_id": output_id,
                    "seq": seq,
                    "meta": meta,
                    "summary": summary,
                    "part4_text": part4_text,
                }
            )

        merged_outputs: List[Path] = []
        if merged_csv_parts:
            merged_csv_text = "".join(merged_csv_parts)
            merged_csv_path = csv_dir / _ensure_csv_name(args.csv_name)
            write_part3_csv(str(merged_csv_path), merged_csv_text)
            merged_outputs.append(merged_csv_path)
        if merged_records:
            index_html = build_html_index_report(
                records=merged_records,
                line_width=args.line_width,
                title="PeptideCutter Report",
            )
            report_path = report_dir / MERGED_HTML_NAME
            report_path.write_text(index_html, encoding="utf-8")
            merged_outputs.append(report_path)
        if merged_outputs:
            _copy_to_cwd(merged_outputs)
        if args.tar_results:
            _tar_results(args.out)

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


def _parse_input_records(text: str) -> List[tuple[str, str, str]]:
    if _looks_like_fasta(text):
        records = parse_fasta_records(text, max_records=MAX_FASTA_RECORDS)
        if len(records) > MAX_FASTA_RECORDS:
            raise ValueError(
                f"FASTA contains more than {MAX_FASTA_RECORDS} records."
            )
        return records
    accession, description = extract_fasta_header(text)
    seq = parse_sequence(text)
    return [(accession, description, seq)]


def _looks_like_fasta(text: str) -> bool:
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        return line.startswith(">")
    return False


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


def _resolve_output_dirs(out_arg: str) -> tuple[Path, Path]:
    base_dir = Path(out_arg or ".")
    if base_dir.suffix:
        base_dir = base_dir.parent
    base_dir.mkdir(parents=True, exist_ok=True)
    results_dir = base_dir if base_dir.name == "results" else base_dir / "results"
    report_dir = results_dir / "report"
    csv_dir = results_dir / "csv"
    report_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)
    return report_dir, csv_dir


def _reserve_chain_id(seq_id: str, counts: dict[str, int]) -> str:
    base = seq_id.strip() if seq_id else "User_Sequence"
    if not base:
        base = "User_Sequence"
    if base not in counts:
        counts[base] = 0
        return base
    counts[base] += 1
    return f"{base}_dup{counts[base]}"


def _reserve_safe_id(seq_id: str, used: dict[str, int]) -> str:
    base = _sanitize_id(seq_id)
    if base not in used:
        used[base] = 0
        return base
    used[base] += 1
    return f"{base}_dup{used[base]}"


def _sanitize_id(value: str) -> str:
    if not value:
        return "User_Sequence"
    cleaned = value.strip()
    if not cleaned:
        return "User_Sequence"
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", cleaned)
    cleaned = cleaned.strip("._-")
    return cleaned or "User_Sequence"


def _ensure_csv_name(name: str) -> str:
    cleaned = (name or "").strip()
    if not cleaned:
        return MERGED_CSV_NAME
    if not cleaned.lower().endswith(".csv"):
        cleaned = f"{cleaned}.csv"
    return cleaned


def _copy_to_cwd(paths: List[Path]) -> None:
    cwd = Path.cwd()
    for path in paths:
        if not path.exists():
            continue
        dest = cwd / path.name
        try:
            if path.resolve() == dest.resolve():
                continue
        except FileNotFoundError:
            pass
        shutil.copy2(path, dest)


def _tar_results(out_arg: str) -> None:
    base_dir = Path(out_arg or ".")
    if base_dir.suffix:
        base_dir = base_dir.parent
    results_dir = base_dir if base_dir.name == "results" else base_dir / "results"
    if not results_dir.exists():
        return
    tar_path = results_dir.parent / "results.tar.gz"
    shutil.make_archive(str(tar_path.with_suffix("")), "gztar", root_dir=results_dir)


if __name__ == "__main__":
    raise SystemExit(main())
