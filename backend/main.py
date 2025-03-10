from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utils.pdf_processor import process_pdf, retrieve_relevant_chunks
from utils.llm_chain import setup_llm_chain
import os

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store vector store and conversation history
vector_store = None
conversation_history = []
MAX_CONTEXT_LENGTH = 5  # Max number of exchanges to keep in memory

# Setup LLM chain
chain = setup_llm_chain()

class ChatRequest(BaseModel):
    message: str

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Save the uploaded file temporarily
    pdf_path = f"temp_{file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(await file.read())
    
    # Process the PDF and create FAISS index
    try:
        vector_store = process_pdf(pdf_path)
        return {"message": "PDF processed successfully."}
    finally:
        # Clean up the temporary file
        os.remove(pdf_path)

@app.post("/chat/")
async def chat(request: ChatRequest):
    global vector_store, conversation_history
    if vector_store is None:
        raise HTTPException(status_code=400, detail="No PDF has been uploaded yet.")
    
    user_message = request.message
    
    # Retrieve relevant chunks from the PDF
    relevant_chunks = retrieve_relevant_chunks(vector_store, user_message)
    document_content = "\n".join([chunk.page_content for chunk in relevant_chunks])
    
    # Format conversation history
    context = "\n".join(conversation_history)
    
    # Generate response
    result = chain.invoke({
        "document_content": document_content,
        "context": context,
        "question": user_message
    })
    
    # Update conversation history
    conversation_history.append(f"Me: {user_message}")
    conversation_history.append(f"Bot: {result}")
    conversation_history = conversation_history[-(MAX_CONTEXT_LENGTH * 2):]
    
    return {"response": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)