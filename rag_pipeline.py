import os
import time
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


def split_text_with_overlap(
    text: str, chunk_size: int = 500, chunk_overlap: int = 100
) -> List[str]:
    """Splits text into overlapping chunks without cutting words in half."""
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        # If we aren't at the end of the text, backtrack to the nearest space
        if end < text_length:
            last_space = text.rfind(" ", start, end)
            if last_space > start:
                end = last_space

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        # Move start forward, stepping back by chunk_overlap
        start = max(end - chunk_overlap, start + 1)

    return chunks


class PDFRAGAssistant:
    def __init__(
        self,
        db_path: str = "./chroma_db",
        collection_name: str = "pdf_collection",
        embedding_model_name: str = "all-MiniLM-L6-v2",
        gemini_model_name: str = "gemini-3.5-flash",
    ):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file.")

        print("⏳ Loading local embedding model & ChromaDB...")
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name
        )

        # Initialize the modern Google GenAI client once
        self.ai_client = genai.Client(api_key=api_key)
        self.gemini_model_name = gemini_model_name

    def index_pdf(
        self, pdf_path: str, chunk_size: int = 500, chunk_overlap: int = 100
    ) -> int:
        """Extracts text page-by-page, chunks with overlap, and stores with metadata in batches."""
        path = Path(pdf_path)
        if not path.is_file():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        print(f"📄 Reading '{path.name}'...")
        reader = PdfReader(str(path))

        chunks: List[str] = []
        metadatas: List[Dict[str, Any]] = []
        ids: List[str] = []

        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if not page_text or not page_text.strip():
                continue

            page_chunks = split_text_with_overlap(
                page_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )
            for chunk_idx, chunk in enumerate(page_chunks):
                chunks.append(chunk)
                metadatas.append({"source": path.name, "page": page_num})
                ids.append(f"{path.stem}_p{page_num}_c{chunk_idx}")

        if not chunks:
            raise ValueError(
                f"No extractable text found in '{path.name}'. It may be a scanned image PDF."
            )

        print(f"🧠 Embedding {len(chunks)} chunks and saving to persistent database...")
        embeddings = self.embedding_model.encode(
            chunks, show_progress_bar=True
        ).tolist()

        # ChromaDB SQLite limit: max 5,461 items per single insert batch
        batch_size = 5000
        for i in range(0, len(chunks), batch_size):
            end_idx = min(i + batch_size, len(chunks))
            print(f"   💾 Saving chunks {i + 1} to {end_idx}...")
            self.collection.upsert(
                ids=ids[i:end_idx],
                embeddings=embeddings[i:end_idx],
                documents=chunks[i:end_idx],
                metadatas=metadatas[i:end_idx],
            )

        print("✅ Database ready!\n")
        return len(chunks)

    def ask(self, question: str, n_results: int = 3) -> str:
        """Retrieves relevant chunks with page numbers and queries Gemini with automatic retry."""
        question_embedding = self.embedding_model.encode([question]).tolist()

        results = self.collection.query(
            query_embeddings=question_embedding,
            n_results=n_results,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        if not documents:
            return "No documents are indexed in the database yet."

        context_blocks = []
        for doc, meta in zip(documents, metadatas):
            page = meta.get("page", "?")
            source = meta.get("source", "Document")
            context_blocks.append(f"[{source} - Page {page}]\n{doc}")

        context = "\n\n---\n\n".join(context_blocks)

        system_instruction = (
            "You are a helpful document assistant. Answer the user's question using ONLY "
            "the context provided. Cite the page number(s) in your answer (e.g., [Page 2]). "
            "If the answer is not in the context, say 'I don't know based on the provided document.'"
        )

        prompt = f"CONTEXT:\n{context}\n\nQUESTION: {question}"

        # Retry logic for temporary server congestion (503 / 429)
        max_retries = 4
        for attempt in range(1, max_retries + 1):
            try:
                response = self.ai_client.models.generate_content(
                    model=self.gemini_model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2,
                    ),
                )
                return response.text or "No response generated."
            except Exception as e:
                error_msg = str(e)
                if ("503" in error_msg or "429" in error_msg) and attempt < max_retries:
                    wait_time = attempt * 3
                    print(
                        f"   ⏳ Server busy (503/429). Retrying in {wait_time}s (Attempt {attempt}/{max_retries})..."
                    )
                    time.sleep(wait_time)
                else:
                    raise


def main():
    pdf_file = "document.pdf"

    try:
        assistant = PDFRAGAssistant()

        if assistant.collection.count() == 0:
            assistant.index_pdf(pdf_file)
        else:
            print(
                f"⚡ Loaded {assistant.collection.count()} existing chunks from disk.\n"
            )

        while True:
            question = input("Ask a question about the PDF (or type 'quit'): ").strip()
            if question.lower() == "quit":
                break
            if not question:
                continue

            print("🔍 Searching context & asking Gemini...")
            try:
                answer = assistant.ask(question, n_results=3)
                print(f"\n💡 Answer:\n{answer}\n")
                print("-" * 50)
            except Exception as e:
                print(
                    f"\n⚠️ API Error: {e}\nPlease try your question again in a moment.\n"
                )

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()