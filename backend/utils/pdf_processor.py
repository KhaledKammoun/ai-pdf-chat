import fitz  # PyMuPDF
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS  # Updated import

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    return text

def process_pdf(pdf_path):
    """Processes the PDF, splits it into chunks, and creates a FAISS index."""
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Adjust based on your needs
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(text)
    
    # Create embeddings for the chunks
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create FAISS index
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def retrieve_relevant_chunks(vector_store, query, k=3):
    """Retrieves the top-k most relevant chunks for a given query."""
    return vector_store.similarity_search(query, k=k)