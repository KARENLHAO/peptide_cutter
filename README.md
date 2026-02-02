# PeptideCutter

PeptideCutter predicts potential cleavage sites for protein sequences under multiple proteases/chemicals using a local `cleavage_rules.json` file and writes a Markdown report to `result.txt`.

## Installation

```
pip install -e .
```

## CLI Usage

Raw sequence input:

```
peptide-cutter --seq "MKWVTFISLLFLFSSAYSRGVFRRDTHKSEIAHRFKDLGE" \
  --enzymes Trypsin Chymotrypsin \
  --rules ./cleavage_rules.json \
  --out ./result.txt
```

Module invocation:

```
python -m peptide_cutter --seq "ACDEFGHIK" --enzymes all
```

FASTA input:

```
peptide-cutter --fasta ./G3P_HUMAM_P04406.fasta \
  --enzymes all \
  --rules ./cleavage_rules.json \
  --out ./result.txt
```

Line width for sequence map (10-60):

```
peptide-cutter --seq "ACDEFGHIKLMNPQRSTVWY" --enzymes all --line-width 40
```

## Parameters

- `--seq`: raw or FASTA text input.
- `--fasta`: FASTA file path.
- `--rules`: rules JSON path (default `./cleavage_rules.json`).
- `--enzymes`: enzyme names or `all`.
- `--out`: output file path (default `./result.txt`).
- `--line-width`: sequence map window width (10-60, default 60).
- `--replace`: explicit replacement mapping, repeatable, e.g. `--replace B=D --replace Z=E`.

## Illegal Characters and Replacement Rules

By default, any illegal characters (including `B`, `J`, `X`, `Z`, or other non-standard letters) cause an error. The error message includes the illegal characters and their 1-based positions.

Replacement guidance:

- `B` (Asx) -> `D` or `N`
- `Z` (Glx) -> `E` or `Q`
- `J` (Xle) -> `I` or `L`
- `X` must be explicitly replaced to a concrete amino acid

Only explicitly provided replacements are applied. When replacements are applied, the report notes the mapping and counts in Part 1.

## Output (`result.txt`) Structure

The report contains four fixed parts in order:

1. Input sequence display (identifier, description, length, 60 aa/line with numbering)
2. Selected cleavage enzymes and chemicals list (alphabetical)
3. Cleavage site table + `The selected enzymes do not cut: ...`
4. Sequence map in a Markdown code block, with merged identical maps using `_`

## Development

Run tests:

```
pytest
```

## TODO

- Optional future integration with UniProt/SWISS-PROT/TrEMBL online retrieval.
