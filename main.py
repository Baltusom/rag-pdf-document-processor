# main.py - FINÁLNÍ VERZE, SPOJENÍ SVĚTŮ

import os
from dotenv import load_dotenv
from parse_pdf_tables import parse_pdf_tables
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# --- 1. KONFIGURACE A NAHRÁNÍ DAT ---
load_dotenv()
print("✅ Konfigurace a klíče načteny.")

PDF_FILE_PATH = os.path.join("data", "MultiPLus.pdf")
PAGES_TO_PARSE = [33, 35]

clean_data_string = parse_pdf_tables(pdf_path=PDF_FILE_PATH, pages=PAGES_TO_PARSE)

if not clean_data_string:
    print("❌ Nebyla získána žádná data z PDF. Systém se ukončuje.")
    exit()

# --- 2. ZPRACOVÁNÍ A STAVBA VEKTOROVÉ DATABÁZE ---
print("\n--- Zpracovávám data a stavím RAG systém ---")
documents = [Document(page_content=clean_data_string)]

# ZDE JE FINÁLNÍ ÚPRAVA: Donutíme splitter, aby vytvořil jeden velký chunk
text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)

texts = text_splitter.split_documents(documents)
print(f"Data rozdělena na {len(texts)} částí (chunků).")

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)
print("✅ Vektorová databáze vytvořena.")
llm = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0)
retriever = db.as_retriever() # Už nepotřebujeme specifikovat "k", máme jen pár velkých chunků

# --- 3. SESTAVENÍ ŘETĚZCE POMOCÍ MODERNÍ LCEL ARCHITEKTURY ---

prompt = ChatPromptTemplate.from_template(
    """Jste přesný a precizní technický asistent. Odpovězte na otázku uživatele POUZE na základě poskytnutého kontextu.
Pokud odpověď v kontextu není, řekněte to. Kombinujte informace z celého kontextu pro kompletní odpověď.

Kontext:
{context}

Otázka: {input}

Odpověď:"""
)

document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, document_chain)

print("✅✅✅ Moderní RAG řetězec (LCEL) je připraven. ✅✅✅\n")

# --- 4. FINÁLNÍ TEST ---
query = "Jaká je maximální účinnost pro každý model? Vypiš hodnoty přehledně pro všechny nalezené modely."
result = rag_chain.invoke({"input": query})

print(f"Otázka: {query}\n")
print(f"Odpověď:\n{result['answer']}")

