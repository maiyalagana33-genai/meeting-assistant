from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class MeetingIngester:

    def __init__(self, persist_dir="./chroma_db"):

        # Free local embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Chroma vector DB
        self.vector_store = Chroma(
            persist_directory=persist_dir,
            embedding_function=self.embeddings
        )

        # Text splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    def ingest_meeting(self, text: str, metadata: dict):

        chunks = self.splitter.split_text(text)

        metadatas = [metadata for _ in chunks]

        self.vector_store.add_texts(
            texts=chunks,
            metadatas=metadatas
        )

    def search(self, query: str, k: int = 3):

        return self.vector_store.similarity_search(
            query,
            k=k
        )