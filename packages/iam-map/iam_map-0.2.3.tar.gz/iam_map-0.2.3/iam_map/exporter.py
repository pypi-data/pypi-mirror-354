# iam_anal/exporter.py  – export IAM graph for any profile
from pathlib import Path
import boto3
from iam_map.paths import DATA_DIR


# ─────────────────────────────────────────────────────────────
def fetch_iam_data(iam):
    users = {u["UserName"]: u["UserId"] for u in iam.list_users()["Users"]}
    groups, user_groups, policies = [], {}, {}

    for user in users:
        g_objs  = iam.list_groups_for_user(UserName=user)["Groups"]
        g_names = [g["GroupName"] for g in g_objs]
        user_groups[user] = g_names
        groups.extend(g for g in g_names if g not in groups)

        upols = iam.list_attached_user_policies(UserName=user)["AttachedPolicies"]
        policies[user] = [p["PolicyName"] for p in upols]

    for g in groups:
        gp = iam.list_attached_group_policies(GroupName=g)["AttachedPolicies"]
        policies[g] = [p["PolicyName"] for p in gp]

    return {"users": users, "groups": groups,
            "user_groups": user_groups, "policies": policies}


def export_to_dot(data, out_file: Path):
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w") as f:
        f.write("digraph IAM {\n")
        for name, uid in data["users"].items():
            f.write(f'  "{name}" [shape=box, user_id="{uid}"];\n')
        for g in data["groups"]:
            f.write(f'  "{g}" [shape=ellipse, style=filled, fillcolor=lightgrey];\n')
        for u, gs in data["user_groups"].items():
            for g in gs:
                f.write(f'  "{u}" -> "{g}" [label="member"];\n')
        for ent, pols in data["policies"].items():
            for p in pols:
                f.write(f'  "{ent}" -> "{p}" [label="attached"];\n')
                f.write(f'  "{p}" [shape=note, style=dashed];\n')
        f.write("}\n")

    print(f"✅  Exported IAM graph → {out_file}")


# Public helper for CLI
def export_graph(profile: str | None = None, out_dir: Path | None = None) -> Path:
    """
    Export the IAM graph for `profile` and return the Path to the .dot file.
    If profile is None → default AWS credentials.
    """
    if profile:
        boto3.setup_default_session(profile_name=profile)

    iam = boto3.client("iam")
    data = fetch_iam_data(iam)

    out_dir = out_dir or DATA_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    dot_file = out_dir / f"{profile or 'default'}.dot"

    export_to_dot(data, dot_file)
    return dot_file
