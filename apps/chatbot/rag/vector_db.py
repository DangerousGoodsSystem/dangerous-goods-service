import os
from django.conf import settings
from langchain.retrievers import EnsembleRetriever
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers import ContextualCompressionRetriever
from dotenv import load_dotenv

load_dotenv()


api_key = settings.OPENAI_API_KEY

filename = "vector_store/indexes"
vector_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


class VectorDB:
    def __init__(self,
                 vector_db=FAISS,
                 embedding=OpenAIEmbeddings(api_key=api_key,
                                            model="text-embedding-3-large")):
        self.vector_db = vector_db
        self.embedding = embedding
        self.db = self._load_or_initialize_db()
        # self.compresor = FlashrankRerank(top_n=6)

    def _initialize_index(self):
        empty_content = " "
        documents = [Document(
            page_content=empty_content,
            metadata={"id": "empty", "page": 1, "source": "empty.pdf"}
        )]
        db = self.vector_db.from_documents(documents=documents, embedding=self.embedding)
        db.save_local(vector_db_path)
        return db

    def _load_or_initialize_db(self):
        """Load existing index or initialize if not found."""
        os.makedirs(vector_db_path, exist_ok=True)

        index_faiss = os.path.join(vector_db_path, "index.faiss")
        index_pkl = os.path.join(vector_db_path, "index.pkl")

        if os.path.exists(index_faiss) and os.path.exists(index_pkl):
            try:
                db = self.vector_db.load_local(
                    vector_db_path,
                    embeddings=self.embedding,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                print(f"⚠️ Lỗi khi load FAISS index: {e}")
                db = self._initialize_index()
        else:
            db = self._initialize_index()

        return db

    def get_retriever(self):
        retriever = self.db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        return retriever
