"""Vector store service for document management."""
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from backend.config import settings

class VectorService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key
        )
        self.vector_store = Chroma(
            collection_name=settings.vector_collection_name,
            embedding_function=self.embeddings,
            persist_directory=settings.vector_db_path
        )
    
    async def search(self, query: str, k: Optional[int] = None) -> List[Document]:
        k = k or settings.vector_search_k
        return await self.vector_store.asimilarity_search(query, k=k)
    
    async def add_documents(self, documents: List[Document]) -> None:
        await self.vector_store.aadd_documents(documents)