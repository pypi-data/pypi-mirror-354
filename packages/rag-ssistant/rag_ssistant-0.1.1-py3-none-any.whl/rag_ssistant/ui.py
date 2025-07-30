import gradio as gr

from ragssitant.agent.mistral import Mistral
from ragssitant.chuncker.text_chuncker import TextChunker
from ragssitant.db.persistant_db import VectorDB


documents_path = "./data"
chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
publications = chunker.load_documents(documents_path)
chunked_publications = chunker.process_documents(publications)

vectordb = VectorDB(db_path="./research_db", collection_name="ml_publications")
vectordb.insert_documents(chunked_publications)

llm = Mistral()


def chat_fn(message, history) -> str:
    answer, sources = llm.answer_question(message, vectordb)
    if sources:
        answer += "\n\nBased on sources:\n" + "\n".join(f"- {src['title']}" for src in sources)
    return answer


demo = gr.ChatInterface(
    fn=chat_fn,
    title="Research Assistant",
    description="Ask a research question about your documents.",
    theme="soft",
    examples=[
        "What are effective techniques for handling class imbalance?",
        "Summarize recent trends in deep learning?",
    ],
)
demo.launch(server_port=8000)
