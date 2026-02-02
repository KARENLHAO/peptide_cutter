from __future__ import annotations

from typing import Dict, List

from .rules import EnzymeRule, Motif, RulesDB


def find_cleavage_sites(
    seq: str, rules: RulesDB, enzymes: List[str]
) -> Dict[str, List[int]]:
    sites_by_enzyme: Dict[str, List[int]] = {}
    length = len(seq)

    for enzyme_name in enzymes:
        if enzyme_name not in rules.enzymes:
            raise KeyError(f"Unknown enzyme: {enzyme_name}")
        rule = rules.enzymes[enzyme_name]
        sites = set()
        for cut_after in range(1, length):
            if _matches_any_motif(seq, cut_after, rule.cleaves):
                if rule.exceptions and _matches_any_motif(
                    seq, cut_after, rule.exceptions
                ):
                    continue
                sites.add(cut_after)
        sites_by_enzyme[enzyme_name] = sorted(sites)

    return sites_by_enzyme


def _matches_any_motif(seq: str, cut_after: int, motifs: List[Motif]) -> bool:
    for motif in motifs:
        if _motif_matches(seq, cut_after, motif):
            return True
    return False


def _motif_matches(seq: str, cut_after: int, motif: Motif) -> bool:
    length = len(seq)
    for constraint in motif.constraints:
        idx = cut_after + constraint.offset
        if idx < 1 or idx > length:
            return False
        aa = seq[idx - 1]
        if constraint.include and aa not in constraint.include:
            return False
        if constraint.exclude and aa in constraint.exclude:
            return False
    return True
