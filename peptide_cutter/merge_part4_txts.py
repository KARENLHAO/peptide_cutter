#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from pathlib import Path

from peptide_cutter.part4 import merge_enzyme_txts


def resolve_output_path(out_arg: str) -> Path:
    out_arg = out_arg or "result_part4.txt"
    if out_arg.endswith(os.sep) or os.path.isdir(out_arg):
        os.makedirs(out_arg, exist_ok=True)
        return Path(out_arg) / "result_part4.txt"
    parent = os.path.dirname(out_arg) or "."
    os.makedirs(parent, exist_ok=True)
    return Path(out_arg)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Merge per-enzyme txts into one result_part4.txt (per-position combo labels + staircase tracks)."
    )
    ap.add_argument(
        "--indir", required=True, help="Directory containing per-enzyme *.txt files."
    )
    ap.add_argument(
        "--out",
        default="tmp/parts_txts/result_part4.txt",
        help="Output merged txt path.",
    )
    ap.add_argument(
        "--fasta",
        default=None,
        help="Optional FASTA (single record). If provided, use it for sequence.",
    )
    ap.add_argument(
        "--block-size", type=int, default=60, help="Residues per block (default: 60)."
    )
    args = ap.parse_args()

    out_path = resolve_output_path(args.out)
    merge_enzyme_txts(
        indir=Path(args.indir),
        out_path=out_path,
        fasta_path=args.fasta,
        block_size=args.block_size,
    )

    print(f"[OK] merged -> {out_path}")
    print(f"     indir: {args.indir}")
    print(f"     block_size: {args.block_size}")


if __name__ == "__main__":
    main()
