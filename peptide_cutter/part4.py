from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


ENZYME_ABBR_MAP = {
    "Arg-C proteinase": "ArgC",
    "Asp-N endopeptidase": "AspN",
    "Asp-N endopeptidase + N-terminal Glu": "AspN+AspGluN",
    "BNPS-Skatole": "BNPS",
    # Chymotrypsin (two variants)
    "Chymotrypsin-high specificity (C-term to [FYW], not before P)": "Ch_hi",
    "Chymotrypsin-low specificity (C-term to [FYWML], not before P)": "Ch_lo",
    "Clostripain (Clostridiopeptidase B)": "Clost",
    "CNBr": "CNBr",
    "Formic acid": "HCOOH",
    "Glutamyl endopeptidase": "GluC",
    "Hydroxylamine (NH2OH)": "Hydro",
    "Iodosobenzoic acid": "Iodo",
    "NTCB (2-nitro-5-thiocyanobenzoic acid)": "NTCB",
    "LysC": "LysC",
    "LysN": "LysN",
    "Neutrophil elastase": "Elast",
    "Pepsin (pH1.3)": "Pn1.3",
    "Pepsin (pH>2)": "Pn2p",
    "Proline-endopeptidase": "Prol",
    "Proteinase K": "ProtK",
    "Staphylococcal peptidase I": "Staph",
    "Thermolysin": "Therm",
    "Thrombin": "Throm",
    "Trypsin": "Tryps",
    # Caspases
    "Caspase1": "Casp1",
    "Caspase2": "Casp2",
    "Caspase3": "Casp3",
    "Caspase4": "Casp4",
    "Caspase5": "Casp5",
    "Caspase6": "Casp6",
    "Caspase7": "Casp7",
    "Caspase8": "Casp8",
    "Caspase9": "Casp9",
    "Caspase10": "Casp10",
    # Others
    "Enterokinase": "EK",
    "Factor Xa": "FXa",
    "GranzymeB": "GzmB",
    "Tobacco etch virus protease": "TEV",
}


def normalize_name(name: str) -> str:
    name = (name or "").strip()
    if len(name) >= 2 and (
        (name[0] == '"' and name[-1] == '"')
        or (name[0] == "'" and name[-1] == "'")
    ):
        name = name[1:-1].strip()
    name = name.replace("[*]", "")
    name = re.sub(r"\s+", " ", name)
    return name


ENZYME_ABBR_MAP_NORM = {normalize_name(k): v for k, v in ENZYME_ABBR_MAP.items()}


def enzyme_abbr(name: str) -> str:
    n = normalize_name(name)

    if n.startswith("Chymotrypsin-high specificity"):
        return "Ch_hi"
    if n.startswith("Chymotrypsin-low specificity"):
        return "Ch_lo"

    m = re.fullmatch(r"Caspase\s*([0-9]+)", n, flags=re.IGNORECASE)
    if m:
        return f"Casp{int(m.group(1))}"

    if re.fullmatch(r"Granzyme\s*B", n, flags=re.IGNORECASE):
        return "GzmB"

    if (
        re.fullmatch(r"Factor\s*Xa", n, flags=re.IGNORECASE)
        or n.lower().replace(" ", "") == "factorxa"
    ):
        return "FXa"

    if n.lower() == "tobacco etch virus protease" or re.search(
        r"\btev\b", n, flags=re.IGNORECASE
    ):
        return "TEV"

    if n.lower().replace(" ", "") == "enterokinase":
        return "EK"

    if n in ENZYME_ABBR_MAP_NORM:
        return ENZYME_ABBR_MAP_NORM[n]

    raise ValueError(
        f"Unknown enzyme name: {name!r} (normalized: {n!r}). "
        "Please add it into ENZYME_ABBR_MAP."
    )


# ---------------------------
# FASTA reading (single record)
# ---------------------------

def read_single_fasta(path: str) -> Tuple[str, str]:
    recs: List[Tuple[str, str]] = []
    cur_id = None
    cur_seq: List[str] = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                if cur_id is not None:
                    seq = "".join(cur_seq)
                    seq = "".join(ch for ch in seq if ch.isalpha()).upper()
                    recs.append((cur_id, seq))
                cur_id = line[1:].strip().split()[0] or "SEQ"
                cur_seq = []
            else:
                cur_seq.append(line)

    if cur_id is not None:
        seq = "".join(cur_seq)
        seq = "".join(ch for ch in seq if ch.isalpha()).upper()
        recs.append((cur_id, seq))

    if not recs:
        raise ValueError(f"No FASTA record found in {path}")
    if len(recs) != 1:
        raise ValueError(
            f"FASTA must contain exactly 1 record, got {len(recs)}: {[r[0] for r in recs]}"
        )
    if not recs[0][1]:
        raise ValueError(f"Empty sequence in FASTA: {path}")

    return recs[0]


# ---------------------------
# CSV reading
# ---------------------------

def parse_positions(field: str) -> List[int]:
    if field is None:
        return []
    nums = re.findall(r"\d+", str(field))
    return [int(x) for x in nums]


def read_csv_rows(
    csv_path: str,
    enzyme_col: str = "Name of enzyme",
    pos_col: str = "Positions of cleavage sites",
) -> List[Tuple[str, List[int]]]:
    rows: List[Tuple[str, List[int]]] = []
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        if enzyme_col not in headers or pos_col not in headers:
            raise ValueError(
                f"CSV must have columns '{enzyme_col}' and '{pos_col}', got: {headers}"
            )

        for r in reader:
            name = normalize_name(r.get(enzyme_col, ""))
            pos = sorted(set(parse_positions(r.get(pos_col, ""))))
            if name:
                rows.append((name, pos))

    if not rows:
        raise ValueError(f"No valid rows in {csv_path}")
    return rows


# ---------------------------
# Rendering (per enzyme)
# ---------------------------

def number_line(start_pos: int, end_pos: int, left_pad: int, width: int) -> str:
    line = [" "] * (left_pad + width)
    s = str(start_pos)
    e = str(end_pos)

    for i, ch in enumerate(s):
        if left_pad + i < len(line):
            line[left_pad + i] = ch

    end_start = left_pad + width - len(e)
    for i, ch in enumerate(e):
        j = end_start + i
        if 0 <= j < len(line):
            line[j] = ch

    return "".join(line).rstrip()


def render_block_for_enzyme(
    seq: str,
    abbr: str,
    positions_in_block: List[int],
    block_start: int,
    block_size: int,
    left_pad: int,
) -> str:
    seq_len = len(seq)
    block_end = min(block_start + block_size - 1, seq_len)
    block_seq = seq[block_start - 1 : block_end]
    width = len(block_seq)

    idxs = sorted(
        {p - block_start for p in positions_in_block if block_start <= p <= block_end}
    )
    if not idxs:
        lines = []
        lines.append((" " * left_pad) + block_seq)
        lines.append(number_line(block_start, block_end, left_pad, width))
        return "\n".join(lines)

    label = abbr
    rows: List[List[str]] = []

    def ensure_row(r: int):
        while len(rows) <= r:
            rows.append([" "] * (left_pad + width))

    def can_place_on_row(r: int, bar_col: int) -> bool:
        ensure_row(r)
        label_start = bar_col - len(label)
        label_end = bar_col - 1

        for c in range(label_start, label_end + 1):
            if c < 0 or c >= left_pad + width:
                return False
            if rows[r][c] != " ":
                return False

        for rr in range(0, r + 1):
            ensure_row(rr)
            ch = rows[rr][bar_col]
            if ch not in (" ", "|"):
                return False

        return True

    def apply_place(r: int, bar_col: int):
        ensure_row(r)
        label_start = bar_col - len(label)

        for i, ch in enumerate(label):
            rows[r][label_start + i] = ch

        for rr in range(0, r + 1):
            if rows[rr][bar_col] == " ":
                rows[rr][bar_col] = "|"

    for idx in idxs:
        bar_col = left_pad + idx
        r = 0
        while True:
            if can_place_on_row(r, bar_col):
                apply_place(r, bar_col)
                break
            r += 1

    out_lines = []
    for r in range(len(rows) - 1, -1, -1):
        out_lines.append("".join(rows[r]).rstrip())

    out_lines.append((" " * left_pad) + block_seq)
    out_lines.append(number_line(block_start, block_end, left_pad, width))
    return "\n".join(out_lines)


