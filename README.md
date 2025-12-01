Samozřejmě. Vytvořit kvalitní `README.md` je stejně důležité jako napsat samotný kód. Je to vizitka vašeho projektu.

Zde je návrh README, který je profesionální, detailní a jasně komunikuje, čeho jste dosáhl. Je napsán v Markdownu, takže ho stačí jen zkopírovat do souboru `README.md` ve vašem repozitáři.

Než to uděláte, musíme vytvořit ještě jeden důležitý soubor.

---

### Krok 1: Vytvoření `requirements.txt`

Pro každého, kdo si bude chtít váš projekt spustit, je klíčové vědět, jaké knihovny si má nainstalovat.

1.  Ujistěte se, že máte aktivované virtuální prostředí `(venv)`.
2.  V terminálu spusťte následující příkaz. Ten automaticky vytvoří soubor se všemi potřebnými závislostmi:
    ```bash
    pip freeze > requirements.txt
    ```
3.  Nyní máte v projektu soubor `requirements.txt`, který bude vypadat přibližně takto (verze se mohou lišit):
    ```
    langchain==0.2.1
    langchain-community==0.2.1
    langchain-core==0.2.3
    langchain-openai==0.1.7
    pdfplumber==0.11.0
    python-dotenv==1.0.1
    faiss-cpu==1.8.0
    ... a další
    ```

### Krok 2: Vytvoření souboru `README.md`

Ve vašem projektu vytvořte nový soubor s názvem `README.md` a vložte do něj následující text.

---

````markdown
# Automated PDF Datasheet Extractor & RAG System

Tento projekt je plně automatizovaná, end-to-end RAG (Retrieval-Augmented Generation) pipeline, která inteligentně extrahuje strukturovaná data z technických PDF datasheetů a umožňuje uživatelům klást dotazy v přirozeném jazyce.

## Motivace

Technické datasheety jsou často jediným zdrojem pravdy pro inženýry a techniky. Tato data jsou však "zamčena" v PDF souborech s komplexními tabulkami, sloučenými buňkami a nestandardním formátováním. Manuální extrakce těchto dat je pomalá, náchylná k chybám a neškálovatelná.

Cílem tohoto projektu bylo vytvořit spolehlivé, opakovatelné datové potrubí, které:
1.  Automaticky parsuje složité PDF tabulky.
2.  Transformuje extrahovaná data do čistého, strojově čitelného formátu.
3.  Vytvoří na těchto datech znalostní bázi a umožní pokládat otázky.

## Klíčové Vlastnosti

*   **Inteligentní Parser PDF:** Využívá `pdfplumber` k přesné extrakci dat z tabulek, včetně správného zpracování sloučených buněk a dynamického přiřazování hodnot k názvům modelů.
*   **End-to-End Automatizace:** Celý proces – od načtení PDF až po odpověď na dotaz – je spuštěn jediným příkazem (`python main.py`) bez potřeby jakýchkoliv mezikroků nebo manuálních zásahů.
*   **Moderní RAG Architektura (LCEL):** Systém je postaven na moderním **LangChain Expression Language (LCEL)**, které zajišťuje transparentnost, modularitu a robustnost.
*   **Výměnný "mozek" (LLM):** Projekt demonstruje, jak výkon jazykového modelu ovlivňuje kvalitu finální odpovědi. Přechodem z `gpt-3.5-turbo` na `gpt-4-turbo-preview` bylo dosaženo schopnosti syntetizovat informace z celého kontextu.
*   **Modulární Design:** Kód je čistě rozdělen na parser (`pdf_parser.py`) a hlavní logiku (`main.py`), což umožňuje snadnou údržbu a další rozšíření.

## Architektura Systému

Systém funguje v několika krocích, které jsou plně zautomatizovány v `main.py`:

