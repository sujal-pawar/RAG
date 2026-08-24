# PDF RAG Assistant

A notebook-based retrieval-augmented generation (RAG) pipeline for loading PDF documents, splitting them into searchable chunks, creating semantic embeddings, storing those embeddings in a persistent ChromaDB collection, and generating answers from retrieved context.

The main workflow is implemented in `notebook/pdf_loader.ipynb`. It combines semantic retrieval with a Groq-hosted language model and can return answers, source metadata, similarity scores, confidence, and the retrieved context. This repository is currently notebook-first; `main.py` is only a placeholder entry point.

## Features

- Load PDF files with LangChain and PyMuPDF/PyPDF.
- Split documents into manageable text chunks.
- Generate 384-dimensional embeddings with `sentence-transformers` and `all-MiniLM-L6-v2`.
- Persist document embeddings and metadata in ChromaDB.
- Retrieve the most relevant chunks with configurable `top_k` and similarity-threshold settings.
- Generate concise answers from retrieved context with LangChain and Groq.
- Return source references, similarity scores, confidence, and optional context previews.
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
├── main.py                   # Placeholder CLI entry point
├── pyproject.toml            # Project metadata and uv dependencies
└── requirements.txt          # pip-compatible dependency list
```

## Requirements

- Python 3.12 or newer
- `uv` (recommended) or `pip`
- A Groq API key for answer generation
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

## Configuration

Create a `.env` file in the project root, or set the variables in your shell:

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

`GROQ_MODEL` is optional and defaults to `openai/gpt-oss-120b`. Use a model currently available to your Groq account if the default is unavailable. The notebook also accepts the legacy `GROQ_API` variable, but `GROQ_API_KEY` is recommended.

Never commit `.env` files or expose API keys in notebook outputs.

## Running the Notebook

1. Open `notebook/pdf_loader.ipynb` in VS Code or Jupyter.
2. Select the `Python (RAG)` kernel, or select the environment where the dependencies were installed.
3. Place PDF files in `data/pdfs/`.
4. Run the ingestion cells to load PDF pages from `../data` and split them into 1,000-character chunks with 200-character overlap.
5. Run the embedding and vector-store cells to generate embeddings and persist them in the `pdf_documents` Chroma collection.
6. Run the retrieval section to inspect the most relevant document chunks.
7. Configure `GROQ_API_KEY`, then run the generation cells to produce an answer from the retrieved context.

The notebook uses paths relative to its own directory. Run it from `notebook/` or keep the existing directory layout so paths such as `../data/vector_store` resolve correctly.

## Usage Examples

### Retrieval only

The notebook exposes an `RAGRetriever` that accepts a query, the number of results, and an optional similarity threshold:

```python
results = rag_retriever.retrieve(
    "What is the difference between supervised and unsupervised learning?",
    top_k=5,
    score_threshold=0.0,
)
```

Each result contains the document content, metadata, ChromaDB distance, similarity score, and rank.

### Simple RAG answer

```python
answer = rag_simple(
    "What is the attention mechanism?",
    rag_retriever,
    llm,
    top_k=3,
)
print(answer)
```

### Advanced RAG result

```python
result = rag_advanced(
    "Explain cattle management in short points.",
    rag_retriever,
    llm,
    top_k=3,
    min_score=0.1,
    return_context=True,
)

print(result["answer"])
print(result["sources"])
print(result["confidence"])
```

The advanced pipeline returns a dictionary with `answer`, `sources`, and `confidence`. Each source includes the source filename, page, similarity score, and a short preview. When `return_context=True`, the result also includes the full retrieved `context`.

## Data and Persistence

The ChromaDB collection `pdf_documents` is stored locally in `data/vector_store/`. Re-running the indexing cells can add duplicate records because document IDs are generated dynamically. If you need a clean index, stop any notebook activity and remove the contents of that directory before indexing again.

PDFs and generated vector-store files may contain sensitive or copyrighted material. Review them before committing or sharing the repository.

## Development Notes

- `pyproject.toml` is the source of truth for the `uv` environment.
- `requirements.txt` is provided for a conventional `pip` workflow.
- `main.py` currently prints a setup message; the notebook is the active pipeline entry point.
- The embedding model is downloaded by `sentence-transformers` on first use and may require internet access.
- Groq model availability can change. Set `GROQ_MODEL` to another model listed in your Groq account when needed.

## Troubleshooting

### Model not found

If Groq returns a `404` or `model_not_found` error, the configured model is unavailable or inaccessible for your account. Set `GROQ_MODEL` to an available model and rerun the LLM initialization cell.

### Missing API key

Set `GROQ_API_KEY` in `.env` or in the environment used by the notebook kernel, then restart the kernel and rerun the configuration cells.

## License

No license has been specified for this project yet.