from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain_huggingface import HuggingFaceEmbeddings
# Embedding model (free + lightweight)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Directory for vector DB
VECTOR_DB_PATH = "data/chroma_db"
db = None  # global db object


def load_and_index(pdf_path: str):
    """Load PDF, split into chunks, embed, and store in ChromaDB"""
    global db
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # Create vector DB
    db = Chroma.from_documents(docs, embedding_model, persist_directory=VECTOR_DB_PATH)
    db.persist()
    print(f"✅ Indexed {len(docs)} chunks from {pdf_path}")


def get_retriever(k: int = 3):
    """Return retriever to fetch top-k relevant docs"""
    global db
    if db is None:
        db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embedding_model)
    return db.as_retriever(search_kwargs={"k": k})
