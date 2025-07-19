import fitz
import streamlit as st

def extract_text(pdf_file):
    with st.spinner("Extracting text from PDF..."):
        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            if not text.strip():
                st.warning("No text found in the PDF file.")
            else:
                st.success("Text extraction complete!")
            return text
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
            return None
        
def display_pdf():
    files = st.file_uploader("Upload a PDF file", type=["pdf"],accept_multiple_files=True)
    for file in files:
        if file is not None:
            text = extract_text(file)
            if text:
                with st.expander("View Extracted Text"):
                    st.text_area("Extracted Text",text, height=300) 

if __name__=="__main__":
    st.set_page_config(page_title="Personal PDF Search Engine", layout="wide")
    st.title("Personal PDF Search Engine")
    display_pdf()