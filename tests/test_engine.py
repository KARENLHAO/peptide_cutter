from pathlib import Path

from peptide_cutter.engine import find_cleavage_sites
from peptide_cutter.rules import load_rules


def _rules():
    path = Path(__file__).parent / "fixtures" / "rules.json"
    return load_rules(str(path))


def test_motif_out_of_bounds():
    rules = _rules()
    seq = "KRR"
    sites = find_cleavage_sites(seq, rules, ["Edgease"])
    assert sites["Edgease"] == []


def test_exceptions_override():
    rules = _rules()
    seq = "AKP"
    sites = find_cleavage_sites(seq, rules, ["Testase"])
    assert sites["Testase"] == []


def test_c_terminal_cleavage_allowed():
    rules = _rules()
    seq = "AK"
    sites = find_cleavage_sites(seq, rules, ["Testase"])
    assert sites["Testase"] == [2]
