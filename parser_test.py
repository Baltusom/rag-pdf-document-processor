import pdfplumber
import os

# --- KONFIGURACE ---
pdf_path = os.path.join("data", "MultiPLus.pdf")
pages_to_analyze = [33, 35] # Stránky 31 a 33
output_file_path = "automaticky_cista_data.txt"

# --- HLAVNÍ FUNKCE PRO ZPRACOVÁNÍ ---
print("--- START: Automatická extrakce a čištění dat z PDF (Verze 2) ---")

with open(output_file_path, "w", encoding="utf-8") as output_file:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in pages_to_analyze:
                page = pdf.pages[page_num]
                tables = page.extract_tables()
                if not tables:
                    continue

                table = tables[0]

                # Získání názvů modelů z hlavičky
                header_row = [str(cell).replace('\n', ' ') for cell in table[0] if cell and str(cell).strip()]
                model_names = [name.strip() for name in header_row[1:]]

                print(f"Zpracovávám stránku {page_num + 1} s modely: {model_names}")

                # Zpracujeme zbytek řádků
                for row in table[1:]:
                    cleaned_row = [str(cell).replace('\n', ' ') for cell in row if cell and str(cell).strip()]
                    if len(cleaned_row) < 2:
                        continue

                    parameter_name = cleaned_row[0]
                    values = [val.strip() for val in cleaned_row[1:]]

                    # --- ZDE JE TA NOVÁ, CHYTŘEJŠÍ LOGIKA ---
                    output_line = f"- {parameter_name}: "

                    # Případ 1: Jen jedna hodnota pro více modelů (spojená buňka)
                    if len(values) == 1 and len(model_names) > 1:
                        common_value = values[0]
                        for model_name in model_names:
                            output_line += f"{model_name} má hodnotu {common_value}; "

                    # Případ 2: Pro každý model vlastní hodnota
                    else:
                        for i, value in enumerate(values):
                            if i < len(model_names):
                                output_line += f"{model_names[i]} má hodnotu {value}; "
                            else:
                                output_line += f"{value}; "

                    final_line = output_line.strip().rstrip(';') + "\n"
                    output_file.write(final_line)

    except Exception as e:
        print(f"Nastala chyba: {e}")

print(f"\n--- HOTOVO ---")
print(f"✅ Úspěšně vytvořen soubor s čistými daty: '{output_file_path}'")