def safe_filename(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "output"


def write_one_enzyme_txt(
    out_dir: Path,
    seq_id: str,
    seq: str,
    enzyme_name: str,
    positions: List[int],
    block_size: int,
    enzyme_col: str,
    pos_col: str,
    used_names: Dict[str, int],
) -> Path:
    abbr = enzyme_abbr(enzyme_name)

    base = safe_filename(abbr)
    if base not in used_names:
        used_names[base] = 1
        filename = f"{base}.txt"
    else:
        used_names[base] += 1
        filename = f"{base}_{used_names[base]}.txt"

    path = out_dir / filename
    pos = sorted({p for p in positions if 1 <= p <= len(seq)})
    left_pad = len(abbr) + 2

    lines: List[str] = []
    lines.append(f">{seq_id}")
    lines.append(f"# Enzyme: {enzyme_name}")
    lines.append(f"# Abbr: {abbr}")
    lines.append(f"# CSV columns: {enzyme_col} / {pos_col}")
    lines.append("")

    for block_start in range(1, len(seq) + 1, block_size):
        lines.append(
            render_block_for_enzyme(
                seq=seq,
                abbr=abbr,
                positions_in_block=pos,
                block_start=block_start,
                block_size=block_size,
                left_pad=left_pad,
            )
        )
        lines.append("")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def generate_enzyme_txts(
    rows: List[Tuple[str, List[int]]],
    seq_id: str,
    seq: str,
    out_dir: Path,
    block_size: int = 60,
    enzyme_col: str = "Name of enzyme",
    pos_col: str = "Positions of cleavage sites",
) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    used_names: Dict[str, int] = {}
    outputs: List[Path] = []
    for enzyme_name, positions in rows:
        outputs.append(
            write_one_enzyme_txt(
                out_dir=out_dir,
                seq_id=seq_id,
                seq=seq,
                enzyme_name=enzyme_name,
                positions=positions,
                block_size=block_size,
                enzyme_col=enzyme_col,
                pos_col=pos_col,
                used_names=used_names,
            )
        )
    return outputs


def generate_enzyme_txts_from_csv(
    csv_path: str,
    fasta_path: str,
    out_dir: Path,
    block_size: int = 60,
    enzyme_col: str = "Name of enzyme",
    pos_col: str = "Positions of cleavage sites",
) -> List[Path]:
    seq_id, seq = read_single_fasta(fasta_path)
    rows = read_csv_rows(csv_path, enzyme_col=enzyme_col, pos_col=pos_col)
    return generate_enzyme_txts(
        rows=rows,
        seq_id=seq_id,
        seq=seq,
        out_dir=out_dir,
        block_size=block_size,
        enzyme_col=enzyme_col,
        pos_col=pos_col,
    )


SEQ_RE = re.compile(r"^\s*[A-Z]{10,}\s*$")
NUM_RE = re.compile(r"\d+")


def normalize_abbr(abbr: str) -> str:
    abbr = (abbr or "").strip()
    abbr = abbr.replace("+", "_")
    abbr = re.sub(r"\s+", "", abbr)
    abbr = re.sub(r"[^A-Za-z0-9._-]+", "_", abbr)
    abbr = re.sub(r"_+", "_", abbr).strip("_")
    return abbr or "UNK"


def list_txt(indir: Path) -> List[Path]:
    files = [p for p in indir.iterdir() if p.is_file() and p.suffix.lower() == ".txt"]
    files.sort()
    return files


def parse_positions_from_enzyme_txt(
    path: Path,
) -> Tuple[str, Set[int], Optional[str], List[Tuple[int, str]]]:
    abbr = path.stem
    seq_id = None
    positions: Set[int] = set()
    blocks: List[Tuple[int, str]] = []

    lines = path.read_text(encoding="utf-8").splitlines()

    for ln in lines:
        if ln.startswith(">"):
            seq_id = ln[1:].strip()
            break

    for ln in lines:
        if ln.startswith("# Abbr:"):
            abbr = ln.split(":", 1)[1].strip()
            break

    abbr = normalize_abbr(abbr)

    i = 0
    n = len(lines)
    while i < n:
        if SEQ_RE.match(lines[i]) and not lines[i].lstrip().startswith("#"):
            seq_line = lines[i]
            seq_str = seq_line.strip()
            left_pad = len(seq_line) - len(seq_line.lstrip())
            width = len(seq_str)

            if i + 1 >= n:
                break
            num_line = lines[i + 1]
            nums = NUM_RE.findall(num_line)
            if len(nums) < 2:
                i += 1
                continue
            block_start = int(nums[0])
            block_end = int(nums[-1])

            k = i - 1
            while k >= 0 and lines[k].strip() != "":
                k -= 1
            track_lines = lines[k + 1 : i]

            for tl in track_lines:
                for col, ch in enumerate(tl):
                    if ch == "|":
                        idx = col - left_pad
                        if 0 <= idx < width:
                            positions.add(block_start + idx)

            blocks.append((block_start, seq_str))
            i += 2
            continue

        i += 1

    return abbr, positions, seq_id, blocks


def reconstruct_seq_from_blocks(blocks: List[Tuple[int, str]]) -> str:
    if not blocks:
        return ""
    blocks_sorted = sorted(blocks, key=lambda x: x[0])
    return "".join(s for _, s in blocks_sorted)


def render_block_by_positions(
    block_seq: str,
    block_start: int,
    events: List[Tuple[int, str]],
    left_pad: int,
) -> str:
    width = len(block_seq)
    rows: List[List[str]] = []

    def ensure_row(r: int):
        while len(rows) <= r:
            rows.append([" "] * (left_pad + width))

    def can_place(label: str, r: int, bar_col: int) -> bool:
        ensure_row(r)
        label_start = bar_col - len(label)
        label_end = bar_col - 1
        if label_start < 0:
            return False

        for c in range(label_start, label_end + 1):
            if c < 0 or c >= left_pad + width:
                return False
            if rows[r][c] != " ":
                return False

        for rr in range(0, r + 1):
            ensure_row(rr)
            ch = rows[rr][bar_col]
            if ch not in (" ", "|"):
                return False
        return True

    def apply(label: str, r: int, bar_col: int):
        ensure_row(r)
        label_start = bar_col - len(label)

        for i, ch in enumerate(label):
            rows[r][label_start + i] = ch

        for rr in range(0, r + 1):
            ensure_row(rr)
            if rows[rr][bar_col] == " ":
                rows[rr][bar_col] = "|"

    for idx, (abs_pos, label) in enumerate(events):
        in_block_idx = abs_pos - block_start
        if not (0 <= in_block_idx < width):
            continue
        bar_col = left_pad + in_block_idx

        r = idx
        while True:
            if can_place(label, r, bar_col):
                apply(label, r, bar_col)
                break
            r += 1

    out_lines = []
    for r in range(len(rows) - 1, -1, -1):
        out_lines.append("".join(rows[r]).rstrip())

    out_lines.append((" " * left_pad) + block_seq)
    out_lines.append(number_line(block_start, block_start + width - 1, left_pad, width))
    return "\n".join(out_lines)


def merge_enzyme_txts(
    indir: Path,
    out_path: Path,
    fasta_path: Optional[str] = None,
    block_size: int = 80,
) -> Path:
    txt_files = list_txt(indir)
    if not txt_files:
        raise ValueError(f"No .txt files found in: {indir}")

    abbr_to_positions: Dict[str, Set[int]] = {}
    enzyme_order: List[str] = []
    seq_id_ref = None
    blocks_ref: List[Tuple[int, str]] = []

    for fp in txt_files:
        abbr, pos_set, seq_id, blocks = parse_positions_from_enzyme_txt(fp)
        abbr_to_positions[abbr] = pos_set
        enzyme_order.append(abbr)
        if seq_id_ref is None and seq_id:
            seq_id_ref = seq_id
        if blocks and not blocks_ref:
            blocks_ref = blocks

    if fasta_path:
        seq_id_ref, seq = read_single_fasta(fasta_path)
    else:
        seq = reconstruct_seq_from_blocks(blocks_ref)

    if not seq:
        raise ValueError("Failed to determine sequence for merged Part 4 output.")

    seq_len = len(seq)
    pos_to_abbrs: Dict[int, Set[str]] = {}
    for abbr, pos_set in abbr_to_positions.items():
        for p in pos_set:
            if 1 <= p <= seq_len:
                pos_to_abbrs.setdefault(p, set()).add(abbr)

    order_index = {a: i for i, a in enumerate(enzyme_order)}

    def join_abbrs(abbrs: Set[str]) -> str:
        items = sorted(abbrs, key=lambda x: (order_index.get(x, 10**9), x))
        return "_".join(items)

    pos_to_label: Dict[int, str] = {p: join_abbrs(s) for p, s in pos_to_abbrs.items()}
    max_label_len = max((len(lbl) for lbl in pos_to_label.values()), default=0)
    left_pad = max_label_len + 2

    out_lines: List[str] = []
    out_lines.append(
        "Cleavage sites of the chosen enzymes and chemicals mapped onto your sequence:"
    )
    out_lines.append("")
    for block_start in range(1, seq_len + 1, block_size):
        block_end = min(block_start + block_size - 1, seq_len)
        block_seq = seq[block_start - 1 : block_end]

        positions = [
            p for p in sorted(pos_to_label.keys()) if block_start <= p <= block_end
        ]
        events = [(p, pos_to_label[p]) for p in positions]

        out_lines.append(
            render_block_by_positions(
                block_seq=block_seq,
                block_start=block_start,
                events=events,
                left_pad=left_pad,
            )
        )
        out_lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out_lines).rstrip() + "\n", encoding="utf-8")
    return out_path
