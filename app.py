import streamlit as st
from backend import llm_pipeline, displayPDF
from translation import translate_to_hindi
import os

# Function to save the uploaded file
def save_uploaded_file(uploaded_file):
    if not os.path.exists('data'):
        os.makedirs('data')

    file_path = os.path.join('data', uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    return file_path

# Streamlit code
st.set_page_config(page_title="Intelligent Document Processing", layout="wide")

# Adjust the sidebar width using custom CSS
st.markdown(""" 
    <style> 
        /* Adjust sidebar width */ 
        .css-1d391kg 
    </style>
""", unsafe_allow_html=True)

def main():
    st.markdown(
        "<h1 style='text-align: center; color: #4CAF50;'>📄Intelligent Document Processing</h1>",  
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Sidebar for module selection
    st.sidebar.header("Module Selection")
    module = st.sidebar.radio("Choose a Module", ("Summary Generator", "Language Translation (English to Hindi)"))
    
    # Add the selected module name above the layout selection
    st.markdown(f"### {module} Module", unsafe_allow_html=True)

    # File uploader for the PDF
    uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf'])
    if uploaded_file is not None:
        filepath = save_uploaded_file(uploaded_file)  # Save the uploaded file and get the file path
        st.markdown("---")
        st.info(f"**Uploaded File**: {uploaded_file.name}")
        
        # Side-by-side layout: document preview on the left and result on the right
        col1, col2 = st.columns([1, 1])  # Equal split for side-by-side layout
        
        with col1:
            # Display document preview in left column
            st.markdown("### Document Preview")
            pdf_display = displayPDF(filepath)
            st.markdown(pdf_display, unsafe_allow_html=True)

        with col2:
            # Only show summary length selection if "Summary Generator" is selected
            if module == "Summary Generator":
                # Dropdown or radio button to select summary length (short or long)
                summary_length = st.radio(
                    "Select the summary length:",
                    options=["Short", "Long"],
                    index=0,  # Default option
                )
                
                # Define summary length parameters based on user choice
                if summary_length == "Short":
                    max_length = 150
                    min_length = 60
                else:  # Long
                    max_length = 500
                    min_length = 200
            else:
                summary_length = None  # No summary length selection for translation module

            # Process button in the right column
            if st.button("Process"):
                if module == "Summary Generator":
                    with st.spinner('Processing...'):
                        summary = llm_pipeline(filepath, max_length, min_length)
                        st.success("Summarization Complete")
                        # Add result box with light background color
                        st.markdown(f"<div style='padding: 20px; background-color: rgba(61, 213, 109, 0.2);; border-radius: 8px;'>"
                                    f"<h4>Summary</h4>{summary}</div>", unsafe_allow_html=True)

                elif module == "Language Translation (English to Hindi)":
                    with st.spinner('Processing...'):
                        translation = translate_to_hindi(filepath)
                        st.success("Translation Complete")
                        # Add result box with light background color
                        st.markdown(f"<div style='padding: 20px; background-color: rgba(61, 213, 109, 0.2);; border-radius: 8px;'>"
                                    f"<h4>Translated Text</h4>{translation}</div>", unsafe_allow_html=True)

    else:
        st.warning("Please upload a PDF file to begin.")

if __name__ == "__main__":
    main()
