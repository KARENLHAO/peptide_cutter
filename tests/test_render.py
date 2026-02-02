from pathlib import Path

from peptide_cutter.aggregate import build_summary
from peptide_cutter.engine import find_cleavage_sites
from peptide_cutter.render import render_result_txt
from peptide_cutter.rules import load_rules


def _rules():
    path = Path(__file__).parent / "fixtures" / "rules.json"
    return load_rules(str(path))


def _meta():
    return {
        "accession": "User_Sequence",
        "description": "N/A",
        "replacements": {},
    }


def test_render_sections_and_do_not_cut():
    rules = _rules()
    seq = "AKR"
    selected = ["Testase", "Twinase"]
    sites = find_cleavage_sites(seq, rules, selected)
    summary = build_summary(selected, sites)
    content = render_result_txt(seq, _meta(), selected, summary, line_width=60)

    idx1 = content.find("Part 1")
    idx2 = content.find("Part 2")
    idx3 = content.find("Part 3")
    idx4 = content.find("Part 4")
    assert 0 <= idx1 < idx2 < idx3 < idx4
    assert "The selected enzymes do not cut:" in content


def test_sequence_map_alignment_and_merge():
    rules = _rules()
    seq = "AKRRAAQQQQ"
    selected = ["Twinase", "Twinase2"]
    sites = find_cleavage_sites(seq, rules, selected)
    summary = build_summary(selected, sites)
    content = render_result_txt(seq, _meta(), selected, summary, line_width=10)

    assert "Twinase_Twinase2" in content

    blocks = content.split("```")
    map_block = blocks[-2].strip()
    lines = map_block.splitlines()
    label_width = max(len("Twinase_Twinase2"), len("Ruler"), len("Sequence"))
    marker_line = next(line for line in lines if line.startswith("Twinase_Twinase2"))
    marker = marker_line[label_width + 1 :]
    assert len(marker) == 10


def test_render_golden_fragment():
    rules = _rules()
    seq = "AKRRAAQQQQ"
    selected = ["Testase", "Twinase", "Twinase2"]
    sites = find_cleavage_sites(seq, rules, selected)
    summary = build_summary(selected, sites)
    content = render_result_txt(seq, _meta(), selected, summary, line_width=10)

    expected = (
        "## Part 3: Cleavage site table\n"
        "| Name of enzyme | No. of cleavages | Positions of cleavage sites |\n"
        "| --- | --- | --- |\n"
        "| Testase | 1 | 2 |\n"
        "| Twinase | 2 | 3, 4 |\n"
        "| Twinase2 | 2 | 3, 4 |\n"
    )
    assert expected in content
