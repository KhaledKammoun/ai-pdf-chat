import time
import sys
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

# Rich for better UI
console = Console()

# Chat prompt template
template = """
Answer the question below.
Here is the conversation history: {context}

Question: {question}

Answer:
"""

# Load the model
model = OllamaLLM(model="llama3")

# Create LangChain pipeline
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Max number of exchanges to keep in memory
MAX_CONTEXT_LENGTH = 5

def print_typing():
    """Simulates a typing indicator in the terminal."""
    for _ in range(3):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.5)
    print("")

def handle_conversation():
    """Handles the conversation loop."""
    context = []
    console.print("[bold cyan]Welcome to the AI ChatBot![/bold cyan] Type 'exit' to quit.")

    while True:
        user_input = Prompt.ask("[bold yellow]You[/bold yellow]")

        if user_input.lower() == "exit":
            console.print("[bold red]Goodbye![/bold red] 👋")
            break

        # Display typing indicator
        console.print("[bold green]Bot is typing[/bold green]", end="")
        print_typing()

        # Generate response
        result = chain.invoke({"context": "\n".join(context), "question": user_input})

        # Display bot response with markdown support
        console.print(Markdown(f"**Bot:** {result}"))

        # Update conversation context (keep only the last MAX_CONTEXT_LENGTH exchanges)
        context.append(f"Me: {user_input}")
        context.append(f"Bot: {result}")
        context = context[-(MAX_CONTEXT_LENGTH * 2):]  # Keep only the last N exchanges

if __name__ == "__main__":
    handle_conversation()
