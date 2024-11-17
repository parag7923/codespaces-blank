from googletrans import Translator
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def translate_to_hindi(file_path):
    # Initialize translator
    translator = Translator()

    # Load PDF and preprocess text
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    texts = text_splitter.split_documents(pages)
    input_text = "\n".join([text.page_content for text in texts])

    try:
        # Translate text
        translated_text = translator.translate(input_text, src='en', dest='hi').text
    except Exception as e:
        translated_text = f"Error occurred during translation: {e}"

    return translated_text
