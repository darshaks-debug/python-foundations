import streamlit as st
import os
from rag_pipeline import PDFRAGAssistant
import uuid import tempfile

# 1. Page Configuration (MUST BE THE FIRST ST COMMAND)
st.set_page_config(page_title="Chat with your PDF", page_icon="📄", layout="wide")
st.title("📄 Chat with your PDF (RAG)")

# 2. Safe Initialization of Session State
# Using .get() prevents the AttributeError if the key doesn't exist yet.
if "assistant" not in st.session_state:
    st.session_state.assistant = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

# 3. Sidebar: File Uploader
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None and not st.session_state.pdf_uploaded:
        file_path = "uploaded_document.pdf"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        with st.spinner("Processing PDF and building knowledge base..."):
            try:
                # Initialize the assistant
                st.session_state.assistant = PDFRAGAssistant()
                
                # Clear previous database chunks for a fresh start
                #Properly reset the collection for a fresh start
                chroma_client = st.session_state.assistant.chroma_client
                collection_name = st.session_state.assistant.collection.name
                
                # Delete the old collection entirely
                try:
                    chroma_client.delete_collection(name=collection_name)
                except Exception:
                    pass # Ignore if it doesn't exist yet
                
                # Recreate a fresh, empty collection
                st.session_state.assistant.collection = chroma_client.get_or_create_collection(
                    name=collection_name
                )
                
                # Index the new PDF
                chunks = st.session_state.assistant.index_pdf(file_path)
                
                st.success(f"Successfully indexed {chunks} chunks!")
                st.session_state.pdf_uploaded = True
                st.session_state.messages = [] # Reset chat history
            except Exception as e:
                st.error(f"Error processing PDF: {e}")

# 4. Display Previous Chat Messages
# We use st.session_state.get() to safely fetch the list.
for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle New User Input
if prompt := st.chat_input("Ask a question about the document..."):
    if not st.session_state.get("pdf_uploaded", False):
        st.warning("Please upload a PDF first using the sidebar.")
    else:
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Searching document and thinking..."):
                try:
                    answer = st.session_state.assistant.ask(prompt)
                    st.markdown(answer)
                    # Add to history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"An error occurred: {e}")