# src/pr_agent/cli.py

import typer
from pr_agent.core.metadata_manager import DirectoryMetadataStore
from pr_agent.settings import settings

app = typer.Typer(help="PR-Agent CLI: explore your discovered docs")

@app.command("list-docs")
def list_docs():
    """
    List all discovered documents with their doc_id and filename.
    """
    store = DirectoryMetadataStore(settings.METADATA_DIR)
    for doc_id in sorted(store.get_all_ids()):
        meta = store.read(doc_id)
        typer.echo(f"{doc_id}  →  {meta.get('Original Filename')}")

@app.command("show-url")
def show_url(doc_id: str):
    """
    Print the Original File URL for a given document ID.
    """
    store = DirectoryMetadataStore(settings.METADATA_DIR)
    meta = store.read(doc_id)
    url = meta.get("Original File URL")
    if not url:
        typer.secho(f"[!] No URL found for {doc_id}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    typer.echo(url)

if __name__ == "__main__":
    app()
