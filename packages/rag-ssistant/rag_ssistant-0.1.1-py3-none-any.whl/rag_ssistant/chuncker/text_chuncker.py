import json
import os
from typing import Dict, List, Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field


class TextChunker(BaseModel):
    chunk_size: int = Field(default=1000, description="Number of characters per chunk")
    chunk_overlap: int = Field(default=200, description="Number of overlapping characters between chunks")
    separators: List[str] = Field(default_factory=lambda: ["\n\n", "\n", ". ", " ", ""], description="Chunk separators")

    def process_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Process a list of documents, chunking each one and returning a list of chunked documents.
        Each document dict must have 'title' and 'content'.
        """
        chunked_documents = []
        for doc in documents:
            title = doc.get("title", "untitled")
            content = doc.get("content", "")
            chunks = self.chunk_text(content, title)
            chunked_documents.extend(chunks)
        return chunked_documents

    def chunk_text(self, text: str, title: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Split text into chunks with optional metadata.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
        )
        chunks = splitter.split_text(text)
        chunk_data = []
        for i, chunk in enumerate(chunks):
            chunk_info = {
                "content": chunk,
                "chunk_id": f"{title}_{i}" if title else f"chunk_{i}",
            }
            if title:
                chunk_info["title"] = title
            chunk_data.append(chunk_info)
        return chunk_data

    def load_documents(self, documents_path: str) -> List[Dict[str, str]]:
        documents = []
        for file in os.listdir(documents_path):
            if file.endswith(".json"):
                file_path = os.path.join(documents_path, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        for obj in data:
                            title = obj.get("title", "untitled")
                            content = obj.get("publication_description", "")
                            documents.append({"title": title, "content": content})
                    print(f"Successfully loaded: {file}")
                except Exception as e:
                    print(f"Error loading {file}: {str(e)}")
        print(f"\nTotal documents loaded: {len(documents)}")
        return documents
