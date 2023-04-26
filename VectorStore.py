#Creates embeddings from local documents (PDF) and stores in a vector database
import os
import re

import fitz
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

load_dotenv()
separator = " "
chunk_size_limit = 1000
max_chunk_overlap = 20
path = os.getenv("PDF_PATH")

def preprocess(text):
    text = text.replace('\n', ' ')
    text = re.sub('\s+', ' ', text)
    return text

def pdf_to_text(path,start_page=1,end_page=None):
    pdf_file = fitz.open(path)
    total_pages = pdf_file.page_count

    if(end_page is None):
        end_page = total_pages
    
    documents = []
    for i in range(start_page-1,end_page):
        text = pdf_file.load_page(i).get_text("text")
        text = preprocess(text)
        doc = Document(page_content=text,metadata={"source":".."})
        documents.append(doc)
    pdf_file.close()

    return documents

def create_vectorstore():
    text_splitter = CharacterTextSplitter(separator=separator,chunk_size=chunk_size_limit,chunk_overlap=max_chunk_overlap)
    split_docs = text_splitter.split_documents(pdf_to_text(path=path))

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(split_docs,embeddings)
    return vector_store