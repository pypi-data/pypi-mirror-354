import argparse

from ragssitant.agent.mistral import Mistral
from ragssitant.chuncker.text_chuncker import TextChunker
from ragssitant.db.persistant_db import VectorDB


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a research question.")
    parser.add_argument("query", type=str, help="The research question to answer.")
    args = parser.parse_args()

    documents_path = "./data"
    chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
    publications = chunker.load_documents(documents_path)
    chunked_publications = chunker.process_documents(publications)
    print(f"\nTotal chunked documents: {len(chunked_publications)}")

    vectordb = VectorDB(db_path="./research_db", collection_name="ml_publications")
    vectordb.insert_documents(chunked_publications)
    print("Documents inserted into vector database.")

    llm = Mistral()
    answer, sources = llm.answer_question(args.query, vectordb)
    print("Query:", args.query)
    print("AI Answer:", answer)
    print("\nBased on sources:")
    for source in sources:
        print(f"- {source['title']}")


if __name__ == "__main__":
    main()
