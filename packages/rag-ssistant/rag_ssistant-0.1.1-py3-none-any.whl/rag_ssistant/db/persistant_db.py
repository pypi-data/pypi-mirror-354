import os
from typing import Any, Dict, List

import chromadb
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field, PrivateAttr


class VectorDB(BaseModel):
    db_path: str = Field(default="./research_db", description="Path to ChromaDB database")
    collection_name: str = Field(default="ml_publications", description="Collection name in ChromaDB")
    model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", description="Embedding model name")

    _client: chromadb.PersistentClient = PrivateAttr()
    _collection: chromadb.Collection = PrivateAttr()
    _embeddings_model: HuggingFaceEmbeddings = PrivateAttr()

    def __init__(self, **data) -> None:
        super().__init__(**data)
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        self._client = chromadb.PersistentClient(path=self.db_path)
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name, metadata={"hnsw:space": "cosine"}
        )
        device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )
        self._embeddings_model = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": device},
        )

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Embed a list of documents and return their embeddings.
        """
        return self._embeddings_model.embed_documents(documents)

    def insert_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Insert a list of chunked documents into the vector database.
        Each document dict must have 'content', 'chunk_id', and optionally 'title'.
        """
        next_id = self._collection.count()
        texts = [doc["content"] for doc in documents]
        embeddings = self.embed_documents(texts)
        ids = [f"document_{next_id + i}" for i in range(len(documents))]
        metadatas = [{k: v for k, v in doc.items() if k != "content"} for doc in documents]
        self._collection.add(
            embeddings=embeddings,
            ids=ids,
            documents=texts,
            metadatas=metadatas,
        )

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search the vector database for the most relevant chunks to the query.
        """
        query_vector = self._embeddings_model.embed_query(query)
        results = self._collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        relevant_chunks = []
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i]
            relevant_chunks.append(
                {
                    "content": doc,
                    "title": meta.get("title", ""),
                    "chunk_id": meta.get("chunk_id", ""),
                    "similarity": 1 - results["distances"][0][i],
                }
            )
        return relevant_chunks
