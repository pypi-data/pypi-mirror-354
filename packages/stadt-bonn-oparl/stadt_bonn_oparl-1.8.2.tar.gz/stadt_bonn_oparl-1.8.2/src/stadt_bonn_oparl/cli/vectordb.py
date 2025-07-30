import json

import chromadb
from chromadb.config import Settings
from cyclopts import App
from loguru import logger
from pydantic import DirectoryPath
import rich

from stadt_bonn_oparl.config import CLI_QUERYABLE_OPARL_TYPES
from stadt_bonn_oparl.papers.models import UnifiedPaper
from stadt_bonn_oparl.papers.vector_db import VectorDb

vectordb = App(name="vectordb", help="Ingest OPARL Papers into VectorDB")


@vectordb.command()
def ingest(data_path: DirectoryPath, vectordb_name: str = "vectordb-100") -> bool:
    """
    Ingest (add or update) OPARL Papers, including metadata, analysis and content, to VectorDB.

    Parameters
    ----------
    data_path: DirectoryPath
        Path to the directory containing OPARL Papers in PDF file
    vector_db_name: str
        Name of the VectorDB to ingest data into
    """
    db = VectorDb(vectordb_name)

    # Check if the directory exists
    if not data_path.exists():
        logger.error(f"Directory {data_path} does not exist.")
        return False

    for dir_path in data_path.iterdir():
        try:
            rats_info = _create_paper(dir_path)
            doc_id = db.create_document(rats_info)
            logger.debug(f"Document created with ID: {doc_id}")
        except FileNotFoundError as e:
            logger.error(e)

    return True


def _create_paper(data_path: DirectoryPath) -> UnifiedPaper:
    """
    Create a Paper object from a directory path.
    """
    # Assuming the directory contains metadata.json and content.txt files
    metadata_path = data_path / "metadata.json"
    analysis_path = data_path / "analysis.json"
    content_path = data_path.glob("*.md")  # Get the first markdown file
    content = ""
    analysis = {}
    metadata = {}

    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found in {data_path}")
    if not content_path:
        raise FileNotFoundError(f"No markdown files found in {data_path}")

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    with open(analysis_path, "r") as f:
        analysis = json.load(f)

    for file in content_path:
        if file.suffix == ".md":
            with open(file, "r") as f:
                content = f.read()

    return UnifiedPaper(
        paper_id=metadata.get("id"),
        metadata=metadata,
        markdown_text=content,
        analysis=analysis,
        enrichment_status="enriched",
        external_oparl_data={},
    )


@vectordb.command()
def query(oparl_type: CLI_QUERYABLE_OPARL_TYPES, query_text: str):
    """
    Query the VectorDB for a specific OParl type and query text.

    Parameters
    ----------
    oparl_type: str
        The type of OParl object to query (e.g., "Paper", "Meeting")
    query_text: str
        The text to search for in the VectorDB
    """

    chromadb_client = chromadb.PersistentClient(
        path="./chroma-api",
        settings=Settings(
            anonymized_telemetry=False,  # disable posthog telemetry
        ),
    )

    if oparl_type == "Organization":
        organizations_collection = chromadb_client.get_or_create_collection(
            name="organizations"
        )

        rich.print(
            f"[yellow]Searching for organizations with query: {query_text}[/yellow]"
        )
        results = organizations_collection.query(
            query_texts=[query_text],
            where_document={"$contains": query_text},
            n_results=10,
        )

        if not results["documents"]:
            rich.print("[red]No organizations found matching the query.[/red]")
            return

        rich.print(f"[green]Found {len(results['documents'])} organizations:[/green]")
        rich.print(results)
