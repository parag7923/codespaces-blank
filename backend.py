import base64
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
import streamlit as st

# Model and tokenizer loading from Hugging Face directly
checkpoint = "MBZUAI/LaMini-Flan-T5-248M"  # Make sure this is the correct model ID
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint, device_map="auto", torch_dtype=torch.float32)

# File loader and preprocessing
def file_preprocessing(file):
    loader = PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    texts = text_splitter.split_documents(pages)
    final_texts = ""
    for text in texts:
        final_texts += text.page_content
    return final_texts

# LLM pipeline for summarization
def llm_pipeline(filepath, max_length, min_length):
    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=max_length,
        min_length=min_length
    )
    input_text = file_preprocessing(filepath)
    result = pipe_sum(input_text)
    return result[0]['summary_text']

# Function to display the PDF of a given file
def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    return pdf_display

# Streamlit UI for file upload and processing
def main():
    st.title("PDF Summarizer")

    # Upload a PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Show the PDF file in Streamlit
        pdf_display = displayPDF(uploaded_file)
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Call the summarization function
        summary = llm_pipeline(uploaded_file)
        st.subheader("Summary:")
        st.write(summary)

if __name__ == "__main__":
    main()