```
1. PDF Input
   [MultiPlus.pdf]
       |
       v
2. PDF Parser (pdf_parser.py)
   - Používá pdfplumber k extrakci tabulek
   - Inteligentně zpracovává sloučené buňky
   - Vrací jeden čistý textový řetězec
       |
       v
3. RAG Pipeline (main.py)
   |
   +--> Text Splitting (RecursiveCharacterTextSplitter)
   |      |
   |      v
   +--> Embeddings & Vectorstore (OpenAIEmbeddings -> FAISS)
   |      |
   |      +-----------+
   |      |           |
   |      v           v
   +--> Retriever <- [Uživatelský Dotaz (input)]
          |
          v
   +--> Získání relevantních chunků
          |
          v
4. LCEL Řetězec (create_retrieval_chain)
   - Zkombinuje dotaz a relevantní chunky do promptu
   - Pošle finální prompt do LLM (GPT-4)
       |
       v
5. Finální Odpověď
   [Přesná, kompletní odpověď vygenerovaná LLM]
```

## Struktura Projektu

```
.
├── data/
│   └── MultiPlus.pdf
├── .env
├── .gitignore
├── main.py
├── pdf_parser.py
├── requirements.txt
└── README.md
```

## Setup a Instalace

1.  **Naklonujte repozitář:**
    ```bash
    git clone https://github.com/VASE-JMENO/NAZEV-REPOZITARE.git
    cd NAZEV-REPOZITARE
    ```

2.  **Vytvořte a aktivujte virtuální prostředí:**
    *   **Linux / macOS:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Nainstalujte závislosti:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Nastavte proměnné prostředí:**
    *   Vytvořte v kořenovém adresáři projektu soubor s názvem `.env`.
    *   Do tohoto souboru vložte svůj OpenAI API klíč:
        ```env
        OPENAI_API_KEY="sk-..."
        ```

## Použití

Po dokončení instalace spusťte hlavní skript:
```bash
python main.py
```

Skript automaticky provede celý proces a vypíše finální odpověď na předdefinovaný dotaz. Očekávaný výstup:

```
✅ Konfigurace a klíče načteny.
--- Spouštím inteligentní PDF parser... ---
Nalezeny modely na stránce 34: ['48/3000/35-32 230V', '48/5000/70-50 230V']
Nalezeny modely na stránce 36: ['48/8000/110-100 230V', '48/10000/140-100 230V', '48/15000/ 200-100 230V']
--- PDF parser dokončil práci. ---
--- Zpracovávám data a stavím RAG systém ---
Data rozdělena na 3 částí (chunků).
✅ Vektorová databáze vytvořena.
✅✅✅ Moderní RAG řetězec (LCEL) je připraven. ✅✅✅

Otázka: Jaká je maximální účinnost pro každý model? Vypiš hodnoty přehledně pro všechny nalezené modely.

Odpověď:
- 48/8000/110-100 230V má maximální účinnost 95%
- 48/10000/140-100 230V má maximální účinnost 96%
- 48/15000/200-100 230V má maximální účinnost 95%
- 48/3000/35-32 230V má maximální účinnost 95%
- 48/5000/70-50 230V má maximální účinnost 96%
```

## Možná Budoucí Vylepšení

*   **Interaktivní Rozhraní:** Vytvoření jednoduchého CLI (Command-Line Interface) nebo webového rozhraní (pomocí Streamlit/Gradio), které umožní uživatelům klást vlastní dotazy v reálném čase.
*   **Konverzační Paměť:** Implementace chatovací historie, aby si systém pamatoval kontext konverzace a umožnil doplňující dotazy.
*   **Zpracování Více Dokumentů:** Rozšíření systému pro možnost vytvoření jedné znalostní báze z více PDF souborů najednou.
*   **Optimalizace Nákladů:** Experimentování s jemným laděním (fine-tuning) promptů pro levnější modely (`gpt-3.5-turbo`), aby bylo dosaženo podobné kvality odpovědí s nižšími náklady.

