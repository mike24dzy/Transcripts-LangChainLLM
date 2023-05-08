# Import packages
import os
from getpass import getpass
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
# Chat Models
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain

# Load file and split
def file_load_split(file_path):
    loader = UnstructuredPDFLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    return texts, data

# Initialize openai embeddings and start chromadb
def init_embeddings(api_key, texts_data):
    embeddings = OpenAIEmbeddings(openai_api_key=api_key) # type: ignore
    db = Chroma.from_documents(texts_data, embeddings)
    return db

# Set up QA chain
def qa_docs(database, api_key, query):
    ## What retriever method should I use here? (doc.search)
    retriever = database.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key) # type: ignore
    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
    result = qa({"query": query})
    return result

# Ask for summerization for the whole doc
## This will be more costly due to more api calls to LLM and more token usage
def summarization(api_key, data, query):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key) # type: ignore
    chain = load_qa_chain(llm, chain_type="map_reduce")
    result = chain.run(input_documents=data, question=query)
    return result
