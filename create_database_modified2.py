import os
import shutil
import openai
import nltk
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
#from langchain.document_loaders import DirectoryLoader, JSONLoader

# Laden der deutschen NLP-Ressourcen
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Lade die Umgebungsvariablen
load_dotenv("settings.env")

# Holt den OpenAI API-Schlüssel
openai_api_key = os.getenv("OPENAI_API_KEY")

CHROMA_PATH = "chroma"
DATA_PATH = "data/german_docs"  # Pfad zu den deutschen Texten

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    # Lade deutsche Dokumente
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf")
    documents = loader.load()
    return documents
'''
def load_documents2():
    # Lade PDF-Dokumente
    pdf_loader = DirectoryLoader(DATA_PATH, glob="*.pdf")
    pdf_documents = pdf_loader.load()

    # Lade JSON-Dokumente
    json_loader = DirectoryLoader(DATA_PATH, glob="*.json", loader_cls=JSONLoader)
    json_documents = json_loader.load()

    # Kombiniere beide Dokumentlisten
    documents = pdf_documents + json_documents
    return documents


def load_documents():
    # Lade PDF-Dokumente
    pdf_loader = DirectoryLoader(DATA_PATH, glob="*.pdf")
    pdf_documents = pdf_loader.load()

    # Definiere ein einfaches Schema, um den gesamten Inhalt zu extrahieren
    jq_schema = "."
    
    # Lade JSON-Dokumente mit dem Schema
    json_loader = DirectoryLoader(DATA_PATH, glob="*.json", loader_cls=JSONLoader, loader_kwargs={"jq_schema": jq_schema})
    json_documents = json_loader.load()

    # Kombiniere beide Dokumentlisten
    documents = pdf_documents + json_documents
    return documents
'''

def split_text_orig(documents: list[Document]):
    # Verwende RecursiveCharacterTextSplitter oder einen splitter basierend auf Worten
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # Sicherstellen, dass wir nicht über die Anzahl der Chunks hinausgehen
    if len(chunks) > 0:
        document = chunks[min(10, len(chunks) - 1)]  # Nimm das 10. Element oder das letzte Element, falls es weniger als 10 gibt
        print(document.page_content)
        print(document.metadata)

    return chunks

def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()