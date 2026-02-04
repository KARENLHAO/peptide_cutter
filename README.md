# PeptideCutter

> Note: This project is inspired by the ExPASy lab’s PeptideCutter and implemented based on public information and our own understanding. No source code was obtained through illegal or unauthorized means. Reference: https://web.expasy.org/peptide_cutter/

PeptideCutter predicts potential cleavage sites for protein sequences under multiple proteases/chemicals using a local `peptide_cutter/cleavage_rules.json` file and writes parts 1-3 into `tmp/parts_txts/`, plus per-enzyme and merged Part 4 outputs into `tmp/enzyme_txts/` and `tmp/parts_txts/`.

## Installation

```
pip install -e .
```

## CLI Usage

Raw sequence input:

```
peptide-cutter --seq "MKWVTFISLLFLFSSAYSRGVFRRDTHKSEIAHRFKDLGE" \
  --enzymes Trypsin Chymotrypsin \
  --out .
```

FASTA input:

```
peptide-cutter --fasta ./G3P_HUMAM_P04406.fasta \
  --enzymes all \
  --out .
```

Line width for sequence display (10-60):

```
peptide-cutter --seq "ACDEFGHIKLMNPQRSTVWY" --enzymes all --line-width 40
```

clean up the tmp directory:

```
peptide-cutter --seq "ACDEFGHIK" --enzymes all --out . --cleanup-tmp
```

## Parameters

- `--seq`: raw or FASTA text input.
- `--fasta`: FASTA file path.
- `--enzymes`: enzyme names or `all`.
- `--out`: output HTML path or directory (default `.`). If a directory is provided (e.g. `.`),
  the tool writes `report.html` inside it. CSV is written alongside the HTML as `result.csv`.
- `--line-width`: line width for sequence display and Part 4 blocks (10-60, default 60).
- `--prob`: probability [0-1] to keep cleavage sites for the selected enzyme (default 1.0).
- `--prob-target`: which enzyme `--prob` applies to (`trypsin` or `chymotrypsin`, default `trypsin`).
- `--cleanup-tmp`: remove the `tmp/` directory after the run completes.

Note: when `--prob` is less than 1.0, the selected enzyme’s cleavage sites are randomly sampled each run.

## Illegal Characters

Any illegal characters (including `B`, `J`, `X`, `Z`, or other non-standard letters) cause an error. The error message includes the illegal character(s).

## Output Files

- CSV (`result.csv`): Table of cutting points in the sequence.
- HTML (`report.html`): 4 parts
1. Input Sequence Display
2. Selected Enzymes
3. Table of cutting points in the sequence
4. The mapping diagram of the cleavage sites of the selected enzymes and chemical substances on your sequence


## Development

Run tests:

```
pytest
```

## Package Structure

```
peptide_cutter/
  __init__.py
  __main__.py
  aggregate.py
  cleavage_rules.json
  cli.py
  engine.py
  render.py
  rules.py
  sequence.py
  utils/
    __init__.py
    html_report.py
    make_enzyme_txts.py
    merge_part4_txts.py
```

### File Notes

- `__init__.py`: package metadata.
- `__main__.py`: module entrypoint (`python -m peptide_cutter`).
- `aggregate.py`: summarize cleavage results.
- `cleavage_rules.json`: enzyme/chemical cleavage rules.
- `cli.py`: CLI parsing and orchestration.
- `engine.py`: cleavage site search logic.
- `render.py`: text/CSV rendering helpers.
- `rules.py`: rules loader and normalization.
- `sequence.py`: FASTA parsing and sequence validation.
- `utils/html_report.py`: HTML report renderer.
- `utils/make_enzyme_txts.py`: tool to generate per-enzyme txt files.
- `utils/merge_part4_txts.py`: Part 4 generation and merge utility.
