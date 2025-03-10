from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Chat prompt template
template = """
Use the provided document content to answer the question.
Here is the document content:
{document_content}

Here is the conversation history:
{context}

Question: {question}

Answer:
"""

def setup_llm_chain():
    """Sets up the LangChain pipeline with Ollama."""
    model = OllamaLLM(model="llama3")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain