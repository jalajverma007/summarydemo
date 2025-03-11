import streamlit as st
from PyPDF2 import PdfReader
import docx
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key =os.getenv("AIKEY")


st.title("Summarizer in English & Hindi")
st.write("upload a file to get is summary")
  
if "content" not in st.session_state:
    st.session_state.content = ""

uploaded_file = st.file_uploader("Upload a .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension == "txt":
        st.session_state.content = uploaded_file.read().decode("utf-8")

    elif file_extension == "pdf":
        pdf_reader = PdfReader(uploaded_file)
        st.session_state.content = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

    elif file_extension == "docx":
        doc = docx.Document(uploaded_file)
        st.session_state.content = "\n".join([para.text for para in doc.paragraphs])

    st.text_area("File Contents:", st.session_state.content, height=300)


def generate_summary(content, language):
    if not content:
        return "No content to summarize."

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are an expert text summarizer. Provide a 500-word summary in {language}."},
            {"role": "user", "content": f"Summarize the following text in {language}:\n\n{content}"}
        ],
        temperature=0.5,
        max_tokens=1000
    )

    return response.choices[0].message.content


if st.button("Generate Summary"):
    with st.spinner("Generating summaries..."):
        english_summary = generate_summary(st.session_state.content, "English")
        hindi_summary = generate_summary(st.session_state.content, "Hindi")

        st.subheader("Summary in English:")
        st.text_area("English Summary:", english_summary, height=300)

        st.subheader("Summary in Hindi:")
        st.text_area("Hindi Summary:", hindi_summary, height=300)
