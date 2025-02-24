1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment:
   2.1. On PowerShell : `.\chatbot\Scripts\Activate.ps1`
   2.2. On Windows Commande prompt : `.\chatbot\Scripts\activate.bat`
   2.2. To close the virtual environement:
   `deactivate`
3. Install dependencies: `pip install -r requirements.txt`
   3.1. NB. or you can install them by writing these lines on terminal :
   `pip install langchain langchain-ollama ollama`
4. Run the development server: `python app.py`
