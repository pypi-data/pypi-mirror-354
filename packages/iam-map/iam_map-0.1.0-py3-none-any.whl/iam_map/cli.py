"""
CLI for offline IAM-graph analysis.
• export-graph   – regenerate data/<profile>.dot
• query-graph    – rich filtering, tabular output
• shell          – natural-language interface (Ollama → CLI)
"""
from __future__ import annotations
import sys, shlex, subprocess
from pathlib import Path
from typing import List

import typer
import networkx as nx
from rich import print
from rich.table import Table
from rich.console import Console

from iam_map.graph_query import query_users_exact
from iam_map.ollama_client import query_ollama
from iam_map.paths import DATA_DIR  # <── NEW
from iam_map.exporter import export_graph


APP = typer.Typer(help="Offline IAM graph toolkit")

# ----------------------------------------------------------------------
MODEL_NAME = "mistral"  # default Ollama model tag


# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 1️⃣  query-graph  (core command)
# ----------------------------------------------------------------------
@APP.command("query-graph")
def query_graph(
        include_policy: List[str] = typer.Option(None, "--include-policy", "-p"),
        exclude_policy: List[str] = typer.Option(None, "--exclude-policy"),
        include_group: List[str] = typer.Option(None, "--include-group", "-g"),
        exclude_group: List[str] = typer.Option(None, "--exclude-group"),
        policy_logic: str = typer.Option("all", help="'all' or 'any'"),
        group_logic: str = typer.Option("all", help="'all' or 'any'"),
        dot_path: Path = typer.Option(None, help="Path to .dot file (defaults to ./data/graph.dot)"),
):
    """Filter IAM users from an offline graph snapshot."""
    # default dot_path = ./data/graph.dot in current workdir
    if dot_path is None:
        dot_path = DATA_DIR / "graph.dot"

    G = nx.drawing.nx_pydot.read_dot(dot_path)

    users = query_users_exact(
        G,
        include_policies=include_policy,
        exclude_policies=exclude_policy,
        in_groups=include_group,
        not_in_groups=exclude_group,
        policy_logic=policy_logic,
        group_logic=group_logic,
        return_meta=True,
    )

    if users:
        console = Console()
        table = Table(title=f"{len(users)} IAM user(s) matched")
        table.add_column("User Name", style="cyan")
        table.add_column("User ID", style="green")
        for u in users:
            table.add_row(u["user_name"], u["user_id"])
        console.print(table)
    else:
        print("[yellow]No users matched.[/]")


# ----------------------------------------------------------------------
# 2️⃣  Interactive NL→CLI shell
# ----------------------------------------------------------------------
@APP.command("shell")
def interactive_shell(
        profile: str = typer.Option("default", help="Graph profile name (data/<profile>.dot)"),
        port: int = typer.Option(11434, "--port", help="Ollama server port"),
        model: str = typer.Option(MODEL_NAME, "--model", help="Ollama model tag"),
):
    """Natural-language shell that wraps `query-graph`."""
    dot_path = DATA_DIR / f"{profile}.dot"

    if not dot_path.exists():
        print(f"[red]Snapshot not found: {dot_path}")
        raise typer.Exit(1)

    print(f"[cyan]🧠 IAM Graph Shell — profile: {profile}  |  Ollama port: {port}")
    print("Type 'exit' or Ctrl-C to quit.")

    while True:
        try:
            question = input("💬 > ").strip()
            if question.lower() in {"exit", "quit"}:
                break

            prompt = _build_prompt(question)
            frag = query_ollama(prompt, model=model, port=port).strip()
            frag = frag.replace("```", "").strip("`").strip()
            if frag.lower().startswith("query-graph"):
                frag = frag.split(None, 1)[1]

            print(f"[dim]⚙  {frag}[/]")

            cmd = f"{sys.executable} {__file__} query-graph --dot-path {dot_path} {frag}"
            subprocess.run(shlex.split(cmd), check=False)
            print()

        except KeyboardInterrupt:
            print()
            break

@APP.command("export-graph")
def export_graph_cmd(
    profile: str = typer.Option(None, help="AWS CLI profile (uses default creds if omitted)"),
):
    """
    Fetch live IAM data and save a DOT snapshot under data/<profile>.dot.
    """
    dot_path = export_graph(profile=profile, out_dir=DATA_DIR)
    print(f"[green]Snapshot written:[/] {dot_path}")

# ----------------------------------------------------------------------
# 3️⃣  Prompt-builder for Ollama
# ----------------------------------------------------------------------
def _build_prompt(nl_query: str) -> str:
    return f"""
You are an assistant that converts questions about IAM graph snapshots
into CLI fragments for the command `query-graph`.

Available flags:

  --include-policy     (repeatable)  exact policy name (e.g., AmazonEC2FullAccess)
  --exclude-policy     (repeatable)
  --include-group      (repeatable)
  --exclude-group      (repeatable)
  --policy-logic       all|any       (default is all)
  --group-logic        all|any       (default is all)

🚫 IMPORTANT RULES:

- If the user says "or" between policies → add: --policy-logic any
- If the user says "or" between groups  → add: --group-logic any
- If the user says "include admins", then add: --include-policy AdministratorAccess
- But if the user does **not** mention admins, do **not** include AdministratorAccess.
- NEVER include `AdministratorAccess` unless the user explicitly says to include admins.
- Return ONLY the CLI options (no 'query-graph', no Python, no prose).
- DO NOT wrap output in quotes or backticks.

Examples:
Q: Users with EC2 and S3 access  
A: --include-policy AmazonEC2FullAccess --include-policy AmazonS3ReadOnlyAccess

Q: Users with EC2 or Lambda  
A: --include-policy AmazonEC2FullAccess --include-policy AWSLambda_FullAccess --policy-logic any

Q: Users with Lambda full access including Admins  
A: --include-policy AWSLambda_FullAccess --include-policy AdministratorAccess --policy-logic any 

Q: Lambda access but not admins  
A: --include-policy AWSLambda_FullAccess --exclude-policy AdministratorAccess

Q: EC2 access in dev or test  
A: --include-policy AmazonEC2FullAccess --include-group dev --include-group test --group-logic any

Now convert this query:

{nl_query}

CLI:""".strip()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    APP()
