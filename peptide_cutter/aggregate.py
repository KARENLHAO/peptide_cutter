from __future__ import annotations

import re
from typing import Dict, List, Tuple


def _natural_key(text: str) -> Tuple:
    parts = re.split(r"(\d+)", text)
    key: List[object] = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part.lower())
    return tuple(key)


def build_summary(selected: List[str], sites_by_enzyme: Dict[str, List[int]]) -> Dict:
    selected_sorted = sorted(selected, key=_natural_key)
    table_rows = []
    do_not_cut = []

    groups: Dict[tuple[int, ...], List[str]] = {}
    for enzyme_name in selected_sorted:
        sites = sorted(set(sites_by_enzyme.get(enzyme_name, [])))
        table_rows.append(
            {
                "name": enzyme_name,
                "count": len(sites),
                "sites": sites,
            }
        )
        if not sites:
            do_not_cut.append(enzyme_name)
        key = tuple(sites)
        if key not in groups:
            groups[key] = []
        groups[key].append(enzyme_name)

    map_groups = []
    for sites_key, names in groups.items():
        map_groups.append(
            {
                "name": "_".join(names),
                "enzymes": names,
                "sites": list(sites_key),
            }
        )

    return {
        "selected_sorted": selected_sorted,
        "table_rows": table_rows,
        "do_not_cut": do_not_cut,
        "groups": map_groups,
    }
