# --- FINÁLNÍ KÓD PRO SPRINT 0 - PRÁCE S ČISTÝMI DATY ---

# 1. Instalace a importy (zůstávají v paměti, ale pro jistotu je tu máme)

import os
import getpass
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Zadejte svůj OpenAI API klíč: ")
print("✅ Klíč API nastaven.")

# 2. Načtení z čistého zdroje pravdy
file_path = "data/cista_data.txt"
loader = TextLoader(file_path)
documents = loader.load()
print(f"✅ Čistá data z '{file_path}' načtena.")

# 3. Zpracování a stavba databáze
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0) # Menší chunky pro přesnost
texts = text_splitter.split_documents(documents)
print(f"Data rozdělena na {len(texts)} částí (chunků).")
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)
print("✅ Vektorová databáze vytvořena.")

# 4. Prompt Engineering pro přesnost
prompt_template = """Jste přesný a precizní technický asistent. Použijte následující kontext k zodpovězení otázky na konci.
- NESHRNUJTE, NEGENERALIZUJTE.
- Vypište každý model a jeho hodnotu samostatně.
- Pokud informace v kontextu není, napište "Informace není v poskytnutém kontextu k dispozici".
Kontext: {context}
Otázka: {question}
Přesná odpověď:"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# 5. Sestavení finálního řetězce
retriever = db.as_retriever(search_kwargs={"k": 5}) # Stačí nám 5, protože máme málo čistých dat
final_qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": PROMPT}
)
print("✅✅✅ Finální QA řetězec je připraven. ✅✅✅\n")

# --- FINÁLNÍ TEST ---
query = "Jaká je maximální účinnost pro každou verzi?"
result = final_qa_chain.invoke({"query": query})
print(f"Otázka: {query}\n")
print(f"Odpověď:\n{result['result']}")