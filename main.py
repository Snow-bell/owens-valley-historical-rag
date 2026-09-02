import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from src.ingest import load_corpus
from src.chunk import chunk_documents
from src.embed import embed_and_store, get_chroma_collection
from src.retrieve import retrieve
from src.generate import generate

console = Console()


def index_corpus() -> None:
    """
    Load, chunk, embed, and store the full corpus in ChromaDB.
    Run this once before querying, or whenever the corpus changes.
    """
    console.print("\n[bold cyan]Indexing corpus...[/bold cyan]")
    documents = load_corpus()
    chunks = chunk_documents(documents)
    embed_and_store(chunks)
    console.print("[bold green]Corpus indexed successfully.[/bold green]\n")


def check_corpus_populated() -> bool:
    """
    Check if ChromaDB collection already has documents.
    """
    collection = get_chroma_collection()
    return collection.count() > 0


def query_loop() -> None:
    """
    Interactive query loop. Retrieves and generates answers
    until the user exits.
    """
    console.print(Panel(
        "[bold]Owens Valley Historical Research Assistant[/bold]\n"
        "Ask research questions about the Owens Valley region circa 1880–1915.\n"
        "Type [bold]exit[/bold] or [bold]quit[/bold] to stop.",
        style="cyan"
    ))

    while True:
        console.print()
        query = console.input("[bold yellow]Research question:[/bold yellow] ").strip()

        if not query:
            continue

        if query.lower() in {"exit", "quit"}:
            console.print("\n[dim]Exiting.[/dim]")
            break

        console.print("\n[dim]Retrieving sources...[/dim]")
        chunks = retrieve(query)

        if not chunks:
            console.print("[red]No relevant sources found.[/red]")
            continue

        console.print("[dim]Generating answer...[/dim]\n")
        result = generate(query, chunks)

        # Print answer
        console.print(Panel(
            result["answer"],
            title="[bold green]Answer[/bold green]",
            border_style="green",
        ))

        # Print sources
        console.print(Panel(
            result["sources"],
            title="[bold yellow]Sources[/bold yellow]",
            border_style="yellow",
        ))


def main() -> None:
    """
    Entry point. Indexes corpus if not already populated,
    then enters the query loop.
    """
    if "--reindex" in sys.argv:
        index_corpus()
    elif not check_corpus_populated():
        console.print(
            "[yellow]No corpus index found. Indexing now...[/yellow]"
        )
        index_corpus()

    query_loop()


if __name__ == "__main__":
    main()