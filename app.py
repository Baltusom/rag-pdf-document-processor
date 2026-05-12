import streamlit as st
import os
import pdfplumber
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="PDF AI Asistent", page_icon="📄", layout="centered")
st.title("📄 PDF AI Asistent")
st.markdown("Nahraj technický PDF soubor a ptej se na jeho obsah přirozeným jazykem.")

uploaded_file = st.file_uploader("Vyber PDF soubor", type=["pdf"])

if uploaded_file:
    pdf_path = f"temp_{uploaded_file.name}"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"✅ Soubor nahrán: {uploaded_file.name}")

    if "full_text" not in st.session_state:
        with st.spinner("Zpracovávám PDF..."):
            try:
                full_text = ""
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        full_text += page.extract_text() or ""

                st.session_state.full_text = full_text
                st.success("✅ Dokument zpracován. Ptej se!")

            except Exception as e:
                st.error(f"Chyba při zpracování: {e}")

    if "full_text" in st.session_state:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        question = st.chat_input("Polož otázku k dokumentu...")

        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Hledám odpověď..."):
                    try:
                        import anthropic

                        client = anthropic.Anthropic(
                            api_key=os.getenv("ANTHROPIC_API_KEY")
                        )

                        context = st.session_state.full_text

                        response = client.messages.create(
                            model="claude-sonnet-4-5",
                            max_tokens=1000,
                            messages=[
                                {
                                    "role": "user",
                                    "content": f"Zde je obsah dokumentu:\n\n{context}\n\nOtázka: {question}\n\nOdpověz přesně na základě dokumentu."
                                }
                            ]
                        )

                        answer = response.content[0].text
                        st.write(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})

                    except Exception as e:
                        st.error(f"Chyba: {e}")