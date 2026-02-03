#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

from peptide_cutter.part4 import (
    generate_enzyme_txts,
    read_csv_rows,
    read_single_fasta,
)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate one TXT per enzyme/chemical from result.csv + a single-seq FASTA."
    )
    ap.add_argument("--csv", default="result.csv", help="Input CSV path.")
    ap.add_argument("--fasta", required=True, help="Input FASTA path (single sequence).")
    ap.add_argument(
        "--outdir",
        default="tmp/enzyme_txts",
        help="Output directory for per-enzyme txts.",
    )
    ap.add_argument(
        "--block-size", type=int, default=60, help="Residues per block (default 60)."
    )
    ap.add_argument(
        "--enzyme-col", default="Name of enzyme", help="Column name for enzyme."
    )
    ap.add_argument(
        "--pos-col",
        default="Positions of cleavage sites",
        help="Column name for cleavage positions.",
    )
    args = ap.parse_args()

    seq_id, seq = read_single_fasta(args.fasta)
    rows = read_csv_rows(args.csv, enzyme_col=args.enzyme_col, pos_col=args.pos_col)

    out_dir = Path(args.outdir)
    outputs = generate_enzyme_txts(
        rows=rows,
        seq_id=seq_id,
        seq=seq,
        out_dir=out_dir,
        block_size=args.block_size,
        enzyme_col=args.enzyme_col,
        pos_col=args.pos_col,
    )

    for (enzyme_name, _), out_path in zip(rows, outputs):
        print(f"[OK] {enzyme_name} -> {out_path}")

    print(f"\nDone. Generated {len(outputs)} txt files in: {out_dir}")


if __name__ == "__main__":
    main()
