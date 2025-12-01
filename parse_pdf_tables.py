#  parse_pdf_tables.py - Náš inteligentní modul pro extrakci dat z PDF

import pdfplumber
import io

def parse_pdf_tables(pdf_path: str, pages: list) -> str:
    """
    Otevře PDF, extrahuje tabulky z daných stránek, vyčistí je
    a vrátí je jako jeden souvislý textový řetězec.
    """
    print("--- Spouštím inteligentní PDF parser... ---")

    # Použijeme StringIO pro efektivní sestavení textu v paměti
    string_io = io.StringIO()

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in pages:
                if page_num >= len(pdf.pages):
                    print(f"Varování: Stránka {page_num + 1} v PDF neexistuje. Přeskakuji.")
                    continue

                page = pdf.pages[page_num]
                tables = page.extract_tables()
                if not tables:
                    continue

                table = tables[0]

                header_row = [str(cell).replace('\n', ' ') for cell in table[0] if cell and str(cell).strip()]
                model_names = [name.strip() for name in header_row[1:]]

                print(f" Nalezeny modely na stránce {page_num + 1}: {model_names}")

                for row in table[1:]:
                    cleaned_row = [str(cell).replace('\n', ' ') for cell in row if cell and str(cell).strip()]
                    if len(cleaned_row) < 2:
                        continue

                    parameter_name = cleaned_row[0]
                    values = [val.strip() for val in cleaned_row[1:]]

                    output_line = f"- {parameter_name}: "

                    if len(values) == 1 and len(model_names) > 1:
                        common_value = values[0]
                        for model_name in model_names:
                            output_line += f"{model_name} má hodnotu {common_value}; "
                    else:
                        for i, value in enumerate(values):
                            if i < len(model_names):
                                output_line += f"{model_names[i]} má hodnotu {value}; "
                            else:
                                output_line += f"{value}; "

                    final_line = output_line.strip().rstrip(';') + "\n"
                    string_io.write(final_line)

    except Exception as e:
        print(f"Chyba v PDF parseru: {e}")
        return "" # V případě chyby vrátíme prázdný text

    print("--- PDF parser dokončil práci. ---")

    # Vrátíme celý sestavený text jako jeden string
    return string_io.getvalue()
