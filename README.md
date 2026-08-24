# RAG Document Retrieval

A notebook-based retrieval-augmented generation (RAG) foundation for loading PDF documents, splitting them into searchable chunks, creating semantic embeddings, and storing those embeddings in a persistent ChromaDB collection.

The current project focuses on the retrieval layer. It demonstrates how to find relevant source passages for a question; an LLM answer-generation step is not wired into the repository yet.

## Features

- Load PDF files with LangChain and PyMuPDF/PyPDF.
- Split documents into manageable text chunks.
- Generate 384-dimensional embeddings with `sentence-transformers` and `all-MiniLM-L6-v2`.
- Persist document embeddings and metadata in ChromaDB.
- Retrieve the most relevant chunks with configurable `top_k` and similarity-threshold settings.
- Keep source PDFs, text examples, notebooks, and the local vector store organized in separate directories.

## Project Structure

```text
.
├── data/
│   ├── pdfs/                 # Input PDF documents
│   ├── text_files/           # Example text documents
│   └── vector_store/         # Persistent ChromaDB data
├── notebook/
│   ├── document.ipynb        # Document-processing experiments
│   └── pdf_loader.ipynb      # PDF loading, indexing, and retrieval pipeline
├── src/                      # Package namespace for reusable code
├── main.py                   # Placeholder project entry point
├── pyproject.toml            # Project metadata and uv dependencies
└── requirements.txt          # pip-compatible dependency list
```

## Requirements

- Python 3.12 or newer
- `uv` (recommended) or `pip`
- Enough disk space for the embedding model and local vector database

## Installation

### Using uv

```powershell
uv sync
```

To register the project environment as a Jupyter kernel:

```powershell
uv run python -m ipykernel install --user --name rag --display-name "Python (RAG)"
```

### Using pip

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the Notebook

1. Open `notebook/pdf_loader.ipynb` in VS Code or Jupyter.
2. Select the `Python (RAG)` kernel, or select the environment where the dependencies were installed.
3. Place PDF files in `data/pdfs/`.
4. Run the notebook cells in order to load documents, create chunks, generate embeddings, and persist them to `data/vector_store/`.
5. Use the retrieval section to submit a query and inspect the most relevant document chunks.

The notebook uses paths relative to its own directory. Run it from `notebook/` or keep the existing directory layout so paths such as `../data/vector_store` resolve correctly.

## Retrieval Example

The notebook exposes an `RAGRetriever` that accepts a query, the number of results, and an optional similarity threshold:

```python
results = retriever.retrieve(
    "What is the difference between supervised and unsupervised learning?",
    top_k=5,
    score_threshold=0.0,
)
```

Each result contains the retrieved document content and its associated metadata, allowing the source context to be inspected before it is passed to a future generation step.

## Data and Persistence

The ChromaDB collection is stored locally in `data/vector_store/`. Re-running the indexing cells can add documents to the existing collection. If you need a clean index, stop any notebook activity and remove the contents of that directory before indexing again.

PDFs and generated vector-store files may contain sensitive or copyrighted material. Review them before committing or sharing the repository.

## Development Notes

- `pyproject.toml` is the source of truth for the `uv` environment.
- `requirements.txt` is provided for a conventional `pip` workflow.
- `main.py` currently prints a setup message and is not the notebook pipeline entry point.
- The embedding model is downloaded by `sentence-transformers` on first use and may require internet access.

## License

No license has been specified for this project yet.