> Note: If you find a bug or notice an error in the cleavage rules during use, please feel free to submit an issue. I will fix and update it as soon as possible.

# Peptide-Cutter
Peptide-Cutter is a local, lightweight tool for predicting protease/chemical cleavage sites in protein sequences. It reads raw or FASTA input, applies curated cleavage rules, and generates a clean HTML report plus a CSV table of cutting points. The report is organized into four sections: input sequence display, selected enzymes, cutting table, and cleavage mapping.


## Installation

```
pip install -e .
```

## CLI Usage

Raw sequence input:

```
peptide-cutter --seq "MKWVTFISLLFLFSSAYSRGVFRRDTHKSEIAHRFKDLGE" \
  --enzymes "Tryps;Ch_hi" \
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
- `--fasta`: FASTA file path. Multi-FASTA is supported (up to 10,000 records).
- `--enzymes`: enzyme names/abbreviations or `all`. Multiple enzymes can be
  provided as a semicolon-separated string, e.g. `"Casp1;Tryps;FXa"`.
- `--out`: base output directory (default `.`). A `results/` folder is created
  under this directory with `report/` and `csv/` subfolders.
- `--line-width`: line width for sequence display and Part 4 blocks (10-60, default 60).
- `--cleanup-tmp`: remove the `tmp/` directory after the run completes.
- `--tar-results`: package the `results/` directory into `results.tar.gz`.

## Illegal Characters

Any illegal characters (including `B`, `J`, `X`, `Z`, or other non-standard letters) cause an error. The error message includes the illegal character(s).

## Output Files

输出All_in_One.csv，内容为输入序列中的切割点表，内容如下：
| Chain ID | Name of enzyme                                                 | No. of cleavages | Positions of cleavage sites       |
| -------- | -------------------------------------------------------------- | ---------------: | --------------------------------- |
| seq_1    | Arg-C proteinase                                               |                1 | 14                                |
| seq_1    | Asp-N endopeptidase                                            |                1 | 2                                 |
| seq_1    | Asp-N endopeptidase + N-terminal Glu                           |                2 | 2, 6                              |
| seq_1    | BNPS-Skatole                                                   |                1 | 4                                 |
| seq_1    | Chymotrypsin-high specificity (C-term to [FYW], not before P)  |                1 | 4                                 |
| seq_1    | Chymotrypsin-low specificity (C-term to [FYWML], not before P) |                2 | 4, 6                              |
| seq_1    | Clostripain (Clostridiopeptidase B)                            |                1 | 14                                |
| seq_1    | Formic acid                                                    |                1 | 3                                 |
| seq_1    | Glutamyl endopeptidase                                         |                1 | 7                                 |
| seq_1    | Iodosobenzoic acid                                             |                1 | 4                                 |
| seq_1    | LysC                                                           |                1 | 1                                 |
| seq_1    | Neutrophil elastase                                            |                1 | 13                                |
| seq_1    | NTCB (2-nitro-5-thiocyanobenzoic acid)                         |                1 | 4                                 |
| seq_1    | Pepsin (pH>2)                                                  |                1 | 4                                 |
| seq_1    | Proteinase K                                                   |                5 | 2, 4, 7, 8, 13                    |
| seq_1    | Staphylococcal peptidase I                                     |                1 | 7                                 |
| seq_1    | Thermolysin                                                    |                2 | 1, 12                             |
| seq_1    | Trypsin                                                        |                1 | 1                                 |
| seq_2    | Asp-N endopeptidase + N-terminal Glu                           |                3 | 2, 11, 17                         |
| seq_2    | BNPS-Skatole                                                   |                2 | 2, 16                             |
| seq_2    | Chymotrypsin-high specificity (C-term to [FYW], not before P)  |                5 | 2, 5, 11, 16, 17                  |
| seq_2    | Chymotrypsin-low specificity (C-term to [FYWML], not before P) |                9 | 1, 2, 5, 6, 9, 10, 11, 16, 17     |
| seq_2    | CNBr                                                           |                1 | 6                                 |
| seq_2    | Glutamyl endopeptidase                                         |                3 | 3, 12, 18                         |
| seq_2    | Iodosobenzoic acid                                             |                2 | 2, 16                             |
| seq_2    | LysC                                                           |                2 | 13, 15                            |
| seq_2    | LysN                                                           |                2 | 12, 14                            |
| seq_2    | Neutrophil elastase                                            |                1 | 4                                 |
| seq_2    | NTCB (2-nitro-5-thiocyanobenzoic acid)                         |                1 | 13                                |
| seq_2    | Pepsin (pH1.3)                                                 |                3 | 4, 5, 10                          |
| seq_2    | Pepsin (pH>2)                                                  |                4 | 4, 5, 10, 16                      |
| seq_2    | Proteinase K                                                   |               10 | 1, 2, 3, 4, 5, 11, 12, 16, 17, 18 |
| seq_2    | Staphylococcal peptidase I                                     |                3 | 3, 12, 18                         |
| seq_2    | Thermolysin                                                    |                3 | 4, 5, 10                          |
| seq_2    | Trypsin                                                        |                2 | 13, 15                            |


说明：
| 字段                        | 说明                                                                                                                                            |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Chain ID                    | 序列/链的标识符。  当`Chain ID`出现多次重复的情况时，`Chain ID`后会被添加上_dup1、如：A_dup1，`1`对应就是重复的次数。                           |
| Name of enzyme              | 蛋白酶/化学试剂名称，用于标识采用哪一种切割规则（例如 `Arg-C proteinase`、`Asp-N endopeptidase`、`BNPS-Skatole`、`CNBr` 等）。                  |
| No. of cleavages            | 该酶/试剂在对应 `Chain ID` 的序列上预测/统计到的切割次数（= 切割位点数量）。通常应与 `Positions of cleavage sites` 中列出的位点个数一致。       |
| Positions of cleavage sites | 切割位点在序列中的位置编号列表（以 1 为起点的序列坐标）。多个位点用逗号 + 空格分隔（例如 `2, 4, 7`）；若只有一个位点则为单个数字（例如 `14`）。 |



输出All_in_One.html，内容将包含所有链的切割信息，展出如下：  
[All_in_One.html](https://karenlhao.github.io/peptide_cutter/)


输出results.tar.gz，包含所有链的单独csv以及HTML报告结果。

## Enzyme Abbreviations

Use these abbreviations with `--enzymes` (quote the string when using `;` in a shell):

| Abbr         | Enzyme / Chemical                                              |
| ------------ | -------------------------------------------------------------- |
| ArgC         | Arg-C proteinase                                               |
| AspN         | Asp-N endopeptidase                                            |
| AspN+AspGluN | Asp-N endopeptidase + N-terminal Glu                           |
| BNPS         | BNPS-Skatole                                                   |
| Ch_hi        | Chymotrypsin-high specificity (C-term to [FYW], not before P)  |
| Ch_lo        | Chymotrypsin-low specificity (C-term to [FYWML], not before P) |
| Clost        | Clostripain (Clostridiopeptidase B)                            |
| CNBr         | CNBr                                                           |
| HCOOH        | Formic acid                                                    |
| GluC         | Glutamyl endopeptidase                                         |
| Hydro        | Hydroxylamine (NH2OH)                                          |
| Iodo         | Iodosobenzoic acid                                             |
| NTCB         | NTCB (2-nitro-5-thiocyanobenzoic acid)                         |
| LysC         | LysC                                                           |
| LysN         | LysN                                                           |
| Elast        | Neutrophil elastase                                            |
| Pn1.3        | Pepsin (pH1.3)                                                 |
| Pn2p         | Pepsin (pH>2)                                                  |
| Prol         | Proline-endopeptidase                                          |
| ProtK        | Proteinase K                                                   |
| Staph        | Staphylococcal peptidase I                                     |
| Therm        | Thermolysin                                                    |
| Throm        | Thrombin                                                       |
| Tryps        | Trypsin                                                        |
| Casp1        | Caspase1                                                       |
| Casp2        | Caspase2                                                       |
| Casp3        | Caspase3                                                       |
| Casp4        | Caspase4                                                       |
| Casp5        | Caspase5                                                       |
| Casp6        | Caspase6                                                       |
| Casp7        | Caspase7                                                       |
| Casp8        | Caspase8                                                       |
| Casp9        | Caspase9                                                       |
| Casp10       | Caspase10                                                      |
| EK           | Enterokinase                                                   |
| FXa          | Factor Xa                                                      |
| GzmB         | GranzymeB                                                      |
| TEV          | Tobacco etch virus protease                                    |


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
