import os

from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch

# Example usage
if __name__ == "__main__":
    store = FaissVectorStore("faiss_store")
    faiss_index = "faiss_store/faiss.index"
    metadata_file = "faiss_store/metadata.pkl"
    if not (os.path.exists(faiss_index) and os.path.exists(metadata_file)):
        docs = load_all_documents("data")
        store.build_from_documents(docs)
    else:
        store.load()
    rag_search = RAGSearch()
    query = "What is attention mechanism?"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Summary:", summary)