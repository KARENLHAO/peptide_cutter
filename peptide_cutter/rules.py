from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, Iterable, List

POSITIONS = ["P4", "P3", "P2", "P1", "P1_prime", "P2_prime"]
CUT = "between P1 and P1_prime"
OFFSETS = {
    "P4": -3,
    "P3": -2,
    "P2": -1,
    "P1": 0,
    "P1_prime": 1,
    "P2_prime": 2,
}


@dataclass(frozen=True)
class PositionConstraint:
    offset: int
    include: frozenset[str]
    exclude: frozenset[str]


@dataclass(frozen=True)
class Motif:
    constraints: List[PositionConstraint]


@dataclass(frozen=True)
class EnzymeRule:
    name: str
    cleaves: List[Motif]
    blocks: List[Motif]


@dataclass(frozen=True)
class RulesDB:
    schema_version: str
    description: str
    positions: List[str]
    cut: str
    enzymes: Dict[str, EnzymeRule]


def load_rules(path: str) -> RulesDB:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key in ("schema_version", "description", "positions", "cut", "enzymes"):
        if key not in data:
            raise ValueError(f"Rules file missing required key: {key}")

    positions = data["positions"]
    if positions != POSITIONS:
        raise ValueError(
            f"Invalid positions list. Expected {POSITIONS}, got {positions}."
        )
    if data["cut"] != CUT:
        raise ValueError(f"Invalid cut definition. Expected '{CUT}'.")

    enzymes_data = data["enzymes"]
    if not isinstance(enzymes_data, dict) or not enzymes_data:
        raise ValueError("Rules file must define a non-empty enzymes object.")

    enzymes: Dict[str, EnzymeRule] = {}
    for name, rule_data in enzymes_data.items():
        enzymes[name] = _parse_enzyme_rule(name, rule_data)

    return RulesDB(
        schema_version=str(data["schema_version"]),
        description=str(data["description"]),
        positions=positions,
        cut=data["cut"],
        enzymes=enzymes,
    )


def _parse_enzyme_rule(name: str, rule_data: dict) -> EnzymeRule:
    if not isinstance(rule_data, dict):
        raise ValueError(f"Invalid rule for enzyme '{name}'.")

    cleaves_data = rule_data.get("cleaves")
    if not isinstance(cleaves_data, list) or not cleaves_data:
        raise ValueError(f"Enzyme '{name}' must have a non-empty cleaves list.")

    blocks_data = _merge_blocks(rule_data)
    if not isinstance(blocks_data, list):
        raise ValueError(f"Enzyme '{name}' blocks must be a list.")

    cleaves = [_parse_motif(motif, name) for motif in cleaves_data]
    blocks = [_parse_motif(motif, name) for motif in blocks_data]

    return EnzymeRule(name=name, cleaves=cleaves, blocks=blocks)


def _merge_blocks(rule_data: dict) -> List[dict]:
    blocks = rule_data.get("blocks")
    legacy = rule_data.get("no_cleavage_exceptions")

    if blocks is None and legacy is None:
        return []
    if blocks is None:
        return legacy or []
    if legacy is None:
        return blocks or []

    if not isinstance(blocks, list) or not isinstance(legacy, list):
        return blocks if isinstance(blocks, list) else legacy

    return list(blocks) + list(legacy)


def _parse_motif(motif_data: dict, enzyme_name: str) -> Motif:
    if not isinstance(motif_data, dict):
        raise ValueError(f"Invalid motif in enzyme '{enzyme_name}'.")

    constraints: List[PositionConstraint] = []
    for pos_name, constraint_data in motif_data.items():
        if pos_name not in OFFSETS:
            raise ValueError(
                f"Invalid position '{pos_name}' in enzyme '{enzyme_name}'."
            )
        constraint = _parse_constraint(constraint_data, enzyme_name, pos_name)
        constraints.append(
            PositionConstraint(
                offset=OFFSETS[pos_name],
                include=frozenset(constraint["include"]),
                exclude=frozenset(constraint["exclude"]),
            )
        )

    return Motif(constraints=constraints)


def _parse_constraint(constraint_data: dict, enzyme_name: str, pos_name: str) -> Dict:
    if not isinstance(constraint_data, dict):
        raise ValueError(
            f"Invalid constraint for enzyme '{enzyme_name}' at {pos_name}."
        )

    include = constraint_data.get("include", [])
    exclude = constraint_data.get("exclude", [])

    if include is None:
        include = []
    if exclude is None:
        exclude = []

    if not isinstance(include, list) or not isinstance(exclude, list):
        raise ValueError(
            f"Invalid include/exclude lists for enzyme '{enzyme_name}' at {pos_name}."
        )

    include_set = _normalize_aa_list(include, enzyme_name, pos_name)
    exclude_set = _normalize_aa_list(exclude, enzyme_name, pos_name)

    return {"include": include_set, "exclude": exclude_set}


def _normalize_aa_list(values: Iterable, enzyme_name: str, pos_name: str) -> List[str]:
    normalized: List[str] = []
    for value in values:
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError(
                f"Invalid amino acid '{value}' for enzyme '{enzyme_name}' at {pos_name}."
            )
        normalized.append(value.upper())
    return normalized
