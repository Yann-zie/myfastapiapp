import json
from pathlib import Path
from typing_extensions import List, TypedDict
import pandas as pd
from langchain import hub
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings 
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langgraph.graph import START, StateGraph

# Import ChatGPTAPI class
from chatgpt_api import ChatGPTAPI

# Initialize ChatGPT API
chatgpt = ChatGPTAPI()

# Initialize OpenAI Embeddings
embeddings = OpenAIEmbeddings()

# Load JSON data
file_path = "advice.json"
loader = JSONLoader(
    file_path=file_path,
    jq_schema=".categories[] | {name: .name, advice: .advice}",
    text_content=False
)
docs = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# Configure vector store and index chunks
vector_store = InMemoryVectorStore(embedding=embeddings)
vector_store.add_documents(documents=all_splits)

# Define application state
class State(TypedDict):
    question: str
    emotion: str
    context: List[Document]
    answer: str

# Define retrieval function
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

# Define response generation function using ChatGPT API
def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    response = chatgpt.get_advice_from_chatgpt(state["emotion"], state["question"])
    return {"answer": response}

# Build the state graph
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

def get_advice(question: str, emotion: str=''):
    """Retrieve and generate advice using RAG."""
    query = {"question": question, "emotion": emotion}
    response = graph.invoke(query)

    if not isinstance(response, dict):  # Ensure response is a dictionary
        return {"answer": str(response)}  # Convert to dictionary format

    return response  # Make sure it's a dict with "answer" key
# Commented out test query for cleaner execution
# query = {"question": "How to keep fit?", "category": "Health & Fitness"}
# response = get_advice(query["question"], query["category"])
# print("Answer:", response)
