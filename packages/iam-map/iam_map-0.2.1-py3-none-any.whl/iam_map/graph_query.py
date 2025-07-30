# graph_query.py  – now optionally returns user metadata
from typing import Iterable, List, Set, Dict, Any
import networkx as nx

# ---------- helpers -------------------------------------------------
def _norm(s) -> str:
    if isinstance(s, (list, tuple)):
        s = s[0] if s else ""
    return str(s).strip('"').strip()

def _edge_label(d) -> str:
    return _norm(d.get("label"))

# ---------- graph traversal ----------------------------------------
def _effective_policies(G: nx.MultiDiGraph, user: str) -> Set[str]:
    user = _norm(user)
    direct = {_norm(t) for _, t, d in G.out_edges(user, data=True)
              if _edge_label(d) == "attached"}
    groups = {_norm(t) for _, t, d in G.out_edges(user, data=True)
              if _edge_label(d) == "member"}
    via_groups = {_norm(p) for g in groups
                  for _, p, d in G.out_edges(g, data=True)
                  if _edge_label(d) == "attached"}
    return direct | via_groups

def _user_groups(G: nx.MultiDiGraph, user: str) -> Set[str]:
    user = _norm(user)
    return {_norm(t) for _, t, d in G.out_edges(user, data=True)
            if _edge_label(d) == "member"}

# ---------- public API ---------------------------------------------
def query_users_exact(
    G: nx.MultiDiGraph,
    *,
    include_policies: Iterable[str] | None = None,
    exclude_policies: Iterable[str] | None = None,
    in_groups:        Iterable[str] | None = None,
    not_in_groups:    Iterable[str] | None = None,
    policy_logic:     str = "all",     # "all" | "any"
    group_logic:      str = "all",     # "all" | "any"
    return_meta:      bool = False     # NEW: True → return dicts with user_id
) -> List[str] | List[Dict[str, Any]]:

    include_policies = {_norm(p) for p in (include_policies or [])}
    exclude_policies = {_norm(p) for p in (exclude_policies or [])}
    in_groups        = {_norm(g) for g in (in_groups or [])}
    not_in_groups    = {_norm(g) for g in (not_in_groups or [])}

    results: list = []
    for raw_n, data in G.nodes(data=True):
        n = _norm(raw_n)
        if _norm(data.get("shape")) != "box":        # skip non-user nodes
            continue

        pols = _effective_policies(G, n)
        grps = _user_groups(G, n)

        # ---- policy filters ----
        if include_policies:
            ok = (include_policies.issubset(pols) if policy_logic == "all"
                  else bool(include_policies & pols))
            if not ok:
                continue
        if exclude_policies and exclude_policies & pols:
            continue

        # ---- group filters ----
        if in_groups:
            ok_grp = (in_groups.issubset(grps) if group_logic == "all"
                      else bool(in_groups & grps))
            if not ok_grp:
                continue
        if not_in_groups and not_in_groups & grps:
            continue

        if return_meta:
            results.append({
                "user_name": n,
                "user_id":   _norm(data.get("user_id", "")),
                "groups":    sorted(grps),
                "policies":  sorted(pols),
            })
        else:
            results.append(n)

    return results
