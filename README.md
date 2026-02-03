# PeptideCutter

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
  --rules ./peptide_cutter/cleavage_rules.json \
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
  --rules ./peptide_cutter/cleavage_rules.json \
  --out ./result.txt
```

Line width for sequence display (10-60):

```
peptide-cutter --seq "ACDEFGHIKLMNPQRSTVWY" --enzymes all --line-width 40
```

## Parameters

- `--seq`: raw or FASTA text input.
- `--fasta`: FASTA file path.
- `--enzymes`: enzyme names or `all`.
- `--line-width`: line width for sequence display and Part 4 blocks (10-60, default 60).
- `--prob`: probability [0-1] to keep cleavage sites for the selected enzyme (default 1.0).
- `--prob-target`: which enzyme `--prob` applies to (`trypsin` or `chymotrypsin`, default `trypsin`).

Note: when `--prob` is less than 1.0, the selected enzyme’s cleavage sites are randomly sampled each run.

## Illegal Characters

Any illegal characters (including `B`, `J`, `X`, `Z`, or other non-standard letters) cause an error. The error message includes the illegal character(s).

## Output Files

The report is written into three text files in `tmp/parts_txts/`. `--out` specifies the
base filename (default `./result.txt`), and the tool writes:

1. `tmp/parts_txts/result_part1.txt`: Input sequence display (identifier, description, length, line width from `--line-width`)
2. `tmp/parts_txts/result_part2.txt`: Selected cleavage enzymes and chemicals list (alphabetical)
3. `tmp/parts_txts/result_part3.txt`: Cleavage site table + `The selected enzymes do not cut: ...`
4. `./result.csv`: CSV version of the Part 3 cleavage site table (written to current directory)
5. `tmp/enzyme_txts/*.txt`: Per-enzyme cleavage tracks (one file per enzyme/chemical)
6. `tmp/parts_txts/result_part4.txt`: Merged Part 4 track file

## Cleavage Rules Reference

### **Comprehensive Protease and Chemical Cleavage Rules**

### Cleavage rules (updated)

| Enzyme / Chemical Name | P4 | P3 | P2 | P1 | P1' | P2' |
| --- | --- | --- | --- | --- | --- | --- |
| Arg-C proteinase | - | - | - | R | - | - |
| Asp-N endopeptidase | - | - | - | - | D | - |
| Asp-N endopeptidase + N-terminal Glu | - | - | - | - | D or E | - |
| BNPS-Skatole | - | - | - | W | - | - |
| Caspase 1 | F,W,Y or L | - | H,A or T | D | not P,E,D,Q,K or R | - |
| Caspase 2 | D | V | A | D | not P,E,D,Q,K or R | - |
| Caspase 3 | D | M | Q | D | not P,E,D,Q,K or R | - |
| Caspase 4 | L | E | V | D | not P,E,D,Q,K or R | - |
| Caspase 5 | L or W | E | H | D | - | - |
| Caspase 6 | V | E | H or I | D | not P,E,D,Q,K or R | - |
| Caspase 7 | D | E | V | D | not P,E,D,Q,K or R | - |
| Caspase 8 | I or L | E | T | D | not P,E,D,Q,K or R | - |
| Caspase 9 | L | E | H | D | - | - |
| Caspase 10 | I | E | A | D | - | - |
| Chymotrypsin-high specificity (C-term to [FYW], not before P) | - | - | - | F or Y | not P | - |
|  | - | - | - | W | not P | - |
| Chymotrypsin-low specificity (C-term to [FYWML], not before P) | - | - | - |  F,L or Y  | not M or P  | - |
|  | - | - | - | W | not M or P | - |
|  | - | - | - | M | not P or Y | - |
|  | - | - | - | H | not D,M,P or W | - |
| Clostripain (Clostridiopeptidase B)| - | - | - | R | - | - |
| CNBr | - | - | - | M | - | - |
| Enterokinase | D or E | D or E | D or E | K | - | - |
| Factor Xa | A,F,G,I,L,T,V or M | D or E | G | R | - | - |
| Formic acid | - | - | - | D | - | - |
| Glutamyl endopeptidase | - | - | - | E | - | - |
| GranzymeB | I | E | P | D | - | - |
| Hydroxylamine  (NH2OH) | - | - | - | N | G | - |
| Iodosobenzoic acid | - | - | - | W | - | - |
| LysC | - | - | - | K | - | - |
| LysN | - | - | - | - | K | - |
| Neutrophil elastase | - | - | - | A or V | - | - |
| NTCB (2-nitro-5-thiocyanobenzoic acid) | - | - | - | - | C | - |
| Pepsin (pH1.3) | - | not H,K or R | not P | not R | F or L | not P |
|  | - | not H,K or R | not P | F or L | - | not P |
| Pepsin (pH>2) | - | not H,K or R | not P | not R | F,L,W or Y | not P |
|  | - | not H,K or R | not P | F,L,W or Y | - | not P |
| Proline-endopeptidase[*]  | - | - | H,K or R | P | not P | - |
| Proteinase K | - | - | - | A,E,F,I,L,T,V,W or Y | - | - |
| Staphylococcal peptidase I | - | - | not E | E | - | - |
| Tobacco etch virus protease | -  | Y  | -  | Q  | G or S | -   |
| Thermolysin | - | - | - | not D or E | A,F,I,L,M or V | not P |
| Thrombin | - | - | G | R | G | - |
| | A,F,G,I,L,T,V or M | A,F,G,I,L,T,V,W or R | P | R | not D or E | not D or E |
| Trypsin | - | - | - | K or R | not P | - |
|  | - | - | W | K | not P | - |
|  | - | - | M | R | not P | - |

[*] NOTE: Proline-endopeptidase was reported to cleave only substrates whose sequences do not exceed 30 amino acids. An unusual beta-propeller domain regulates proteolysis: see Fulop et al., 1998.


---

### **Trypsin Exceptions (Blocking Rules)**

| Enzyme Name | P4 | P3 | P2 | P1 | P1' | P2' |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Trypsin | - | - | C or D | K | D | - |
| Trypsin | - | - | C | K | H or Y | - |
| Trypsin | - | - | C | R | K | - |
| Trypsin | - | - | R | R | H or R | - |

## Development

Run tests:

```
pytest
```

## TODO

- Optional future integration with UniProt/SWISS-PROT/TrEMBL online retrieval.
