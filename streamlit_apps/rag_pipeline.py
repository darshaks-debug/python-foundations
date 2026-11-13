import os
import time
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables (GEMINI_API_KEY)
load_dotenv()

class PDFRAGAssistant:
    def __init__(self, db_path="./chroma_db", collection_name="pdf_collection"):
        # 1. Setup Embedding Model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 2. Setup ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
        
        # 3. Setup Gemini Client (This fixes the missing attribute error)
        self.ai_client = genai.Client()

    def split_text_with_overlap(self, text, chunk_size=500, chunk_overlap=100):
        """Splits text into chunks of a certain size with overlapping context."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - chunk_overlap
        return chunks

    def index_pdf(self, pdf_path, chunk_size=500, chunk_overlap=100):
        """Extracts text from a PDF, chunks it, and stores embeddings in ChromaDB."""
        print(f"📄 Reading PDF: {pdf_path}")
        reader = PdfReader(pdf_path)
        
        all_chunks = []
        all_metadata = []
        all_ids = []
        
        chunk_counter = 0
        
        # Extract text page by page to keep track of page numbers for citations
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
                
            chunks = self.split_text_with_overlap(text, chunk_size, chunk_overlap)
            
            for chunk in chunks:
                all_chunks.append(chunk)
                all_metadata.append({"source": Path(pdf_path).name, "page": page_num})
                all_ids.append(f"chunk_{chunk_counter}")
                chunk_counter += 1
                
        if not all_chunks:
            raise ValueError("No text could be extracted from the PDF.")

        print(f"🧠 Embedding {len(all_chunks)} chunks in batches...")
        
        # Batch processing to prevent memory crashes
        batch_size = 500
        for i in range(0, len(all_chunks), batch_size):
            batch_texts = all_chunks[i:i+batch_size]
            batch_ids = all_ids[i:i+batch_size]
            batch_meta = all_metadata[i:i+batch_size]
            
            batch_embeddings = self.embedding_model.encode(batch_texts).tolist()
            
            self.collection.upsert(
                embeddings=batch_embeddings,
                documents=batch_texts,
                metadatas=batch_meta,
                ids=batch_ids
            )
            
        return len(all_chunks)

    def ask(self, question, n_results=3):
        """Retrieves relevant chunks and asks Gemini to answer the question."""
        print(f"🔍 Searching for: '{question}'")
        
        # 1. Embed the question
        question_embedding = self.embedding_model.encode([question]).tolist()
        
        # 2. Query ChromaDB
        results = self.collection.query(
            query_embeddings=question_embedding,
            n_results=n_results
        )
        
        # 3. Build Context with Citations
        context_blocks = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                page = meta.get('page', 'Unknown')
                source = meta.get('source', 'Unknown')
                context_blocks.append(f"[{source} - Page {page}]\n{doc}")
                
        context = "\n\n".join(context_blocks)
        
        if not context:
            return "I couldn't find any relevant information in the document."

        # 4. Generate Prompt
        prompt = f"""
        You are a helpful document assistant. Answer the user's question using ONLY the context provided below. 
        If the answer is not in the context, say "I don't know based on the provided document."
        Always cite the page number(s) you used.

        CONTEXT:
        {context}

        QUESTION: {question}
        """
        
        print("🤖 Asking Gemini...")
        
        # 5. Generate Response with Retry Logic (Exponential Backoff)
        max_retries = 4
        for attempt in range(max_retries):
            try:
                # Using the new google-genai SDK
                response = self.ai_client.models.generate_content(
                    model="gemini-3.5-flash", # or gemini-1.5-flash depending on your API access
                    contents=prompt,
                )
                return response.text
            except Exception as e:
                error_msg = str(e)
                # Catch 503 (Overloaded) or 429 (Rate Limit) errors
                if '503' in error_msg or '429' in error_msg:
                    if attempt == max_retries - 1:
                        return f"❌ Failed after {max_retries} attempts. The AI server is busy. Error: {error_msg}"
                    wait_time = 2 ** (attempt + 1)
                    print(f"⚠️ Server busy. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    return f"❌ AI Error: {error_msg}"
                    
        return "An unknown error occurred."


# For local CLI testing (optional)
if __name__ == "__main__":
    assistant = PDFRAGAssistant()
    # assistant.index_pdf("document.pdf")
    # print(assistant.ask("What is this document about?"))