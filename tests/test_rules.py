from pathlib import Path

from peptide_cutter.rules import load_rules


def test_load_rules_fixture():
    path = Path(__file__).parent / "fixtures" / "rules.json"
    rules = load_rules(str(path))
    assert "Testase" in rules.enzymes
    assert rules.cut == "between P1 and P1_prime"
