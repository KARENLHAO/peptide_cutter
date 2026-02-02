import pytest

from peptide_cutter.sequence import parse_sequence, validate_sequence


def test_parse_sequence_fasta():
    text = ">sp|P12345| Example protein\nac d1E\nFG2\n"
    seq = parse_sequence(text)
    assert seq == "ACDEFG"


def test_validate_sequence_illegal_positions():
    seq = "ACBZX"
    with pytest.raises(ValueError) as exc:
        validate_sequence(seq, strict=True, replacements=None)
    message = str(exc.value)
    assert "B" in message and "3" in message
    assert "Z" in message and "4" in message
    assert "X" in message and "5" in message


def test_validate_sequence_replacements():
    seq = "ABX"
    new_seq, meta = validate_sequence(
        seq, strict=True, replacements={"B": "D", "X": "A"}
    )
    assert new_seq == "ADA"
    assert meta["replacements"]["B"]["count"] == 1
    assert meta["replacements"]["X"]["count"] == 1
